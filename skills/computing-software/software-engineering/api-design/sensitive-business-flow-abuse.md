---
id: computing-software.software-engineering.api-design.sensitive-business-flow-abuse
name: sensitive-business-flow-abuse
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, business-flow-abuse, owasp-api-top-10, bots, scalping, referral-abuse, anti-automation, api-security]
level: advanced
status: docs-checked
description: "Defend sensitive business flows (OWASP API6:2023) such as checkout, signup and referral from automated abuse using flow-level limits, not only request rate limits."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/", "https://owasp.org/www-project-automated-threats-to-web-applications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unrestricted access to sensitive business flows (OWASP API6:2023)

The API works exactly as designed, yet automation harms the business. OWASP examples: buying all stock of a high-demand item to resell (scalping), spamming posts or comments, reserving every available time slot, booking most seats and cancelling at once, and scripted sign-ups that farm referral credit. Technical impact is usually small; the harm is to the business. What counts as risky varies: a script posting may be spam on one network and encouraged on another.

## Approach
OWASP plans mitigation in two layers: business (identify flows that excessive use would harm) and engineering (pick protections that match the risk).
1. List the flows whose automation costs money (purchasing, reservations, posting, sign-up and referral rewards) and rank by harm.
2. Slow automation with the mechanisms OWASP lists:
   - Device fingerprinting: deny unexpected client devices such as headless browsers, which pushes attackers to costlier tooling.
   - Human detection: captcha or more advanced biometrics such as typing patterns.
   - Non-human patterns: analyse the user flow, for example "add to cart" then "complete purchase" in under one second.
   - Consider blocking IP addresses of Tor exit nodes and well-known proxies (expect false positives).
3. Add flow-specific business limits that follow from the scenarios (design suggestions, not an OWASP list): a per-account cap or hold expiry on reservations and carts, and paying referral rewards only after a verified first purchase.
4. Secure and limit machine-consumed APIs (developer and B2B APIs); they are easy targets because they often lack the protections above.
5. Instrument the flow: count completions per account, payment instrument and address, and alert on outliers. OWASP lists insufficient logging and monitoring as a related reference.

## Gotchas
- Scenario #1 shows the attacker distributing purchases across many IP addresses and locations, so plain per-IP limits fail; limit by account and business entity as well.
- Do not leak the reason for a block; it teaches the attacker.
- For terminology of automated threats, see the OWASP Automated Threats to Web Applications project (Automated Threat Handbook).

Verify: script the flow with a headless client at 10x human speed and from many IPs; confirm flow-level caps or step-up challenges trigger while a normal session still completes.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API6 and the OWASP Automated Threats to Web Applications project page (a landing page; only the project's existence and the Automated Threat Handbook are used). Removed: the control table (email/phone verification, proof-of-work, queue or lottery, identity binding, uniform responses), the signal-scoring and step-up-challenge approach, and the residential-proxy claim, none of which appear on the pages. Items in step 3 are marked as design suggestions.
Method: documentation only; no commands were run.
