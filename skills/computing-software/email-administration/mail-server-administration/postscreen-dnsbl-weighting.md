---
id: computing-software.email-administration.mail-server-administration.postscreen-dnsbl-weighting
name: postscreen-dnsbl-weighting
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postscreen-dnsbl-weighting, postscreen-dnsbl-sites, postscreen-dnsbl-threshold]
level: advanced
status: draft
description: "Score DNS blocklists in postscreen with postscreen_dnsbl_sites weights and a reject threshold."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postscreen dnsbl weighting

**Goal:** reject clients when combined blocklist score reaches a threshold.
## Steps
1. `postscreen_dnsbl_sites = zen.example.org*2, dnsbl.example.net*1` (use the real lists you have licence/usage terms for).
2. `postscreen_dnsbl_threshold = 2`; `postscreen_dnsbl_action = enforce`.
3. Add an allow list: `postscreen_dnsbl_allowlist_threshold = -1` with negative-weighted allowlist entries.
4. Consider `postscreen_dnsbl_ttl` to limit repeat lookups.
## Failure modes
- Public resolvers are rate limited or blocked by many DNSBL operators; use your own recursive resolver.
- A threshold of 1 with one list means a single listing blocks mail: tune carefully.
## Verify
- `postscreen: DNSBL rank 3 for [192.0.2.50]` appears in the log for a listed test client.
- Check list policy documents for query-volume terms.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
