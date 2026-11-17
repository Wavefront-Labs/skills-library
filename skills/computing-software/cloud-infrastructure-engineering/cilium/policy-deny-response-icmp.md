---
id: computing-software.cloud-infrastructure-engineering.cilium.policy-deny-response-icmp
name: policy-deny-response-icmp
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, policy-deny-response, icmp, egress, timeouts, experimental]
level: advanced
status: docs-checked
description: "Make Cilium send ICMP destination unreachable for egress traffic denied by policy using --policy-deny-response=icmp instead of silent drops."
sources:
  - https://docs.cilium.io/en/stable/security/policy/intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy deny response

Default: denied egress packets are silently dropped, so apps see connection timeouts.

Option `--policy-deny-response`:
- `none` (default): silent drop.
- `icmp` (experimental): send ICMP Destination Unreachable back to the source pod when egress traffic is denied, giving fast failure.

## Limits and gotchas
- Applies only to IPv4 and IPv6 egress pod traffic denied by network policy. Ingress denial behaviour is not supported (the page points to GitHub issue 41859).
- Your policies must allow ICMP ingress to the source pod. If ingress policy blocks ICMP the app never sees the rejection and still times out.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the policy enforcement modes and rule basics page: https://docs.cilium.io/en/stable/security/policy/intro/. Confirmed the statements above. Nothing was removed.

Method: documentation only; no commands were run.
