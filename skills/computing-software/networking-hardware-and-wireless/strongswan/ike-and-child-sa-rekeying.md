---
id: computing-software.networking-hardware-and-wireless.strongswan.ike-and-child-sa-rekeying
name: ike-and-child-sa-rekeying
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, rekeying, reauthentication, rekey-time, make-before-break, lifetimes]
level: practitioner
status: docs-checked
description: "Tune strongSwan IKE and CHILD_SA renewal: rekey versus reauth, make_before_break, rekey_time, over_time, rand_time and time, byte and packet lifetimes, AUTH_LIFETIME behaviour."
sources:
  - https://docs.strongswan.org/docs/latest/config/rekeying.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ike and child sa rekeying
**Rekeying** replaces keys inline via CREATE_CHILD_SA without interrupting IKEv2 IKE or IPsec SAs; it is the default for swanctl.conf. **Reauthentication** builds a new IKE SA and all CHILD SAs from scratch and re-checks credentials (certificate expiry and CRL/OCSP revocation are only checked during authentication). IKEv1 supports only reauthentication.

Reauth is make-before-break by default (overlapping SAs created before old ones are deleted; both peers must tolerate overlap, e.g. virtual IPs, duplicate policies, updown scripts). Disable with `charon.make_before_break = no` for break-before-make; use firewall or drop policies so plaintext does not leak during the gap.

Responders with reauth configured send the AUTH_LIFETIME notify (RFC 4478). As a client, strongSwan honours it even when reauth is disabled, subtracting `over_time` from the lifetime.

Connection settings: `reauth_time` (default `0s`, off), `rekey_time` (default `4h`; becomes zero if `reauth_time` is set, so set it explicitly for both), `over_time` (default 0.1 x max of rekey and reauth time), `rand_time` (default `over_time`).

CHILD_SA: `rekey_time` (default 1h, or `life_time` / 1.1), `life_time` (1.1 x `rekey_time`), `rand_time`; the same triplets exist for `_bytes` and `_packets`, volume-based rekeying being off by default.

## Checked
2026-11-04. Confirmed against the IKE and IPsec SA Renewal page: rekey versus reauth, make_before_break, AUTH_LIFETIME behaviour, and all IKE and CHILD_SA defaults.

Method: documentation only; no commands were run.
