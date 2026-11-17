---
id: computing-software.cybersecurity-defensive.suricata.flowint-stream-size-flow-counters
name: flowint-stream-size-flow-counters
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [flowint, stream-size, flow-age, flow-pkts, flow-bytes]
level: advanced
status: docs-checked
description: "Count and size-check flows: flowint math, stream_size, flow.age, flow.pkts, flow.bytes and flow.elephant with their syntax."
sources: ["https://docs.suricata.io/en/latest/rules/flow-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Flow counters and sizes

- `flowint: name, modifier[, value];` integer variables in a flow. Modifiers `+`, `-`, `=`, `>`, `<`, `>=`, `<=`, `==`, `!=`; existence checks `isset`, `notset`, `isnotset`. The value may be an integer or another variable. Combine with `noalert` for counting.
- `stream_size:<server|client|both|either>, <op>, <number>;` bytes registered via sequence numbers, for example `stream_size:both, >, 5000;`.
- `flow.age: [op]<number>` seconds, unsigned 32-bit, checked on every packet. Pair with flowbits to alert once.
- `flow.pkts:<toclient|toserver|either|both>,[op]<number>` (32-bit).
- `flow.bytes:<direction>,[op]<number>` (64-bit).
- `flow.elephant:<direction>`.

Legacy `flow.pkts_toclient` and similar forms still work but the directional syntax is preferred.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/flow-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
