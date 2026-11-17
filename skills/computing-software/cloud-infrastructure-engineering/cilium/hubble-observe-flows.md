---
id: computing-software.cloud-infrastructure-engineering.cilium.hubble-observe-flows
name: hubble-observe-flows
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, hubble, hubble-observe, verdict, l7-http, policy-denied]
level: practitioner
status: docs-checked
description: "Inspect flows with hubble observe filtering by pod, protocol and verdict to find HTTP policy denials and TCP SYN drops from policy."
sources:
  - https://docs.cilium.io/en/stable/observability/hubble/hubble-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# hubble observe

Prereqs: Cilium installed, Hubble enabled, Hubble CLI installed, Hubble API reachable. Run `cilium status` and `hubble status` to confirm.

Commands from the docs:
- `hubble observe --pod deathstar --protocol http` shows L7 HTTP flows: `http-request FORWARDED`, `http-response FORWARDED (HTTP/1.1 200 0ms ...)`, and `http-request DROPPED` for a request violating L7 policy (e.g. PUT /v1/exhaust-port).
- `hubble observe --pod deathstar --verdict DROPPED` shows all drops. A pod lacking the required label shows `Policy denied DROPPED (TCP Flags: SYN)` repeated as the client retransmits SYN; the client side sees a hang or curl exit code 28.
- `hubble help observe` lists all filters.

Interpretation: an L7 denial returns an HTTP response (Access denied) and shows as http-request DROPPED; an L3/L4 denial is a silent SYN drop and shows Policy denied.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/observability/hubble/hubble-cli/. 

Method: documentation only; no commands were run.
