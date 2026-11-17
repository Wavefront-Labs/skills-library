---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hubble-observe-drop-debugging
name: hubble-observe-drop-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-networking, hubble-observe, cilium, network-policy, netpol-troubleshooting]
level: practitioner
status: docs-checked
description: "Find dropped and denied flows with Cilium Hubble: hubble observe filters for verdict, pod, port and policy, reading drop reasons, and enabling flow visibility."
sources: ["https://docs.cilium.io/en/stable/observability/hubble/", "https://docs.cilium.io/en/stable/observability/hubble/hubble-cli/", "https://docs.cilium.io/en/stable/observability/visibility/", "https://github.com/cilium/cilium/blob/main/pkg/monitor/api/drop.go", "https://github.com/cilium/cilium/blob/main/hubble/cmd/observe/flows.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging drops with hubble observe

## Access
```bash
cilium hubble enable                     # Hubble Relay by default; add --ui for the UI
cilium hubble port-forward &
hubble status
```

## Filters that matter
```bash
hubble observe --verdict DROPPED -f
hubble observe --namespace shop --verdict DROPPED --last 200
hubble observe --from-pod shop/web-5d8 --to-pod shop/api-7c9 --port 8080
hubble observe --type policy-verdict --namespace shop       # allow/deny decisions
hubble observe --drop-reason-desc POLICY_DENIED             # filter by drop reason
hubble observe --to-fqdn api.stripe.com                     # flows to a DNS name (needs DNS visibility)
hubble observe --protocol dns --namespace shop              # DNS queries and NXDOMAIN
hubble observe --http-status "5+"                           # HTTP status prefix, L7 visibility needed
```
`--type` takes `capture`, `drop`, `l7`, `policy-verdict`, `trace` or `trace-sock`
(`TYPE[:SUBTYPE]`). `--verdict` takes `FORWARDED`, `DROPPED`, `AUDIT`, `REDIRECTED`, `ERROR`,
`TRACED` or `TRANSLATED`. `--http-status` matches a status code prefix such as `404` or
`5+`, not a range. DNS and HTTP flows only appear when an L7 `CiliumNetworkPolicy` rule
covers that traffic (it also restricts that traffic). Output fields include the source and
destination identity (labels), verdict and drop reason.

## Drop reasons (strings from Cilium's drop reason table)
| Reason | Meaning |
|---|---|
| `Policy denied` | no policy allows it (or deny policy); check ingress vs egress side |
| `Policy denied by denylist` | explicit deny rule |
| `Stale or unroutable IP` | destination IP is not a known, routable endpoint; check for a gone pod or a client caching an old pod IP |
| `Unsupported L3 protocol` / `Invalid packet` | datapath-level rejection; also look at MTU and fragmentation |
| `CT: Map insertion failed` | the connection-tracking map is full; raise `bpf-ct-global-tcp-max` / `bpf-ct-global-any-max` (agent defaults 524288 and 262144 in v1.20) |

## Workflow
1. Reproduce the failing request.
2. `hubble observe --verdict DROPPED --from-pod ...` to see whether and where it is dropped.
3. Policy denied: add or fix the policy; re-run and see `FORWARDED`.
4. Nothing in Hubble: traffic never reached the Cilium datapath (DNS failure, app config).

## Retention
Hubble keeps only recent flows in memory (Helm `hubble.eventBufferCapacity`, default 4095);
use the Hubble exporter (`hubble.export.static.enabled=true`) or Hubble metrics to
Prometheus for historical analysis.

## Checked
2026-10-27. Documentation releases: Cilium v1.20.4 (hubble CLI source `hubble/cmd/observe`, `pkg/monitor/api/drop.go`, Helm values) and the current cilium-cli command reference.
Confirmed: every `hubble observe` flag used above and its value set (including that `--http-status` takes a prefix such as `5+`), `cilium hubble enable --ui/--relay`, `cilium hubble port-forward`, all six drop-reason strings, CT flag names and defaults, `eventBufferCapacity` default, Hubble exporter keys, L7 visibility requirement.
Method: documentation only; no commands were run.
