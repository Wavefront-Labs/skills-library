---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-lifetimes-and-t1-t2
name: dhcp6-lifetimes-and-t1-t2
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, preferred-lifetime, valid-lifetime, renew-timer, t1, t2]
level: practitioner
status: docs-checked
description: "Set preferred and valid lifetime triplets and control T1 and T2 values in kea-dhcp6, fixed or calculated, and the T1=T2=0 caveat."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 lifetimes and T1/T2
Lifetimes are triplets: `min-preferred-lifetime` (optional), `preferred-lifetime`, `max-preferred-lifetime` (optional), and the same for valid lifetime. They may be set within client classes. If the client specifies none, the default is used; a specified value outside the min/max bounds is rounded to them. If `preferred-lifetime` is unset, or larger than `valid-lifetime`, the server uses `valid-lifetime` multiplied by 0.625.

T1/T2 fixed: `renew-timer` and `rebind-timer` in seconds. T2 may be any value of zero or more; T1 must be less than T2, otherwise T1 is silently set to zero in the outbound IA.

T1/T2 calculated:
- `calculate-tee-times`: defaults to true (unlike DHCPv4).
- `t1-percent`: percentage of the valid lifetime, default 0.5, must be less than `t2-percent`.
- `t2-percent`: percentage of the valid lifetime, default 0.8, must be greater than `t1-percent`. RFC 9915 recommends 50% and 80% of the preferred lifetime for T1 and T2.

Normal ordering is T1 < T2 < preferred < valid. T1 and T2 both 0 lets clients renew at their discretion, but some broken clients then renew immediately, so test first. Setting them equal to or above the valid lifetime stops renewal and makes clients lose addresses; the docs say to avoid it unless intended.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (DHCPv6 chapter, lifetime and T1/T2 section). Removed: an unclear t2-percent description.
Method: documentation only; no commands were run.
