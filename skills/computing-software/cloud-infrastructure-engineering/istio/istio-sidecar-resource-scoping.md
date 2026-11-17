---
id: computing-software.cloud-infrastructure-engineering.istio.istio-sidecar-resource-scoping
name: istio-sidecar-resource-scoping
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, sidecar-resource, sidecar-scope, egress-hosts]
level: practitioner
status: docs-checked
description: "Limit what each workload's proxy imports with a Sidecar resource egress hosts list, and avoid duplicate selector-less Sidecar objects."
sources: ["https://istio.io/latest/docs/reference/config/networking/sidecar/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `Sidecar` configures which services a workload's proxy can reach (and its inbound listeners). Egress `hosts` use `namespace/dnsName` format.

```yaml
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata: {name: default, namespace: shop}
spec:
  egress:
  - hosts: ["./*", "istio-system/*", "payments/*"]
```

Host syntax from the reference: the namespace can be `*` (any), `.` (the sidecar's own) or `~` (none); `*` as dnsName selects every service in that namespace; `*/*` reaches every service exported to the sidecar's namespace; `~/*` trims configuration for a sidecar that makes no outbound connections; a `~` prefix on the namespace excludes hosts (for example `~prod-us2/*`). Only services and configuration exported to the sidecar's namespace (`exportTo` `*`) can be referenced.

Gotchas: each namespace can have only one Sidecar without a `workloadSelector` (the namespace default, conventionally named `default`); more than one is undefined behaviour, as is two selector-based Sidecars selecting the same workload. A Sidecar in the MeshConfig root namespace applies by default to namespaces that have none, and should have no `workloadSelector`. A Sidecar with `workloadSelector` omitted applies to all workloads in its namespace. If `egress` is not specified, the proxy inherits the namespace-wide or global default. Blocking unknown external destinations is a separate setting, `outboundTrafficPolicy`.

## Checked

2026-11-03. Confirmed against the Sidecar reference: egress `hosts` format and wildcards, `exportTo` note, selector-less and root-namespace default rules and their undefined-behaviour notes, `outboundTrafficPolicy`. Removed: unsourced claims about memory and push savings, 503/passthrough on omitted hosts, no effect on gateways, `istioctl proxy-config` verify step, and rollout advice.
Method: documentation only; no commands were run.
