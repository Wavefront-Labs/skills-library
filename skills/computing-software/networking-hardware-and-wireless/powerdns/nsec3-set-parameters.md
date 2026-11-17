---
id: computing-software.networking-hardware-and-wireless.powerdns.nsec3-set-parameters
name: nsec3-set-parameters
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, nsec3, nsec, pdnsutil, set-nsec3, opt-out, narrow, max-nsec3-iterations]
level: practitioner
status: docs-checked
description: "Switch a PowerDNS zone between NSEC and NSEC3 with pdnsutil set-nsec3: parameter fields, narrow mode, opt-out, algorithm 5/6/7 limit."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/operational.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NSEC3 parameters

NSEC is the default. Enable NSEC3:
```
pdnsutil zone set-nsec3 example.net '1 0 0 -'
pdnsutil zone set-nsec3 example.net '1 0 0 -' narrow
pdnsutil zone unset-nsec3 example.net
```
(`set-nsec3` / `unset-nsec3` without `zone` before 5.0.)

Parameter fields, in order:
1. Hash algorithm: `1` (SHA-1).
2. Flags: `0` recommended; `1` turns on opt-out (RFC 5155 section 6).
3. Iterations: see RFC 5155 section 10.3; capped by `max-nsec3-iterations`.
4. Salt: hex, or `-` for none.

Modes:
- Inclusive (default NSEC3): the backend supplies previous and next hashed names.
- Narrow (RFC 7129 white lies): responses are computed on the fly, preventing zone enumeration. It needs online signing on all nameservers and denies incoming AXFR for those zones.

Do not switch between NSEC and NSEC3 for zones using algorithm 5 (RSASHA1), 6 (DSA-NSEC3-SHA1) or 7 (RSASHA1-NSEC3-SHA1).

## Checked

2026-11-08. Read in full: PowerDNS docs dnssec/operational.rst and dnssec/modes-of-operation.rst. Confirmed NSEC as default, the set-nsec3 and unset-nsec3 syntax and pre-5.0 names, the four NSEC3PARAM fields, the max-nsec3-iterations limit, inclusive and narrow mode behaviour, and the algorithm 5, 6 and 7 warning. Nothing removed.

Method: documentation only; no commands were run.
