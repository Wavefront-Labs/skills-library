---
id: computing-software.digital-privacy-hygiene.phishing-awareness.checking-links-with-url-scanners
name: checking-links-with-url-scanners
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, url-scanner, link-inspection, phishing]
level: practitioner
status: draft
description: "Check suspicious links safely with urlscan.io, VirusTotal, Safe Browsing status and redirect tracing, without leaking private tokens or visiting the page."
sources:
  - "https://urlscan.io/about/"
  - "https://docs.virustotal.com/docs/how-it-works"
  - "https://transparencyreport.google.com/safe-browsing/search"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Checking links with URL scanners

**Goal:** find out where a link goes and whether it's known-bad without opening it in your normal browser.

## Expand first
Hover (desktop) or long-press (mobile) to see the real URL. For shortened links, trace redirects without rendering:
```
curl -sIL --max-redirs 10 "https://short.example/abc" | grep -iE '^(HTTP|location)'
```

## Scanners
| Tool | Gives | Privacy note |
|---|---|---|
| urlscan.io | Screenshot, redirects, contacted domains, verdicts | Scans are **public** by default; choose Unlisted or Private |
| VirusTotal (URL) | Verdicts from many engines | Submissions are shared with the security community |
| Google Safe Browsing site status | Whether Google flags the domain | Lookup only |
| Domain age (whois) | Newly registered domains are suspicious | `whois example.com` creation date |

## Don't submit
Links that contain personal tokens: password reset links, document share links, unsubscribe links with your
email, invoice links. Scanning them publicly can expose your account or document. Strip the query string or skip.

## Interpreting
- "Clean" doesn't mean safe: new phishing sites aren't on lists for hours.
- A screenshot showing a Microsoft/Google login on a non-Microsoft/Google domain = phishing.

## Gotchas
- Some phishing kits show harmless pages to scanners (cloaking); the screenshot may look benign.
- Opening the link "just to see" in a normal browser can trigger drive-by downloads or confirm your address.
