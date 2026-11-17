---
id: computing-software.cybersecurity-defensive.suricata.migrating-snort-rules
name: migrating-snort-rules
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [snort-migration, snort-differences, urilen-ranges, alert-limit]
level: practitioner
status: docs-checked
description: "Convert Snort rules to Suricata: port-independent protocol detection, urilen ranges, header buffers, fast pattern, flowbits and alert-limit differences."
sources: ["https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snort versus Suricata

- Protocols are detected regardless of port: use `alert http ... any` or add `app-layer-protocol:<proto>;` to a `tcp` rule.
- `urilen` ranges are exclusive (`2<>10` is 3 to 9); default normalized, add `,raw`.
- No `http_raw_cookie`; use `http_raw_header`.
- New buffers: `http_user_agent`, `http_host`, `http_content_type`, `http_server_body`, `http_raw_host`.
- `rawbytes` is accepted but does nothing.
- `fast_pattern:only` is silently ignored. Fast pattern is case sensitive unless `nocase`, and any `http_*` buffer qualifies.
- Packet keywords (`dsize`, `flags`, `ttl`) and stream keywords (`http_*`) cannot mix; use `tcp-pkt` or `tcp-stream`, and `stream_size`.
- `noalert;` works alone.
- Hard-coded limit of 15 alerts per packet or stream.
- Two alerts for one TCP packet can happen when evaluated alone and in the stream.
- File keywords (`filestore`, `filename`, `fileext`, `filemagic`, `filesize`, `filemd5`, `filesha1`, `filesha256`) cover FTP, HTTP and SMTP.
- The `lua` keyword has no Snort equivalent.

## Checked

2026-11-04. Every point above confirmed against the Differences From Snort page.

Method: documentation only; no commands were run.
