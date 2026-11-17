---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-key-commands
name: pdnsutil-key-commands
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, dnssec-keys, add-key, import-key, export-key, generate-key, key-size]
level: practitioner
status: docs-checked
description: "pdnsutil DNSSEC key commands: add-key defaults, activate, deactivate, publish, unpublish, remove, generate-key, import and export."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/kskrollcdnskey.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil key commands

- `zone add-key ZONE [KSK|ZSK] [active|inactive] [published|unpublished] ALGORITHM [KEYBITS]`: defaults are KSK, inactive, published. Prints the key ID. `KEYBITS` defaults to `default-ksk-size` or `default-zsk-size`.
- `zone activate-key ZONE KEY_ID`, `zone deactivate-key ZONE KEY_ID`: control signing.
- `zone publish-key ZONE KEY_ID`, `zone unpublish-key ZONE KEY_ID`: control DNSKEY presence.
- `zone remove-key ZONE KEY_ID`.
- `zone generate-key KSK|ZSK [ALGORITHM] [KEYBITS]`: generates and prints a key; default algorithm `ecdsa256`.
- `zone import-key ZONE FILE [KSK|ZSK] [active|inactive] [published|unpublished]`: BIND/NSD/LDNS private key format; defaults are KSK, active, published.
- `zone import-key-pem ZONE FILE ALGORITHM {KSK|ZSK}`: PEM private key.
- `zone export-key ZONE KEY_ID`: full private key in BIND/NSD/LDNS format. `zone export-key-pem ZONE KEY_ID`: PEM.

Note the contrast: `add-key` creates inactive by default, `import-key` creates active. Combine `active`/`inactive` with `published`/`unpublished` to stage rollovers (see the rollover skills).

Exported private keys must be handled as secrets. Before 5.0 these were named `add-zone-key`, `activate-zone-key`, `deactivate-zone-key` and `remove-zone-key`.

## Checked

2026-11-08. Read docs/manpages/pdnsutil.1.rst in full and docs/guides/kskrollcdnskey.rst in full. Confirmed the zone key command forms, add-key defaults (KSK, inactive, published), KEYBITS defaults, generate-key default ecdsa256, import-key defaults (KSK, active, published), PEM variants and export commands; the pre-5.0 names add-zone-key, activate-zone-key, deactivate-zone-key and remove-zone-key are confirmed by the KSK rollover guide. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
