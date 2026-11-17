---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-list-sas-and-conns
name: swanctl-list-sas-and-conns
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl, list-sas, list-conns, list-pols, monitoring]
level: practitioner
status: docs-checked
description: "Inspect strongSwan state with swanctl --list-sas, --list-conns and --list-pols: filters, raw output, and how to read the IKE and CHILD SA display."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListSas.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListConns.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListPols.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl list sas and conns
`swanctl --list-sas` lists established IKE SAs and dependent CHILD SAs. Filters: `--ike`/`-i` (name), `--ike-id`/`-I`, `--child`/`-c`, `--child-id`/`-C` (child filters noted as since 5.9.6). `--noblock`/`-n` does not wait for IKE SAs in use. `--raw`/`-r` dumps the raw response message, `--pretty`/`-P` the same in pretty print.

Example output:

```
home: #1, ESTABLISHED, IKEv2, 6fd55d95f66b4a67_i* cea64d4a303e0ca2_r
  local  'carol@strongswan.org' @ 192.168.0.100[4500]
  remote 'moon.strongswan.org' @ 192.168.0.1[4500]
  AES_CBC-128/HMAC_SHA2_256_128/PRF_HMAC_SHA2_256/CURVE_25519
  established 1s ago, rekeying in 14043s
  net: #1, reqid 1, INSTALLED, TUNNEL, ESP:AES_GCM_16-128
    installed 1s ago, rekeying in 3397s, expires in 3959s
```

It also shows SPIs, byte and packet counters per direction, and the local and remote traffic selectors.

`swanctl --list-conns` (`--ike <name>` filters) shows loaded configurations: IKE version, whether reauthentication is on, rekey interval, local and remote addresses, the local and remote authentication with ids and certs, and each child with mode, rekey interval and selectors.

`swanctl --list-pols` lists installed trap, drop and pass policies. Options: `--child`/`-c` (filter by CHILD_SA config name), `--trap`/`-t`, `--drop`/`-d`, `--pass`/`-p`, plus `--raw` and `--pretty`.

## Checked
2026-11-04. Confirmed against the swanctl --list-sas, --list-conns and --list-pols pages: options and short forms, the since-5.9.6 note on child filters, and the example output. Removed the unsupported pointer to `--help`; the list-pols description now matches the page (trap, drop and pass policies).

Method: documentation only; no commands were run.
