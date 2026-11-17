---
id: computing-software.cybersecurity-defensive.suricata.app-layer-parser-settings
name: app-layer-parser-settings
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [app-layer, libhtp, tls-encryption-handling, max-tx]
level: advanced
status: docs-checked
description: "Adjust application-layer parser limits in suricata.yaml: libhtp personalities and body limits, TLS encryption handling, SMB, NFS, FTP, HTTP2, max-tx."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# app-layer settings

- `error-policy` governs parser errors; `asn1-max-frames: 256`.
- libhtp: default personality `IDS`, `request-body-limit` and `response-body-limit` 3072; `server-config` blocks use personalities such as `Apache_2_2` or `IIS_7_0`.
- TLS: `detection-ports: 443`, `encryption-handling` `track-only` (also the behaviour when unset; or `bypass`, `full`).
- SSH: `hassh` yes, auto or no.
- FTP: `memcap: 64 MiB`, `max-line-length: 4kb`, `max-preliminary-responses: 16`.
- SMB: `max-read-size: 8mb`, `max-write-size: 1mb`, read queue limits.
- NFS: read, write and metadata sizes 16mb.
- DCERPC `max-stub-size: 1MiB`; HTTP2 `max-table-size` 4096, `max-streams` 256; MQTT `max-msg-length: 1mb`; Modbus `stream-depth: 0`.
- `max-tx` applies to SMTP, MQTT, FTP, PGSQL, SMB, DCERPC, HTTP1, ENIP and NFS; `max-responses` to LDAP and PGSQL.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page (app-layer protocol sections: libhtp, TLS, SSH, FTP, SMB, NFS, DCERPC, HTTP2, Modbus, MQTT, Maximum transactions, Maximum Responses).

Removed: the `ja3-fingerprints` claim, which that page does not describe.

Method: documentation only; no commands were run.
