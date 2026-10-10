# Opportunity Scanner (AI instructor roles + AI startup funding)

Runs two separate digests daily, each scored against its own profile with Claude and emailed to john.weru@konzaltant.com:
- `configs/instructor.py` - AI instructor / trainer opportunities
- `configs/funding.py` - AI startup funding, grants, accelerators, credits

## Setup (10 minutes)
1. Create a private GitHub repo and upload these files (keep the `.github/workflows` folder).
2. Gmail: turn on 2-step verification, then create an App Password (Google Account > Security > App passwords).
3. Repo > Settings > Secrets and variables > Actions, add:
   - `SMTP_USER` (the Gmail address that sends the digest)
   - `SMTP_APP_PASSWORD`
4. Actions tab > "Opportunity scan" > Run workflow to test. It then runs weekdays at 08:00 EAT.

## Cost
Runs free: GitHub Actions (private repos get 2,000 free minutes/month; this uses ~1 minute a day), Google News RSS, and Gmail. Scoring uses keyword rules by default (`SCORER=keywords`), so no API key is needed. To upgrade later, set `SCORER=claude` in the workflow, add an `ANTHROPIC_API_KEY` secret, and restore `anthropic` in requirements.

## Tuning
- Keyword mode: edit `POSITIVE` (weights), `NEGATIVE` (disqualifiers) and `MUST_HAVE_ANY` at the bottom of each file in `configs/`. `PROFILE` is only used in Claude mode.
- Add sources to `FEEDS` in the relevant config (Google Alerts RSS URLs work well).
- Raise or lower `MIN_SCORE` (default 4 in keyword mode; try 6 in Claude mode) to control volume.
- Run locally: `pip install -r requirements.txt` then set the env vars and run `python scanner.py instructor`, `python scanner.py funding` or `python scanner.py all`.
- To add a third digest, copy a file in `configs/`, edit it, and add its name to the list in `scanner.py`.
