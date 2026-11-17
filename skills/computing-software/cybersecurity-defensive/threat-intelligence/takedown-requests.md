---
id: computing-software.cybersecurity-defensive.threat-intelligence.takedown-requests
name: takedown-requests
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [digital-risk-protection, takedown-requests, abuse-reporting, registrar-abuse, hosting-abuse, udrp, phishing-takedown]
level: practitioner
status: draft
description: "Get phishing and impersonation content removed: collect evidence, report to hosting providers, registrars, CDNs and platforms, use browser blocklists and escalate to UDRP when needed."
sources: ["ICANN - Registrar Accreditation Agreement abuse contact obligations", "Anti-Phishing Working Group (APWG) reporting", "WIPO - Uniform Domain-Name Dispute-Resolution Policy (UDRP)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Takedown requests

**Goal:** malicious sites, domains and accounts impersonating you come down fast, and users are protected while they are up.

## Evidence package
URL(s), screenshots with timestamps, HTML source/HAR, WHOIS/RDAP, DNS records, hosting IP and ASN, certificate details, phishing kit artefacts, examples of phishing emails (headers), and how it infringes (trademark, impersonation, credential harvesting).

## Report in parallel
1. **Hosting provider** abuse contact (from RDAP for the IP / `abuse-c` in RIR WHOIS; e.g. `whois -h whois.arin.net <ip>`).
2. **Registrar** abuse contact (RDAP for the domain; ICANN requires registrars to publish abuse contacts and respond to reports). Ask for suspension (`clientHold`).
3. **CDN/proxy** (Cloudflare abuse form) - they forward to the host and can add interstitial warnings.
4. **Browser protections:** Google Safe Browsing report, Microsoft SmartScreen report, Netcraft, APWG (eCrime exchange) - often the fastest user protection.
5. **Platforms:** social media impersonation forms, app stores, code hosts, URL shorteners, email providers for sending accounts.
6. **Your own controls:** block internally, email gateway rules, inform helpdesk/customers if relevant.

## Follow-up
Track each report: provider, time sent, ticket id, status; resend/escalate after 24-48 h. Check for redeployment to new domains (same kit/IP).

## Escalation
- UDRP (WIPO, Forum) for trademark-infringing domains used in bad faith - transfers the domain, takes weeks and costs fees.
- URS (for gTLDs) for clear-cut cases - suspension, faster and cheaper.
- Law enforcement or national CERT for fraud at scale; DRP vendors with established provider relationships when volume is high.

## Gotchas
- Reporting only to the registrar of a domain on compromised legitimate hosting (the site owner is a victim too; contact host/owner to clean).
- Sending threatening legal letters to bulletproof hosts - focus on browser blocklists and registries.

## Verify
- [ ] Takedown tracker shows time to takedown per case; median reported monthly.
- [ ] Browser blocklist reports submitted for every active phishing URL.
