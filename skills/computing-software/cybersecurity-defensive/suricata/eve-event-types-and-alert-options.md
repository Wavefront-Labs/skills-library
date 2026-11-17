---
id: computing-software.cybersecurity-defensive.suricata.eve-event-types-and-alert-options
name: eve-event-types-and-alert-options
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [eve-types, eve-alert, payload-logging, eve-dns-tls-http]
level: practitioner
status: docs-checked
description: "Choose EVE event types and alert detail: payload, packet, metadata, verdict, tx guessing, and per-protocol options for http, dns, tls and mqtt."
sources: ["https://docs.suricata.io/en/latest/output/eve/eve-json-output.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Event types and alert options

Enabled by default include alert, anomaly, http, dns, tls, files, smtp, ftp, ssh, flow, stats and many more. Off by default: `frame` (very verbose), `arp`, `ntp`, `netflow`, `pgsql`, `drop` (opt-in).

## Alert options
- Payload: `payload`, `payload-buffer-size`, `payload-printable`, `payload-length`.
- `packet`: packet dump without stream segments.
- `http-body`, `websocket-payload` need metadata.
- `metadata`: `app-layer`, `flow`, `rule` details.
- `tagged-packets`, `verdict` (final engine action), `guess-applayer-tx` (marked `tx_guessed: true`).

## Protocols
- HTTP: `extended`, `custom`, `dump-all-headers`.
- DNS version 2 is the default; version 1 removed in 7.0.
- TLS: one record per session; `custom` disables `extended`.
- MQTT: `passwords` enables output of passwords; `string-log-limit` limits logged string size (default 1KB, 0 disables limiting).
- Stats: `null-values: false` omits zero counters.

## Checked

2026-11-04. Confirmed against the EVE JSON Output page and the suricata.yaml sample (event types and their enabled state, alert options, http, dns, tls, mqtt, stats).

Changed: the MQTT line claimed passwords are cleartext unless limited by `string-log-limit`; the page describes `passwords` as an output toggle and `string-log-limit` as a size limit.

Method: documentation only; no commands were run.
