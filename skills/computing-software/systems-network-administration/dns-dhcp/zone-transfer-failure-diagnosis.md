---
id: computing-software.systems-network-administration.dns-dhcp.zone-transfer-failure-diagnosis
name: zone-transfer-failure-diagnosis
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [bind, zone-transfer, transfer-failure, zone-transfer-troubleshooting, axfr, ixfr, tsig, refused, expired-zone]
level: practitioner
status: docs-checked
description: "Diagnose secondaries that stop updating: test AXFR/IXFR with dig, read xfer-in logs, fix REFUSED, NOTAUTH/TSIG and serial problems, and catch zones about to expire."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://www.rfc-editor.org/rfc/rfc5936
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zone transfer failure diagnosis

## Symptom check
Compare SOA serials on all authoritative servers:
```
for ns in $(dig +short NS example.net); do echo "$ns"; dig +short SOA example.net @$ns; done   # third field of the SOA is the serial
```
A secondary stuck on an old serial is not transferring.

## Test the transfer manually (from the secondary's IP)
```
dig @primary.example.net example.net AXFR                       # without TSIG
dig @primary.example.net example.net AXFR -y hmac-sha256:xfr-key:BASE64SECRET=
dig @primary.example.net example.net IXFR=2026101701 -k /etc/bind/xfr.key
```

## Read the logs on both sides
Secondary (`xfer-in` category), primary (`xfer-out` and `security`):
Look for the transfer result and the rcode (for example REFUSED) in the `xfer-in` log, and for a denied transfer on the primary.

## Causes and fixes
| Error | Cause |
|---|---|
| REFUSED / "zone transfer denied" | primary's `allow-transfer` does not include the secondary IP or key; the secondary uses a different source IP (multi-homed, NAT). Set `transfer-source` on the secondary or fix the ACL |
| NOTAUTH / TSIG errors (BADSIG, BADTIME) | key name, algorithm or secret differs; clock skew between servers can break TSIG verification |
| SOA answer lacks the aa flag or is not authoritative | zone not loaded on the primary (syntax error after an edit): check `named-checkzone` and primary logs |
| Timeouts | TCP 53 blocked between servers (AXFR/IXFR use TCP) |
| Serial lower on primary | serial went backwards (manual edit, restore); a secondary only transfers when it sees a larger serial, so correct the serial and use `rndc retransfer` on each secondary |
| IXFR fails then AXFR succeeds | incremental data unavailable; harmless if the AXFR completes |

## Force and watch
```
rndc retransfer example.net        # on the secondary
rndc zonestatus example.net        # serial, next refresh, expires
```

## Expiry and primary selection
If a secondary cannot refresh for longer than the SOA `expire` time it stops serving the zone. `rndc zonestatus` shows the scheduled refresh and expiry times. A secondary tries its primaries in turn and caches an unreachable primary for 10 minutes (or until a NOTIFY from it arrives), so a recently failed primary may be skipped; `rndc refresh` or `rndc retransfer` forces another attempt.

## Verify
- [ ] All authoritative servers report the same serial within minutes of a change.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed: primaries tried in turn, 10-minute unreachable cache, refresh on restart or rndc refresh, rndc retransfer and zonestatus descriptions (rndc man page), dig -y/-k/-t options, xfer-in/xfer-out/security logging categories. Removed unconfirmed log lines, the 5-minute TSIG skew figure, 2^31 serial advice and typical expire durations.

Method: documentation only; no commands were run.
