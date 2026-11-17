---
id: computing-software.cybersecurity-defensive.suricata.decoder-and-tunnel-settings
name: decoder-and-tunnel-settings
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [teredo, vxlan, decoder-recursion, flow-timeouts]
level: advanced
status: docs-checked
description: "Configure tunnel decoders and flow state timers: Teredo, VXLAN strict checks, recursion-level tracking and flow-timeouts."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Decoder and flow-timeouts

## Decoder
- Teredo: enabled by default; `ports` takes up to four; unset or `any` inspects all UDP.
- VXLAN: enabled, port 4789; `reserved-bits-check` is `strict` (RFC 7348, default) or `permissive`.
- Recursion level: `use-for-tracking: true` associates flows only when encapsulation depth matches.

## flow-timeouts (seconds)
- default: new 30, established 300, emergency-new 10, emergency-established 100.
- tcp: new 60, established 3600, closed 120, emergency-new 10, emergency-established 300, emergency-closed 20.
- udp and icmp: new 30, established 300, emergency-new 10, emergency-established 100.

`flow` has `rate-tracking` (disabled by default). Emergency values apply when `flow.memcap` is under pressure and `emergency-recovery: 30` percent governs recovery.

## Security
`security.limit-noproc` blocks process creation via RLIMIT_NPROC and has no effect as root.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page: Teredo, VXLAN and recursion-level sections, Flow and Flow Time-Outs (all timeout values, emergency-recovery 30, rate-tracking), Configuration hardening.

Method: documentation only; no commands were run.
