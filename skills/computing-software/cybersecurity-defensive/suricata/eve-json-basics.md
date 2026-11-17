---
id: computing-software.cybersecurity-defensive.suricata.eve-json-basics
name: eve-json-basics
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [eve-json, eve-log, json-logging, eve-filetype]
level: intro
status: docs-checked
description: "Configure EVE JSON logging: the eve-log core settings, filetype options (regular, syslog, unix, redis), buffering, heartbeat, rotation and multiple instances."
sources: ["https://docs.suricata.io/en/latest/output/eve/eve-json-output.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EVE JSON basics

EVE writes alerts, anomalies, metadata, file info and protocol records as JSON, default file `eve.json`.

Core: `enabled`, `filetype`, `filename`, `threaded` (file per thread, such as `eve.9.json`), `buffer-size` (0 = unbuffered), `prefix`, `ethernet`, `suricata-version`, `ipv6-compress`, `pcap-file`, `filemode`.

`filetype`: `regular` (default), `syslog` (`identity`, `facility`, `level`), `unix_dgram`, `unix_stream`, `redis` (modes list/lpush, rpush, channel/publish, xadd/stream; also `key`, `stream-maxlen`, `pipelining`).

`heartbeat.output-flush-interval`: 0 or 1 to 60 seconds; matters only with buffering.

Rotation: `rotate-interval` of `minute`, `hour` or `day` (local time aligned), or relative values such as `30m`. Filenames accept strftime modifiers.

Several `eve-log` instances are allowed (only `drop` is limited to one). Standalone JSON loggers are deprecated.

## Checked

2026-11-04. Confirmed against the EVE JSON Output page (core options, filetypes, Redis modes and options, heartbeat, rotation, multiple instances, filemode).

Method: documentation only; no commands were run.
