---
id: computing-software.cloud-infrastructure-engineering.cilium.l7-policy-rules-overview
name: l7-policy-rules-overview
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, layer7, l7rules, http-403, dns-refused, envoy-proxy]
level: advanced
status: docs-checked
description: "How Cilium L7 rules nest in L4 rules: union of HTTP or DNS per port, merge/reject behaviour, 403 and REFUSED instead of drops, and Envoy dependency."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Layer 7 policy basics

L7 rules sit inside L4 `toPorts` rules. `L7Rules` is a union: exactly one of `http` or `dns` per port.

- Several `toPorts` with identical PortProtocol selecting overlapping endpoints have their L7 rules merged if the same type; different types are rejected.
- A request passes if at least one rule matches. No rules means all traffic permitted.
- If a plain L4 rule and a similar L4 rule with L7 both exist, the L7 portion has no effect.
- L7 violations are not dropped: HTTP gets 403 access denied, DNS gets REFUSED.
- Port ranges are supported except for DNS rules.
- Host policies (nodeSelector): only DNS L7 works (beta).
- L7 traffic proxies through node-local Envoy (DaemonSet or embedded in the agent pod). Embedded Envoy means L7-targeted traffic depends on agent availability.
- L7 for SNATed IPv6 (pod-to-world) needs a kernel with the fix; stable versions with it: 6.14.1, 6.12.22, 6.6.86, 6.1.133, 5.15.180, 5.10.236.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the Layer 7 policy page: https://docs.cilium.io/en/stable/security/policy/layer7/. Confirmed the L7Rules union, merge and reject behaviour, 403 and REFUSED responses, port range, host policy, Envoy and kernel version notes stated above. Nothing was removed.

Method: documentation only; no commands were run.
