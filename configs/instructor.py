NAME = "instructor"
SUBJECT = "AI Instructor Opportunities"
EXTRA_LABEL = "Type"   # shown in the email next to the deadline

PROFILE = """
Consultant and trainer, 25+ years teaching experience. Founder of an AI, automation and digital
consulting firm in East Africa. Wants AI instructor / trainer / facilitator / curriculum roles and
training consultancies. Based in Nairobi, wants to establish mainly in Mombasa / coast; also open
to remote and regional (East Africa) work. Subjects: AI literacy, generative AI, agentic AI,
automation, digital skills, AI for sectors (law, energy, governance, SMEs).
"""

CRITERIA = """a genuine opportunity to be hired, contracted or to apply as an AI instructor, trainer,
facilitator or training consultant (not news, not an ad for a course to buy, not expired).
'extra' = contract type (job, consultancy, tender, bootcamp, other)."""

def _g(q):
    import urllib.parse
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + " when:7d", "hl": "en-KE", "gl": "KE", "ceid": "KE:en"})

FEEDS = {
    "News: AI trainer Kenya": _g('"AI trainer" OR "AI instructor" OR "AI facilitator" Kenya'),
    "News: call for trainers": _g('"call for trainers" OR "expression of interest" training "artificial intelligence" Africa'),
    "News: digital skills training": _g('"digital skills" training consultancy Kenya OR Tanzania OR Rwanda OR Uganda'),
    "News: Mombasa AI training": _g('AI training Mombasa OR Kilifi OR Kwale OR Coast'),
    "Jobs: BrighterMonday": _g('site:brightermonday.co.ke AI trainer OR instructor OR facilitator'),
    "Jobs: MyJobMag": _g('site:myjobmag.co.ke trainer AI OR "digital skills"'),
    "Jobs: Fuzu": _g('site:fuzu.com instructor AI OR "data" OR "digital skills"'),
    "Tenders: UNGM": _g('site:ungm.org training consultancy artificial intelligence Africa'),
    "Tenders: ReliefWeb": _g('site:reliefweb.int trainer OR consultant AI Kenya'),
    "Tenders: DevEx": _g('site:devex.com AI training Africa consultant'),
    "Tenders: Kenya portal": _g('tenders.go.ke OR PPIP training ICT consultancy'),
    "Bootcamps/Edu": _g('"instructor" AI bootcamp Kenya Moringa OR Zindua OR "Power Learn Project" OR university'),
    # "Alert: my phrase": "https://www.google.com/alerts/feeds/XXXX/YYYY",
}

# ---- Free keyword scoring (no API) ---------------------------------------
# Each hit adds its weight; any NEGATIVE term disqualifies the item.
MUST_HAVE_ANY = ["trainer", "instructor", "facilitator", "training", "curriculum", "lecturer", "tutor", "coach"]
POSITIVE = {
    "ai": 3, "artificial intelligence": 3, "generative ai": 3, "chatgpt": 2, "agentic": 3,
    "automation": 2, "digital skills": 2, "data": 1, "machine learning": 2,
    "consultancy": 2, "consultant": 1, "expression of interest": 2, "call for": 1, "tender": 1,
    "mombasa": 3, "kilifi": 3, "mtwapa": 3, "coast": 2, "kwale": 2,
    "kenya": 2, "east africa": 2, "remote": 2, "tanzania": 1, "rwanda": 1, "uganda": 1,
}
NEGATIVE = ["enroll now", "enrol now", "buy course", "discount", "% off", "webinar replay", "obituary"]
