---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-traffic-splitting-weights-canary
name: httproute-traffic-splitting-weights-canary
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, weight, traffic-splitting, canary, blue-green, rollout]
level: practitioner
status: docs-checked
description: "Roll out a new version with backendRef weights: canary by header, 90/10 split, and completing by setting the old weight to 0; weights are proportional, default 1."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/traffic-splitting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rules[].backendRefs` takes several backends; their relative `weight` defines the split.

Facts:

- `weight` is a proportion, not a percentage. The sum of weights within the rule is the denominator.
- `weight` is optional and defaults to 1.
- A single backend gets 100% regardless of its weight.
- Setting a weight to `0` means that backend receives no traffic.

90/10 split:

```yaml
rules:
- backendRefs:
  - name: foo-v1
    port: 8080
    weight: 90
  - name: foo-v2
    port: 8080
    weight: 10
```

Rollout sequence from the guide for `foo.example.com`:

1. **Canary**: two rules with no weights. A rule matching header `traffic: test` sends synthetic traffic to `foo-v2`; everything else goes to `foo-v1`. Routing precedence picks the more specific match for the header.
2. **Gradual**: one rule with `foo-v1` weight 90 and `foo-v2` weight 10.
3. **Complete**: set `foo-v1` weight to `0` so 100% goes to `foo-v2`.

If `foo-v2` errors, change the weights to shift back to `foo-v1` quickly. Once the rollout is final, decommission v1.

## Checked

2026-11-08. Read in full: the HTTP traffic splitting guide (raw markdown on GitHub). Confirmed: weight is proportional with the sum as denominator, defaults to 1, a single backend gets 100%, weight 0 means zero traffic, the 90/10 split, the header traffic=test canary rule and the routing precedence note, and the three rollout stages. Removed: the GRPCRoute and TCPRoute weighting sentence, whose pages are not cited.

Method: documentation only; no commands were run.
