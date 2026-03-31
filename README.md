# LLM Red Team Kit
> Automated adversarial testing framework for LLM-powered applications
> covering OWASP LLM Top 10 vulnerability classes

## What it does
- Fires 30+ adversarial payloads across 3 attack categories
- Auto-scores responses using heuristic + LLM-judge pipeline  
- Generates professional VAPT-style PDF reports
- Includes VulnBot: a deliberately insecure target app for testing

## Attack categories covered
| Category | OWASP ID | Payloads |
|---|---|---|
| Prompt Injection | LLM01 | 10 |
| Sensitive Info Disclosure | LLM06 | 10 |
| Jailbreak / Safety Bypass | LLM04 | 10 |

## Sample results
[Screenshot of terminal output]
[Screenshot of PDF report first page]

## Architecture
[Link to architecture diagram]

## Setup
```bash
pip install -r requirements.txt
python vulnbot/app.py &
python redteamkit/runner.py
```

## Disclaimer
Built for educational purposes only. Test only systems you own or have permission to test.
