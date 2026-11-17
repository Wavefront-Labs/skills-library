---
id: computing-software.cybersecurity-defensive.suricata.exception-policies
name: exception-policies
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [exception-policy, memcap-policy, midstream-policy, error-policy]
level: advanced
status: docs-checked
description: "Control what Suricata does at memcap hits, midstream pickup and parser errors: exception-policy values, auto behaviour in IDS and IPS, counters."
sources: ["https://docs.suricata.io/en/latest/configuration/exception-policies.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exception policies

Master switch `exception-policy` (sample value `auto`); individual settings override it.

Values: `drop-packet`, `drop-flow`, `reject`, `bypass`, `pass-packet`, `pass-flow`, `ignore` (and `rejectboth`). `auto` exists only at master level: in IPS most policies fail closed (drop flow); in IDS it is effectively disabled.

| Setting | Policy variable |
|---|---|
| stream.memcap, stream.reassembly.memcap, flow.memcap, defrag.memcap | `memcap-policy` |
| stream.midstream | `midstream-policy` |
| app-layer | `error-policy` |

Flow and defrag memcap policies apply to packets only.

Meanings: `drop-flow` stops decoding/parsing and drops the flow; `pass-flow` disables detection but keeps reassembly, parsing and logging; `bypass` stops decoding; `ignore` applies nothing.

Packet-level drops can make later packets look midstream. Flow events gain `exception_policy`; counters such as `exception_policy.tcp.midstream` appear only when applied. Invalid combinations stop startup.

## Checked

2026-11-04. Confirmed against the Exception Policies page (master switch, auto, policy variables, values, midstream matrix, interactions, flow event, counters).

Changed: `auto` was called the default; the page shows it only as the sample value.

Method: documentation only; no commands were run.
