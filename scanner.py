"""
Opportunity scanner: collect -> dedupe -> score with Claude -> email digest.
Usage: python scanner.py instructor | funding | all
"""
import os, sys, json, hashlib, smtplib, ssl, html, datetime, importlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import feedparser

RECIPIENT = os.environ.get("DIGEST_TO", "john.weru@konzaltant.com")
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_APP_PASSWORD"]
MIN_SCORE = int(os.environ.get("MIN_SCORE", "4"))
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
SCORER = os.environ.get("SCORER", "keywords")   # "keywords" = free, "claude" = needs ANTHROPIC_API_KEY

def collect(cfg):
    items = []
    for name, url in cfg.FEEDS.items():
        try:
            for e in feedparser.parse(url).entries[:25]:
                items.append({"source": name,
                              "title": html.unescape(e.get("title", "")).strip(),
                              "link": e.get("link", ""),
                              "summary": html.unescape(e.get("summary", ""))[:500],
                              "published": e.get("published", "")})
        except Exception as ex:
            print(f"[warn] {name}: {ex}")
    return items

def key(i): return hashlib.sha1((i["title"].lower() + i["link"]).encode()).hexdigest()

def dedupe(items, seen_file):
    seen = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()
    fresh, batch = [], set()
    for i in items:
        k = key(i)
        if k in seen or k in batch: continue
        batch.add(k); fresh.append(i)
    return fresh, seen | batch

def keyword_score(cfg, items):
    """Free scoring: weighted keyword matching, no API needed."""
    out = []
    for c in items:
        text = (c["title"] + " " + c["summary"]).lower()
        if any(n in text for n in cfg.NEGATIVE): continue
        if not any(m in text for m in cfg.MUST_HAVE_ANY): continue
        pts = sum(w for k, w in cfg.POSITIVE.items() if k in text)
        sc = min(10, round(pts * 10 / 14))   # ~14 points of matches = 10/10
        matched = [k for k in cfg.POSITIVE if k in text][:5]
        c.update(score=sc, org=c["source"], deadline="See listing", extra="",
                 why="Matched: " + ", ".join(matched) if matched else "Weak match")
        out.append(c)
    return sorted([o for o in out if o["score"] >= MIN_SCORE], key=lambda x: -x["score"])

def score(cfg, items):
    if SCORER != "claude":
        return keyword_score(cfg, items)
    import anthropic
    client = anthropic.Anthropic()
    scored = []
    for start in range(0, len(items), 15):
        chunk = items[start:start + 15]
        listing = "\n".join(f"{n}. [{c['source']}] {c['title']} | {c['summary']} | {c['published']}"
                            for n, c in enumerate(chunk))
        prompt = f"""You screen opportunities for this person/organisation:
{cfg.PROFILE}
Today is {datetime.date.today()}. For each numbered item decide whether it is {cfg.CRITERIA}
Return ONLY a JSON array of objects:
{{"i": number, "score": 0-10 fit, "org": "organisation or Unknown", "deadline": "date or Unknown",
"extra": "see above", "why": "one short sentence on fit, eligibility and next step"}}.
Items:
{listing}"""
        try:
            r = client.messages.create(model=MODEL, max_tokens=2000,
                                       messages=[{"role": "user", "content": prompt}])
            txt = r.content[0].text.strip().replace("```json", "").replace("```", "")
            for row in json.loads(txt):
                c = chunk[row["i"]]
                c.update(score=row["score"], org=row["org"], deadline=row["deadline"],
                         extra=row.get("extra", ""), why=row["why"])
                scored.append(c)
        except Exception as ex:
            print(f"[warn] scoring chunk failed: {ex}")
    return sorted([s for s in scored if s["score"] >= MIN_SCORE], key=lambda x: -x["score"])

def send(cfg, hits):
    today = datetime.date.today().strftime("%d %b %Y")
    rows = "".join(
        f"""<tr><td style="padding:10px 0;border-bottom:1px solid #eee">
        <b>{h['score']}/10</b> &middot; <a href="{h['link']}">{html.escape(h['title'])}</a><br>
        <span style="color:#555">{html.escape(h['org'])} &middot; Deadline: {html.escape(h['deadline'])}
        &middot; {cfg.EXTRA_LABEL}: {html.escape(str(h.get('extra','')))}
        &middot; {html.escape(h['source'])}</span><br>{html.escape(h['why'])}</td></tr>""" for h in hits)
    body = f"""<div style="font-family:Arial,sans-serif;max-width:680px">
    <h2>{cfg.SUBJECT} &mdash; {today}</h2>
    <p>{len(hits)} new match(es) scoring {MIN_SCORE}+ out of 10.</p>
    <table width="100%">{rows}</table>
    <p style="color:#888;font-size:12px">Verify each listing at its source before applying.
    Never pay a fee to apply for funding.</p></div>"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{cfg.SUBJECT}: {len(hits)} new ({today})"
    msg["From"], msg["To"] = SMTP_USER, RECIPIENT
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(SMTP_USER, [RECIPIENT], msg.as_string())

def run(name):
    cfg = importlib.import_module(f"configs.{name}")
    seen_file = Path(f"seen_{name}.json")
    items = collect(cfg)
    fresh, seen = dedupe(items, seen_file)
    print(f"[{name}] collected {len(items)}, {len(fresh)} new")
    hits = score(cfg, fresh) if fresh else []
    print(f"[{name}] {len(hits)} matches")
    if hits: send(cfg, hits)
    seen_file.write_text(json.dumps(sorted(seen)))

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    for n in (["instructor", "funding"] if target == "all" else [target]):
        run(n)
