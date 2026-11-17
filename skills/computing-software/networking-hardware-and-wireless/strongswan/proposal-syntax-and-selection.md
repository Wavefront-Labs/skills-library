---
id: computing-software.networking-hardware-and-wireless.strongswan.proposal-syntax-and-selection
name: proposal-syntax-and-selection
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, proposals, cipher-suites, prefer-configured-proposals, esp-proposals]
level: practitioner
status: docs-checked
description: "Write strongSwan IKE and ESP/AH proposal strings, understand ordering and AEAD separation, and how charon.prefer_configured_proposals changes proposal selection."
sources:
  - https://docs.strongswan.org/docs/latest/config/proposals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proposal syntax and selection
A proposal is a list of algorithm keywords separated by dashes, used in `proposals` and `ah_proposals`/`esp_proposals`. With IKEv2 several algorithms of one kind may be listed and their order sets preference; IKEv1 allows one per kind and strips the rest (use several proposals instead). The order of algorithms of different kinds does not matter.

```
aes256gcm16-aes192gcm16-prfsha384-prfsha256-ecp384-modp3072
```

Here `aes256gcm16` is preferred over `aes192gcm16`, `prfsha384` over `prfsha256`, `ecp384` over `modp3072`.

Multiple proposals are comma-separated in swanctl.conf, ordered by preference. This is needed to accept both AEAD and classic encryption plus integrity algorithms, which must not share a proposal.

**Selection as responder.** By default strongSwan prefers its own configuration: the first configured proposal, and within it the first algorithm of each kind, that the received proposals accept. If the initiator's first key exchange differs from the selected one, the result is an INVALID_KE_PAYLOAD error and an extra round trip. Disable `charon.prefer_configured_proposals` in strongswan.conf to pick the first received proposal (and its first acceptable algorithm per kind) instead; the selected key exchange then likely matches the received KE payload.

The special value `default` adds a safe default proposal. Check available keywords with `swanctl --list-algs`.

## Checked
2026-11-04. Confirmed against the strongSwan Algorithm Proposals page (format, ordering, AEAD separation, selection as responder, charon.prefer_configured_proposals, INVALID_KE_PAYLOAD) and the swanctl --list-algs page. Nothing removed.

Method: documentation only; no commands were run.
