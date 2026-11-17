---
id: computing-software.systems-network-administration.openldap.size-and-time-limits
name: size-and-time-limits
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, sizelimit, timelimit, soft-hard, olcsizelimit, limits]
level: practitioner
status: docs-checked
description: "Set global OpenLDAP size and time limits: sizelimit and timelimit defaults, soft vs hard, size.unchecked, size.pr, size.prtotal and who is exempt."
sources:
  - https://www.openldap.org/doc/admin26/limits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# size and time limits
Keywords: `sizelimit`, `timelimit` (slapd.conf); `olcSizeLimit`, `olcTimeLimit` (cn=config). Defaults: 500 entries and 3600 seconds.

Forms:
- Simple: one value sets soft and hard (integer or `unlimited`).
- Extended: `size.soft=`, `size.hard=`, `time.soft=`, `time.hard=`.
- Special size limits (unchanged by the simple form):
  - `size.unchecked`: caps candidates examined after index lookups before filter evaluation; default `unlimited`, `disabled` blocks the search. Exceeding it aborts the search. Useful to block unindexed searches.
  - `size.pr`: max page size for paged searches (integer, `noEstimate`, `unlimited`).
  - `size.prtotal`: total entries across a paged search; defaults to `size.hard`; also `unlimited` or `disabled`.

Example:
```
sizelimit size.soft=5 size.hard=100 size.unchecked=100
```
Semantics:
- The soft limit is the default; the hard limit cannot be exceeded by ordinary users. If the client asks for a limit, the lower of request and hard limit applies.
- Violations return `adminLimitExceeded`, usually with partial results.
- The rootdn is never subject to limits.
- A client using the paged results control gets the hard limit applied to the total across pages.

Verify: `ldapsearch -z <n>` (a client-side size limit, ldapsearch(1)) against a larger result set; the server reports adminLimitExceeded once the hard limit is passed.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide Limits chapter: keywords and olc attributes, defaults 500 entries and 3600 seconds, simple and extended forms, size.unchecked, size.pr, size.prtotal, soft and hard semantics, adminLimitExceeded, rootdn exempt, paged results, and the ldapsearch -z option from ldapsearch(1). Removed the exact error text with code (11), which no fetched page states.

Method: documentation only; no commands were run.
