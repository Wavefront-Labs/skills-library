---
id: computing-software.systems-network-administration.network-design.punch-down-and-rj45-termination
name: punch-down-and-rj45-termination
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-physical, punchdown, rj45-termination, t568a-t568b, keystone, 110-block]
level: practitioner
status: gated
description: "Terminate copper correctly: T568A/B pinouts, punch-down on 110/Krone/keystone, RJ45 plugs, untwist limits, shielded terminations, and verifying with a tester."
sources:
  - https://tiaonline.org/products-and-services/standards/
  - https://www.fluke.com/en-us/learn/blog/network-testing/t568a-vs-t568b
  - https://www.flukenetworks.com/knowledge-base/applications-standards-articles-copper/what-maximum-untwist-allowed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Punch-down and RJ45 termination

## Pinouts (TIA-568) (gated: unconfirmed, source is paywalled or blocked)
| Pin | T568A | T568B |
|---|---|---|
| 1 | white/green | white/orange |
| 2 | green | orange |
| 3 | white/orange | white/green |
| 4 | blue | blue |
| 5 | white/blue | white/blue |
| 6 | orange | green |
| 7 | white/brown | white/brown |
| 8 | brown | brown |
Use one scheme everywhere on a site (both ends the same = straight-through). Pairs: 1-2, 3-6, 4-5, 7-8.

## Punch-down (110, Krone LSA, keystone jacks)
- Follow the jack's colour label for the chosen scheme.
- Keep jacket up to the termination; **untwist no more than the limit in your cabling specification**.
- 110 tool with the cutting blade facing the waste side; seat each conductor fully; Krone tools for
  LSA blocks are not interchangeable with 110 blades.
- Shielded (F/UTP, S/FTP): bond the foil/drain to the jack shield 360 degrees; ground the panel.

## RJ45 plugs (patch leads and field terminations)
- Use plugs matching conductor type (solid vs stranded) and gauge; pass-through plugs are easy but trim flush.
- Crimp with the jacket inside the plug strain relief.
- Field-terminated plugs on horizontal cabling are permitted for devices like cameras and APs (the TIA
  "MPTL" arrangement); test as MPTL (gated: unconfirmed, source is paywalled or blocked).

## Faults from bad termination
Split pairs (pins 3 and 6 on non-paired wires: passes a continuity tester, fails NEXT), reversed
pairs, opens, shorts, high NEXT from excess untwist, PoE failures from poor contact.

## Verify
- [ ] Wiremap and certification test (from a cable certifier) pass to the cable category for every link; results stored with the link ID.

## Checked

2026-10-28: The Fluke T568A/B page resolved to a blog index and the untwist article returned a stub; TIA-568 is paywalled. The T568A/T568B pin table and the MPTL rule stay but are gated. Removed: the 13 mm (0.5 in) untwist figure and the Cat6A 23 AWG plug remark.
Method: documentation only; no commands were run.
