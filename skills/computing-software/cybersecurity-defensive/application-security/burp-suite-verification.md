---
id: computing-software.cybersecurity-defensive.application-security.burp-suite-verification
name: burp-suite-verification
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [burp-suite, appsec-verification, finding-validation, repeater, autorize, manual-testing]
level: practitioner
status: docs-checked
description: "Use Burp Repeater to reproduce and retest findings and the Autorize extension to check authorisation enforcement in applications you are authorised to test."
sources: ["https://portswigger.net/burp/documentation/desktop/tools/repeater", "https://raw.githubusercontent.com/PortSwigger/autorize/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Burp Suite for AppSec verification

Only test applications you own or are authorised to test.

## Repeater
Burp Repeater modifies and sends an interesting HTTP or WebSocket message over and over. The
documentation lists these uses:
- Send a request with varying parameter values to test for input-based vulnerabilities.
- Send a series of HTTP requests in a specific sequence to test multi-step processes, or
  vulnerabilities that rely on manipulating connection state.
- Manually verify issues reported by Burp Scanner.

Each message gets its own tab; modifications are saved in the tab history, tabs can be grouped,
and HTTP tabs accept notes. Repeater is in both Professional and Community editions. Use it to
reproduce a reported request, then resend it and variants after the fix is deployed.

## Autorize extension
Autorize is an open-source extension that detects missing authorization and authentication
enforcement. It watches traffic from a high-privileged user and replays each request with a
low-privileged user's credentials and unauthenticated, then compares the responses.
- Needs Burp (Community or Professional) and a Jython standalone JAR set in the Python
  environment; install from the BApp Store (recommended) or by adding `Autorize.py`.
- Workflow: in Autorize Configuration insert the low-privileged user's Cookie or Authorization
  header (it replaces the header if present and adds it if missing). Optionally keep Check
  unauthenticated and Intercept requests from Repeater on. Click "Intercept is off" to start,
  proxy the browser through Burp, browse as the high-privileged user, then inspect each entry:
  original, modified and unauthenticated request and response.
- Statuses: Bypassed! (not enforced), Enforced!, and Is enforced??? (needs manual fingerprint
  configuration).
- Enforcement detectors match on response body (string or regular expression), headers, content
  length or full response, for example the text `You are not authorized to perform this action`.
- Interception filters: Burp scope, whitelist, blacklist and regular expressions; images and
  scripts are excluded by default.
- Several low-privileged users can be compared side by side.
- The README warns that it relies on response comparison heuristics, so false positives and
  false negatives are possible and complex authorization logic may need detector tuning.
  Review flagged entries manually.

## Verify
- [ ] Each fixed finding has a reproduced request and a retest of the same request and variants.
- [ ] Autorize results were reviewed manually, with detectors tuned where status was uncertain.

## Checked
Confirmed 2026-11-09 against the PortSwigger Burp Repeater documentation page and the Autorize README.
Removed as unconfirmed: proxy listener and CA setup, target scope steps, Intruder, Comparer, Scanner, Collaborator and Logger guidance, Community edition throttling, session handling macros, the PortSwigger desktop landing page (not read), and the production-testing gotchas.
Method: docs-checked 2026-11-09 against portswigger.net Burp Repeater documentation and the PortSwigger/autorize README on raw.githubusercontent.com
