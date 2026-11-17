---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-list-certs-pools-algs
name: swanctl-list-certs-pools-algs
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl, list-certs, list-pools, list-algs, flush-certs]
level: practitioner
status: docs-checked
description: "Use swanctl --list-certs with type and flag filters, --list-pools with leases, --list-algs to see crypto plugins, and --flush-certs to clear the cert cache."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListCerts.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListPools.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlListAlgs.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl list certs pools algs
**Certificates.** `swanctl --list-certs [--subject <dn/san>] [--pem] [--type x509|x509_ac|x509_crl|ocsp_response|pubkey]`. Further options: `--flag`/`-f` (filter by X.509 flag: none, ca, aa, ocsp or any), `--short`/`-S`, `--utc`/`-U`, `--pem`/`-p`. For example, loaded CA certificates:

```
swanctl --list-certs --type x509 --flag ca
```

Output shows subject, issuer, validity, serial, flags, key IDs and the public key.

**Pools.** `swanctl --list-pools [--leases] [--name]` lists configured IPv4 and IPv6 pools with their state, shown as `online / offline / size`; `--leases` (`-l`) adds each lease with the identity and `online` status, and `--name` (`-n`) filters. `--pretty` prints the vici reply.

**Algorithms.** `swanctl --list-algs` lists loaded algorithms by group (encryption and so on) and the plugin that implements each, e.g. `AES_CBC[openssl]`.

**Flush.** `swanctl --flush-certs` (`-f`) flushes cached certificates.

## Checked
2026-11-04. Confirmed against the swanctl --list-certs, --list-pools, --list-algs and swanctl tool pages: options with short forms, type and flag values, the pool lease output and the algorithm listing. Removed the unsupported advice about proposal keywords.

Method: documentation only; no commands were run.
