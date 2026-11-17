---
id: computing-software.cybersecurity-defensive.suricata.app-layer-protocol-keywords
name: app-layer-protocol-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [app-layer-protocol, app-layer-event, app-layer-state, protocol-detection]
level: practitioner
status: docs-checked
description: "Match on detected protocol, events and parser state with app-layer-protocol, app-layer-event and app-layer-state."
sources: ["https://docs.suricata.io/en/latest/rules/app-layer.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# app-layer-* keywords

## app-layer-protocol
`app-layer-protocol:[!]<protocol>[,<qualifier>]...;` Modes: `direction` (default), `to_server`, `to_client`, `either`, `final`, `original`; plus optional `exact`. `failed` and `unknown` are special values. `http` also matches `http1` and `http2` unless `exact` is used. Pipe lists OR values; `!tls|http` is a NOR that skips the detection window.

Example: `alert tcp any any -> any 80 (msg:"non-HTTP traffic over HTTP standard port"; flow:to_server; app-layer-protocol:!http,final; sid:1;)`

Suricata detects protocols regardless of port, so you can use `any` instead of `$HTTP_PORTS`.

## app-layer-event
`app-layer-event:<event name>;` for example `applayer_mismatch_protocol_both_directions`, `applayer_wrong_direction_first_data`, `applayer_detect_protocol_only_one_direction`, `applayer_proto_detection_skipped`, `http.gzip_decompression_failed`.

## app-layer-state
`app-layer-state:[<>]<state>;` for example `request_headers`. Not usable with `http2` or `doh2`.

## Checked

2026-11-04. Confirmed against the Generic App Layer Keywords page (syntax, modes, exact, multi-value and NOR forms, example rule, events, app-layer-state) and Differences From Snort (any instead of port variables).

Method: documentation only; no commands were run.
