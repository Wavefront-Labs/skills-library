---
id: computing-software.cloud-infrastructure-engineering.cilium.ip-options-packet-tracing
name: ip-options-packet-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, ip-options, bpf-monitortraceipoption, hubble, ip-trace-id, nping]
level: advanced
status: docs-checked
description: "Extract IP Option 136 trace IDs with bpf.monitorTraceIPOption in Cilium 1.19+, inject with nping, and filter in Hubble with --ip-trace-id."
sources:
  - https://docs.cilium.io/en/stable/observability/hubble/ip-packet-tracing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IP Options packet tracing

Cilium v1.19 and later can read configured IP Options and show the data in Cilium Monitor and Hubble. Cilium only observes; applications, sidecars or network devices must inject the options.

Enable via Helm: `bpf.monitorTraceIPOption=136` (option 136 is Stream ID), with `hubble.enabled=true`, `hubble.relay.enabled=true`, `hubble.ui.enabled=true`. Restart the agent after setting.

Manual test with nping from a netshoot client to an nginx server pod:
```
kubectl exec deployment/client -- nping --tcp -p 80 --ip-options '\x88\x04\x34\x21' -c 3 ${server_ip}
```
`\x88` is type 136, `\x04` is the length (header plus data), `\x34\x21` is the ID (13345 decimal). Payload length must be exactly 2, 4 or 8 bytes.

Observe: `hubble observe -f --ip-trace-id 13345`. Flows between client and server show with the matching ID. The docs build the Hubble CLI from the hubble repo for this flag and connect with `cilium hubble port-forward`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/observability/hubble/ip-packet-tracing/. 

Method: documentation only; no commands were run.
