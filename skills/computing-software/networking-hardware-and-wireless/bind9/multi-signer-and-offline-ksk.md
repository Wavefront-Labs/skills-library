---
id: computing-software.networking-hardware-and-wireless.bind9.multi-signer-and-offline-ksk
name: multi-signer-and-offline-ksk
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, multi-signer, offline-ksk, skr]
level: advanced
status: docs-checked
description: "BIND 9 advanced DNSSEC operation: multi-signer model 2 from RFC 8901, offline-ksk with signed key response files, and manual-mode."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# multi signer and offline ksk
Multi-signer setups follow RFC 8901 Model 2: each provider has its own KSK and ZSK (or CSK) and signs and serves the zone independently; the other provider's keys are imported by dynamic update. Each active KSK needs a DS record in the parent. Signing-state private-type records default to type 65534.

`offline-ksk yes` in a `dnssec-policy` stops BIND signing the DNSKEY, CDS and CDNSKEY RRsets. Signed copies come from Signed Key Response (SKR) files, and existing RRsets in the unsigned zone are replaced. It is a configuration error with a CSK. Import files with `rndc skr -import`; `dnssec-ksr` helps create requests and responses.

`manual-mode yes` stops automatic rollovers: changes are logged and applied only after `rndc dnssec -step`.

## Checked

2026-11-04. Confirmed against the ARM DNSSEC chapter (multi-signer, private type 65534), the `offline-ksk` and `manual-mode` entries, and the rndc man page (`skr -import`, `dnssec -step`). Reworded the multi-signer sentence to match the manual.

Method: documentation only; no commands were run.
