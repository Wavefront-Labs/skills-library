---
id: computing-software.networking-hardware-and-wireless.unbound.aggressive-nsec-caching
name: aggressive-nsec-caching
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, aggressive-nsec, rfc8198, nsec, nxdomain, wildcard]
level: practitioner
status: docs-checked
description: "Use cached DNSSEC NSEC records to synthesise NXDOMAIN, NODATA and wildcard answers in Unbound with aggressive-nsec (RFC 8198)."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/privacy/aggressive-nsec.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aggressive nsec caching
With `aggressive-nsec: yes`, Unbound builds answers from NSEC records already in its validated cache instead of querying the authoritative server (RFC 8198). The unbound.conf manual lists the default as yes.

Answers it can generate:
- NODATA: a cached NSEC shows the name exists but lacks the queried type.
- NXDOMAIN: cached NSEC records show the name falls between two existing names and no wildcard applies.
- Wildcard answers: RRSIG label counts reveal wildcard-expanded records; Unbound stores the wildcard RRset under its original owner name, so later queries for other names the wildcard covers are answered without upstream queries.

Limits: it works from NSEC records that are DNSSEC-validated and already cached, so it helps most for names whose proofs were cached earlier. The page says it can cut traffic at every level of the hierarchy, most noticeably at the root, where more than half of responses are NXDOMAIN.

Counters `num.query.aggressive.NOERROR` (NODATA answers from cached NSEC) and `num.query.aggressive.NXDOMAIN` appear under Extended Statistics in the unbound-control manual.

## Checked
Method: 2026-11-08 read the aggressive-nsec topic page and the unbound.conf and unbound-control manuals. Rewrote the wildcard and limits wording to match the pages and dropped the "only signed zones" claim; the default of yes and counter names are confirmed.
