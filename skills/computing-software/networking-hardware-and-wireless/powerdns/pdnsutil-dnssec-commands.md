---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-dnssec-commands
name: pdnsutil-dnssec-commands
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, dnssec, secure, rectify, set-presigned, publish-cds, algorithms]
level: practitioner
status: docs-checked
description: "pdnsutil DNSSEC zone commands: secure, rectify, set-nsec3 defaults, set-presigned, publish CDS/CDNSKEY, export-ds, dnssec-disable and list-keys."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil DNSSEC commands

Algorithms: rsasha1, rsasha1-nsec3-sha1, rsasha256, rsasha512, ecdsa256, ecdsa384, ed25519, ed448 (the last two need suitable crypto libraries at compile time). `pdnsutil list-algorithms [with-backend]` lists what the build supports.

- `zone secure ZONE [ZONE]...`: default DNSSEC settings, then rectify. `zone secure-all [increase-serial]` secures every unsigned zone; follow with `zone rectify-all`.
- `zone rectify ZONE` / `zone rectify-all`: recalculate ordername and auth.
- `zone show ZONE`: details including DNSSEC settings. `zone list-keys [ZONE]` (`-v` includes disabled or empty zones).
- `zone export-ds ZONE`: DS for all KSKs. `zone export-dnskey ZONE KEY_ID`: DNSKEY and DS for one key.
- `zone set-nsec3 ZONE ['HASH-ALG FLAGS ITERATIONS SALT'] [narrow]`: hash algorithm must be 1; flag 1 is opt-out; salt is hex or `-`. Default parameters are `'1 0 0 -'` (RFC 9276). `narrow` sends white lies (RFC 7129) and denies zone transfers. `zone unset-nsec3 ZONE` returns to NSEC.
- `zone set-presigned ZONE` / `zone unset-presigned ZONE`: use in-zone RRSIGs.
- `zone set-publish-cds ZONE [DIGESTALGOS]`: comma-separated list, default `2` (SHA-256); `0` publishes the delete algorithm. `zone set-publish-cdnskey ZONE [delete]`. Matching `unset-` commands stop publication.
- `zone dnssec-disable ZONE`: deactivates all keys and unsets PRESIGNED.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst.

Method: documentation only; no commands were run.
