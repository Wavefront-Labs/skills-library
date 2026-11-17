---
id: computing-software.digital-privacy-hygiene.phishing-awareness.reporting-sites-to-safe-browsing
name: reporting-sites-to-safe-browsing
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, safe-browsing-report, google-safe-browsing, smartscreen, reporting-phishing]
level: practitioner
status: draft
description: "Report phishing and malware sites to Google Safe Browsing and Microsoft SmartScreen so browsers start warning everyone, and check a site's status."
sources:
  - "https://safebrowsing.google.com/safebrowsing/report_phish/"
  - "https://transparencyreport.google.com/safe-browsing/search"
  - "https://feedback.smartscreen.microsoft.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reporting a site to Google Safe Browsing

**Goal:** turn one person's suspicion into a browser warning for billions of users, usually within hours.

## Google Safe Browsing (Chrome, Firefox, Safari use its lists)
1. Go to `safebrowsing.google.com/safebrowsing/report_phish/` and paste the full URL (from the email link, copied
   without visiting if possible).
2. Add a short note (what brand it impersonates).
3. Malware sites: use the "report malware" form; false positives on your own site go through Search Console.
4. In Chrome: three-dot menu > Help > Report an issue, or use the Suspicious Site Reporter where available.

Check status: Google Transparency Report > Safe Browsing site status.

## Microsoft SmartScreen (Edge, Windows)
In Edge: menu > Help and feedback > **Report unsafe site**; or the SmartScreen feedback page. Outlook users can
also use Report > Report phishing.

## Others worth hitting
- The impersonated company's abuse address (often `phishing@brand` or `abuse@`).
- The domain registrar and host (found via WHOIS/RDAP) abuse contacts.
- APWG: forward the phishing email to `reportphishing@apwg.org`.
- Netcraft's report form feeds many blocklists.

## Gotchas
- Don't log in or submit test data to "see what happens"; your IP and any data go to the attacker.
- Shortened URLs: expand them with a preview service and report the final destination plus the shortener.
