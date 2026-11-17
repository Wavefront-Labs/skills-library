---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-signaling-zone
name: dnssec-signaling-zone
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, rfc9615, signaling-zone, bootstrapping, cds, set-signaling]
level: advanced
status: docs-checked
description: "Set up authenticated DNSSEC bootstrapping (RFC 9615) in PowerDNS: _signal zones with pdnsutil zone create and set-signaling, delegation and DS, and limits."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/operational.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticated bootstrapping signaling zone

Server-wide: it applies to every zone publishing CDS/CDNSKEY.

Steps, repeated for every NS hostname used by bootstrapped domains:
1. The nameserver hostname (for example `ns1.example.net`) must itself live in a signed zone with a DS in its parent.
2. On the nameserver, or another instance serving the same zones:
```
pdnsutil zone create _signal.$nshost $nshost
pdnsutil zone set-signaling _signal.$nshost
```
The first command also creates the NS record.
3. Delegate `_signal.<nshost>` to the PowerDNS instance and publish a DS for that delegation.

`set-signaling` is shorthand for securing the zone, enabling NSEC3 narrow mode, and setting the `SIGNALING-ZONE` metadata.

Limits: a nameserver cannot bootstrap its own parent zone, so skip the signaling zone if no other zones sit under that hostname.

## Checked

2026-11-04. Read the Authenticated Bootstrapping (RFC 9615) section of dnssec/operational.rst and confirmed server-wide effect, the three steps, the set-signaling equivalence, repeat-per-NS-hostname rule and the own-parent limit. Nothing removed.

Method: documentation only; no commands were run.
