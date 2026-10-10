NAME = "funding"
SUBJECT = "AI Startup Funding & Programmes"
EXTRA_LABEL = "Amount / type"

# Edit this to describe your ventures and stage; the sharper it is, the better the scoring.
PROFILE = """
Founder-led AI-focused startups based in Kenya / East Africa, early stage (idea to seed).
Interested in grants, equity-free funding, pre-seed and seed investment, accelerators, incubators,
competitions, cloud/AI credits, and pilot or procurement programmes. Open to opportunities open to
African, Kenyan or East African founders, and global programmes that accept African applicants.
Sector-agnostic unless noted here: [add your sectors, e.g. fintech, agri/climate, edtech].
"""

CRITERIA = """a real, currently open funding or support opportunity a startup can apply to: grant,
investment call, accelerator or incubator cohort, competition with prizes, credits programme, or
fellowship for founders. Reject: news about funding already given, generic articles, paid 'apply
for a fee' schemes, loan-shark or advance-fee style offers, and expired calls. Prefer AI-related
or open-to-all-tech programmes eligible to Kenyan / African founders.
'extra' = funding amount and type if stated (e.g. 'USD 50k grant', 'equity-free', 'credits'), else Unknown."""

def _g(q):
    import urllib.parse
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + " when:14d", "hl": "en-KE", "gl": "KE", "ceid": "KE:en"})

FEEDS = {
    "Calls: AI startup Africa": _g('"call for applications" AI startups Africa'),
    "Calls: Kenya startups": _g('Kenya startups "applications open" OR "call for proposals" funding'),
    "Calls: grants African founders": _g('grant African founders AI "applications" 2026'),
    "Calls: accelerator Africa": _g('accelerator OR incubator "applications" Africa AI 2026'),
    "Calls: climate/agri tech": _g('"applications open" agritech OR climatetech OR greentech Africa startups'),
    "Calls: fintech": _g('"applications open" fintech startups Africa funding'),
    "Calls: Mastercard/AfDB/EU": _g('Mastercard Foundation OR AfDB OR "European Union" startup challenge Africa AI call'),
    "Calls: Google/Microsoft/AWS": _g('"Google for Startups" OR "Microsoft for Startups" OR "AWS Activate" Africa AI program'),
    "Source: Devex funding": _g('site:devex.com funding opportunity AI innovation Africa'),
    "Source: FundsforNGOs": _g('site:fundsforngos.org AI OR innovation OR startup Africa'),
    "Source: Opportunity Desk": _g('site:opportunitydesk.org startup OR entrepreneur AI Africa'),
    "Source: TechCabal": _g('site:techcabal.com accelerator OR grant OR "applications open"'),
    "Source: Disrupt Africa": _g('site:disruptafrica.com accelerator OR grant OR competition applications'),
    "Source: Techpoint": _g('site:techpoint.africa grant OR accelerator OR "applications open"'),
    "Kenya: ICT Authority / KeNIA": _g('Konza OR "ICT Authority" OR KeNIA OR "Kenya Innovation Agency" startups call AI'),
    "Kenya: Safaricom/Ecosystem": _g('Safaricom OR Villgro OR "Kenya Climate Innovation Center" OR "iHub" startup programme applications'),
    # "Alert: my phrase": "https://www.google.com/alerts/feeds/XXXX/YYYY",
}

# ---- Free keyword scoring (no API) ---------------------------------------
MUST_HAVE_ANY = ["apply", "applications", "call for", "grant", "accelerator", "incubator",
                 "competition", "challenge", "fellowship", "credits", "funding", "prize", "cohort"]
POSITIVE = {
    "ai": 3, "artificial intelligence": 3, "machine learning": 2, "startup": 2, "start-up": 2, "founder": 1,
    "africa": 2, "kenya": 3, "east africa": 3, "nairobi": 1,
    "applications open": 3, "call for applications": 3, "call for proposals": 3, "deadline": 2,
    "grant": 2, "equity-free": 3, "pre-seed": 2, "seed": 1, "credits": 2, "prize": 1,
    "agritech": 1, "climate": 1, "fintech": 1, "edtech": 1, "greentech": 1,
}
NEGATIVE = ["raises", "raised", "secures", "closes", "closed", "winners announced", "announces winners",
            "registration fee", "application fee", "processing fee", "loan"]
