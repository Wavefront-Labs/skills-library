---
id: computing-software.systems-network-administration.openldap.overlay-sssvlv
name: overlay-sssvlv
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, sssvlv, server-side-sort, vlv, overlay, paged-results]
level: practitioner
status: docs-checked
description: "Enable server-side sorting and virtual list view in OpenLDAP with the sssvlv overlay: sssvlv-max, sssvlv-maxkeys, sssvlv-maxperconn defaults and memory cost."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-sssvlv&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldapsearch&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sssvlv overlay
```
overlay sssvlv
sssvlv-max 10
sssvlv-maxkeys 5
sssvlv-maxperconn 5
```
Directives (after `overlay sssvlv`):
- `sssvlv-max <num>`: concurrent sort requests across all connections; default half the server threads.
- `sssvlv-maxkeys <num>`: sort keys per request; default 5.
- `sssvlv-maxperconn <num>`: concurrent paged searches per connection; default 5, still capped by `sssvlv-max`.

The overlay works with any backend or globally, and replaces the default PagedResults (RFC 2696) control so paging works with sorting.

Client testing with ldapsearch:
- Server-side sort: `ldapsearch -E 'sss=cn' ...`
- Virtual list view: `-E 'vlv=<before>/<after>(/<offset>/<count>|:<value>)'`.

Gotcha: sorting builds the full result set in memory before sorting, so large sorts can raise memory use sharply. Keep `sssvlv-max` low.

Verify: a sorted search with `-E 'sss=cn'` returns entries ordered by cn.

## Checked

2026-11-04. Confirmed against slapo-sssvlv(5) (RFC 2891 sorting, VLV, replacing the RFC 2696 PagedResults control, any backend or global, the three directives and their defaults, complete result set built in memory) and the ldapsearch(1) -E sss= and vlv= extension syntax. Removed the claim that vlv must be used together with sss and the advice to index filter attributes, neither stated on those pages.

Method: documentation only; no commands were run.
