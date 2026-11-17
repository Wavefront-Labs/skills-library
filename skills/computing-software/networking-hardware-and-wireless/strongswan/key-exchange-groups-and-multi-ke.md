---
id: computing-software.networking-hardware-and-wireless.strongswan.key-exchange-groups-and-multi-ke
name: key-exchange-groups-and-multi-ke
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, key-exchange, dh-groups, multiple-key-exchanges, post-quantum, ml-kem]
level: advanced
status: docs-checked
description: "Choose strongSwan key exchange keywords (modp, ecp, curve25519) and chain additional or post-quantum key exchanges with the keX_ prefix per RFC 9370."
sources:
  - https://docs.strongswan.org/docs/latest/config/proposals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# key exchange groups and multi ke
In IKE proposals the key exchange method is mandatory. In ESP/AH proposals it is optional: if omitted, CHILD_SA keys derive from the IKE SA key material; if present, it applies to rekeying and CREATE_CHILD_SA exchanges. Adding `none` makes a key exchange optional, which helps when peers differ.

Keyword families:
- Modular prime: `modp768`, `modp1024`, `modp1536` (all three deprecated), `modp2048`, `modp3072` and larger (the table lists the gmp plugin)
- NIST curves: `ecp192` (deprecated), `ecp224`, `ecp256`, `ecp384`, `ecp521`
- Brainpool: `ecp224bp`, `ecp256bp`, `ecp384bp`, `ecp512bp`
- Modern curves: `curve25519` or `x25519`, `curve448` or `x448`
- Post-quantum methods have their own table (e.g. ML-KEM)

**Multiple key exchanges (RFC 9370).** With peers that support them, up to seven additional exchanges can be negotiated by prefixing the keyword with `keX_` where X is 1 to 7, for eight in total per SA. Example from the page: `x25519-ke1_mlkem768` adds ML-KEM-768 after X25519, and this works with any classic or post-quantum method. Make a round optional by adding `keX_none`; gaps are fine, e.g. `x25519-ke7_mlkem768`. Peers must agree on the chosen methods like any other algorithm.

## Checked
2026-11-04. Confirmed against the strongSwan Algorithm Proposals page: key exchange keyword tables and deprecation letters, optional none, keX_ prefix (X 1 to 7, eight in total), x25519-ke1_mlkem768 and x25519-ke7_mlkem768 examples. Clarified that modp768 and modp1024 are deprecated as well.

Method: documentation only; no commands were run.
