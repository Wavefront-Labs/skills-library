---
id: computing-software.cybersecurity-defensive.threat-intelligence.lookalike-domain-monitoring
name: lookalike-domain-monitoring
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [digital-risk-protection, lookalike-domain-monitoring, typosquatting, dnstwist, certificate-transparency, brand-impersonation, phishing-domains]
level: practitioner
status: draft
description: "Monitor for lookalike and typosquat domains of your brands with dnstwist and certificate transparency, triage registrations, block internally and escalate to takedown."
sources: ["dnstwist project documentation", "Certificate Transparency - RFC 9162 and crt.sh", "ICANN - Domain name abuse and registrar abuse contacts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lookalike domain monitoring

**Goal:** find newly registered domains impersonating your brands early, before phishing or fraud campaigns use them.

## Generate and check permutations
```
dnstwist --registered --format csv --mxcheck --lsh --whois corp-example.com > lookalikes.csv
dnstwist --dictionary words.txt --tld tlds.txt --registered corp-example.com
```
Fuzzers: addition, bitsquatting, homoglyph (IDN like `corp-exаmple.com` with Cyrillic a), hyphenation, insertion, omission, repetition, replacement, subdomain, transposition, vowel-swap, dictionary (`corp-example-login.com`), TLD swaps.

## Certificate transparency
Monitor CT logs for certificates containing your brand strings: crt.sh queries (`%corpexample%`), certstream real-time feed, or commercial monitoring. Attackers get certificates within minutes of setting up phishing sites.

## Triage each hit
- Registered date, registrar, name servers, MX records (MX present = email-capable, higher risk for BEC), web content (screenshot via urlscan with private visibility), similarity score (LSH/fuzzy hash vs your site).
- Classify: defensive registration by you, unrelated legitimate business, parked/for sale, active phishing/fraud.

## Actions
- Block internally (DNS RPZ, proxy, email gateway) for suspicious/active domains.
- Watchlist parked domains for changes (MX/A record or content change triggers re-triage).
- Active abuse -> takedown process; notify customers if impersonation targets them.
- Defensive registration of the most obvious variants and key TLDs; set DMARC `p=reject` and null MX on non-sending domains you own.

## Gotchas
- Huge volumes for short brand names; prioritise by MX presence, content similarity and keywords (login, secure, invoice).
- Homoglyph IDNs display differently by browser; check punycode (`xn--`).

## Verify
- [ ] Scheduled scan (daily) with diff of new registrations goes to the queue.
- [ ] CT monitoring alerts on certificates with brand strings.
