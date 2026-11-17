---
id: computing-software.qa-testing-engineering.test-automation.burp-suite-manual-security-testing
name: burp-suite-manual-security-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [burp-suite, security-testing, intercepting-proxy, manual-pentest, owasp-wstg]
level: advanced
status: draft
description: "Use Burp Suite for manual web security testing: proxy setup and CA certificate, scope, Repeater, Intruder, Comparer, Sequencer and logging evidence."
sources:
  - https://portswigger.net/burp/documentation/desktop
  - https://owasp.org/www-project-web-security-testing-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manual security testing with Burp Suite

**Goal:** inspect and tamper with every request between browser and server to find access control, injection and logic flaws the scanner misses. Only on targets you have written authorisation for.

## Setup
1. Start Burp (Community or Professional). Use the built-in Chromium (**Proxy > Intercept > Open browser**), which is pre-configured; otherwise proxy the browser to `127.0.0.1:8080`.
2. External browser or mobile device: visit `http://burpsuite`, download the CA certificate and install it as a trusted root (Android 7+ apps ignore user CAs unless the app's network security config allows them).
3. **Target > Scope:** add the target host and tick "show only in-scope items" in HTTP history so noise is hidden.

## Core tools
- **Proxy > HTTP history:** browse the whole app once as each role to build the site map.
- **Repeater (Ctrl+R):** resend a request with edits: change IDs (IDOR), drop auth headers, alter prices or quantities, switch methods.
- **Intruder:** mark payload positions and run lists (Community is throttled): ID ranges, fuzz strings, username lists. Attack types: Sniper (one position), Pitchfork (paired lists), Cluster bomb (all combinations).
- **Comparer:** diff two responses (valid vs invalid user) to spot enumeration.
- **Sequencer:** analyse token randomness from a live capture.
- **Decoder:** base64/URL/hex encode and decode, including JWT parts.
- **Match and replace** rules: e.g. strip `X-Frame-Options` or swap a role cookie automatically.
- Professional only: active Scanner, Collaborator for out-of-band (blind SSRF, blind XSS) detection.

## Access control routine
Log in as a low-privilege user in one browser, an admin in another; replay admin requests with the low-privilege cookie (extensions such as Autorize automate this).

## Evidence
Save the project file; for each finding keep the exact request and response, and annotate items with highlights and comments.

## Verify
Every in-scope endpoint in the site map has been exercised in Repeater with at least the authorisation and tampering checks, and findings have reproducible request/response pairs.
