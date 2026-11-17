---
id: computing-software.cybersecurity-defensive.suricata.stream-reassembly-and-memcaps
name: stream-reassembly-and-memcaps
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [stream-memcap, reassembly, midstream, stream-bypass]
level: advanced
status: docs-checked
description: "Size TCP stream tracking and reassembly: memcap, depth, chunk sizes, midstream, checksum validation, inline, bypass and urgent data policy."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html", "https://docs.suricata.io/en/latest/performance/tuning-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# stream and reassembly

Sample defaults in suricata.yaml:
- `stream`: `memcap: 64mb`, `checksum-validation: yes`, `prealloc-sessions: 32768`, `midstream: false`, `async-oneside: false`, `inline: no`, `drop-invalid: yes`, `bypass: no`.
- `reassembly`: `memcap: 256mb`, `depth: 1mb`, `toserver-chunk-size` and `toclient-chunk-size` 2560, `randomize-chunk-size: yes`, `segment-prealloc: 2048`. Raw reassembly (for plain `content` and `pcre` matching) can be turned off with `raw: no`.
- Urgent data `policy: oob` (drop, inline, oob, gap).

Tuning notes:
- `stream.bypass: yes` stops inspecting a flow once reassembly depth is reached.
- `stream.inline: auto` enables inline mode in IPS.
- Memcap hits are governed by `memcap-policy` (see exception policies).

Also see `defrag` (`memcap: 32mb`, `timeout: 60`) and `flow` (`memcap` 32 MiB, `hash-size: 65536`, `prealloc: 10000`, `emergency-recovery: 30`).

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/performance/tuning-considerations.html (read in full) and the Flow and Stream handling, defrag and TCP urgent sections of https://docs.suricata.io/en/latest/configuration/suricata-yaml.html; replaced the unconfirmed raw default with the documented raw: no switch.
