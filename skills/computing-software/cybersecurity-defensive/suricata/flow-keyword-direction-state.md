---
id: computing-software.cybersecurity-defensive.suricata.flow-keyword-direction-state
name: flow-keyword-direction-state
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [flow-keyword, to-server, established, only-stream]
level: intro
status: docs-checked
description: "Use the flow keyword for direction, connection state and reassembly: to_server, to_client, established, stateless, only_stream, no_frag."
sources: ["https://docs.suricata.io/en/latest/rules/flow-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The flow keyword

**Direction**
- `to_client` = `from_server`
- `to_server` = `from_client`

**State**
- `established`: for TCP after the three-way handshake; for UDP after traffic from both sides.
- `not_established`
- `stateless`: any packet that is part of a flow, regardless of state. Packets not seen as in a flow never match.

**Reassembly**
- `only_stream` / `no_stream`: reassembled by the stream engine or not.
- `only_frag` / `no_frag`: reassembled from fragments or not.

Combine: `flow:to_server, not_established, no_frag`.

`tcp.session` matches `setup`, `established` and `closing` phases (ORed, lowercase, no repeats, never matches non-TCP). It is useful in firewall-mode accept rules.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/flow-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
