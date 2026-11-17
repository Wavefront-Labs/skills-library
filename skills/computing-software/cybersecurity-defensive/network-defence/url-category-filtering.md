---
id: computing-software.cybersecurity-defensive.network-defence.url-category-filtering
name: url-category-filtering
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [web-filtering, url-filtering, url-categories, newly-registered-domains, acceptable-use-policy, category-overrides, uncategorised-sites]
level: practitioner
status: draft
description: "Design URL category policy: block, warn and allow lists tied to acceptable use, newly registered domain handling, overrides workflow and recategorisation requests."
sources: ["CIS Control 9.3 (maintain and enforce network-based URL filters)", "CompTIA Security+ SY0-701 objective 4.5 (URL scanning, content categorization, block rules, reputation)", "Palo Alto Networks URL Filtering best practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# URL category filtering

**Goal:** block web destinations that carry the most risk while users can still work, with a
quick path to fix miscategorisations.

## Policy tiers
| Action | Categories (typical) |
|---|---|
| Block | Malware, phishing, command-and-control, grayware, cryptomining, proxy avoidance/anonymisers, parked domains, dynamic DNS (consider), adult/illegal per AUP |
| Block or warn | Newly registered domains (first 30 days), uncategorised, insufficient content, high-risk file sharing, personal VPNs |
| Warn (continue page) | Gambling, games, streaming where AUP allows with justification |
| Allow and log | Everything else |
Use group-based policies: developers may need paste sites and code hosting; finance does not.

## Newly registered and newly observed domains
Phishing and malware domains are mostly days old. Blocking NRDs (often 30 days) cuts risk a
lot; expect some business false positives (new vendor sites) and provide a fast unblock.

## Override and recategorisation workflow
- Block page shows category and a link to request access (ticket with URL and justification).
- Security reviews: is it malicious (check reputation, sandbox), miscategorised (submit to vendor), or legitimate business (add to allow list with expiry).
- Target response within one business day.

## Integrate intelligence
Custom block lists from threat intel (domains/URLs from incidents and feeds), with expiry.

## Gotchas
- Allow-listing a whole domain like `*.googleusercontent.com` or `*.amazonaws.com` lets attacker-hosted content through; allow specific hosts.
- Category databases differ between vendors; migrating vendors changes what is blocked.
- Without TLS inspection, filtering works on SNI/hostname only (no URL paths).

## Verify
- [ ] Test domains for each blocked category return the block page.
- [ ] Monthly review of overrides and allow list entries; expired entries removed.
