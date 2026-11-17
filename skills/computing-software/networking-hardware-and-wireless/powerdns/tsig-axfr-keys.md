---
id: computing-software.networking-hardware-and-wireless.powerdns.tsig-axfr-keys
name: tsig-axfr-keys
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, tsig, axfr, tsig-allow-axfr, axfr-master-tsig, pdnsutil, tsigkey]
level: practitioner
status: docs-checked
description: "Provision TSIG keys for PowerDNS AXFR: pdnsutil tsigkey import and activate, TSIG-ALLOW-AXFR, AXFR-MASTER-TSIG, algorithms."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/tsig.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSIG keys for AXFR

Metadata kinds: `TSIG-ALLOW-AXFR` (primary: key allowed to AXFR the zone) and `AXFR-MASTER-TSIG` (secondary: key used to sign requests to primaries). Content is the key name.

Provision with pdnsutil (5.0+):
```
pdnsutil tsigkey import <keyname> <algorithm> '<base64-secret>'
pdnsutil tsigkey activate <zone> <keyname> primary
pdnsutil tsigkey activate <zone> <keyname> secondary
```
Before 5.0 the commands are `import-tsig-key` and `activate-tsig-key <zone> <keyname> primary|secondary`. On generic SQL backends the same can be done by inserting into `tsigkeys` (name, algorithm, secret) and `domainmetadata` (domain_id, kind, content).

Algorithms: `hmac-md5` (typical), `hmac-sha1`, `hmac-sha224`, `hmac-sha256`, `hmac-sha384`, `hmac-sha512`.

Test the primary:
```
dig -t axfr <zone> @<server> -y '<keyname>:<base64-secret>'
```

The key itself must be provisioned (imported) before the metadata can use it, on the server that uses it.

Caveats:
- Most backends need DNSSEC support turned on for TSIG; with generic SQL use the DNSSEC schema and the matching flag (such as `gmysql-dnssec`).
- A validly TSIG-signed request gets AXFR even when the client IP is not in `allow-axfr-ips`, so any holder of the key can transfer.
- The page notes that the equivalent BIND `server` statement signs all communication with the primary, not just AXFR requests.

## Checked

2026-11-08. Read in full: PowerDNS docs tsig.rst (the GSS-TSIG section is not covered by this skill). Confirmed both metadata kinds, the pdnsutil commands and their pre-5.0 names, the algorithm list, the dig test, the DNSSEC-support note for backends, the allow-axfr-ips warning and the BIND comparison. Removed the unsupported ordering advice.

Method: documentation only; no commands were run.
