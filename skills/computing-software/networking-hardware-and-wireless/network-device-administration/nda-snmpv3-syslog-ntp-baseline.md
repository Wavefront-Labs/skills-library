---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-snmpv3-syslog-ntp-baseline
name: nda-snmpv3-syslog-ntp-baseline
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [snmpv3-baseline, device-syslog-config, ntp-sync-devices, nda-monitoring]
level: practitioner
status: gated
description: "Configure SNMPv3 authPriv, syslog to a collector with severity and timestamps, and NTP so logs correlate."
sources:
  - https://www.rfc-editor.org/rfc/rfc5424
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring baseline

- Syslog messages follow the RFC 5424 format (header with VERSION and TIMESTAMP, structured data including a `sequenceId` parameter). Transport mappings are separate documents; UDP is described in RFC 5426.
- SNMPv3 with authPriv (SHA/AES) per user; disable v1/v2c community strings or restrict them by ACL. (gated: unconfirmed, source is paywalled or blocked)
- NTP: at least two or three sources, authentication where supported. (gated: unconfirmed, source is paywalled or blocked)
- Poll interface counters, CPU, memory, temperature and neighbour state; set thresholds by baseline rather than defaults.

## Verify
- [ ] A test change appears in the syslog server with a correct timestamp and SNMP polls succeed with v3 credentials.
## Checked
2026-11-02. Confirmed against RFC 5424 (message format, TIMESTAMP, sequenceId; UDP transport via RFC 5426). Gated: SNMPv3 and NTP guidance (RFC 3414/5905 not read). Removed: TLS syslog and severity claims (RFC 5425 not read).
Method: documentation only; no commands were run.
