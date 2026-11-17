---
id: computing-software.networking-hardware-and-wireless.frrouting.prefix-lists-and-access-lists
name: prefix-lists-and-access-lists
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, prefix-list, access-list, ge-le, sequence-numbers, implicit-deny]
level: practitioner
status: docs-checked
description: "Define FRR IP access lists and prefix lists with seq, ge and le, inspect them with show commands and debug prefix-list, and handle the implicit deny."
sources:
  - https://docs.frrouting.org/en/latest/filter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prefix lists and access lists
Access lists:
- `access-list NAME [seq (1-4294967295)] <permit|deny> <A.B.C.D/M [exact-match]|any>`
- Extended: `access-list NAME [seq N] <deny|permit> ip <source> <destination>`, each as `A.B.C.D A.B.C.D` (wildcard mask), `host A.B.C.D` or `any`. Wildcard masks use inverse logic. Example: `access-list filter seq 10 deny ip 10.0.20.0 0.0.0.255 232.1.1.0 0.0.0.255`.
- Unnumbered entries take the next multiple of 5 after the highest sequence number.
- `show <ip|ipv6> access-list [WORD] [json]`.

Prefix lists:
- `ip prefix-list NAME [seq NUMBER] (permit|deny) PREFIX [le LEN] [ge LEN]`
- Without `le`/`ge` the length must match exactly; `ge` and `le` can be combined in either order.
- Evaluation runs from the lowest sequence and stops at the first match. Reusing a sequence number overwrites it; a different number with identical rules is an error.
- `ip prefix-list NAME description DESC`; `clear ip prefix-list [NAME [A.B.C.D/M]]`.
- `show ip prefix-list [NAME [seq NUM]] [json]`, `show ip prefix-list NAME A.B.C.D/M` with `longer` or `first-match`, `show ip prefix-list summary|detail [NAME]`.
- `debug prefix-list NAME match <A.B.C.D/M|X:X::X:X/M> [address-mode]` shows which entry matched (succeeds only on permit).

Implicit behaviour: an access list with no match is denied. If no prefix list is specified it acts as permit, but a defined prefix list with no matching entry is denied.

## Checked

2026-11-04. Confirmed against the FRR Filtering page: access-list and extended access-list syntax, sequence numbering, prefix-list ge/le rules, overwrite and duplicate-rule behaviour, show, clear and debug commands, default verdicts. Nothing changed.
Method: documentation only; no commands were run.
