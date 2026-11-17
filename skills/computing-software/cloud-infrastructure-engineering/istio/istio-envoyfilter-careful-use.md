---
id: computing-software.cloud-infrastructure-engineering.istio.istio-envoyfilter-careful-use
name: istio-envoyfilter-careful-use
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, envoyfilter, envoy-patch, listener-filter]
level: practitioner
status: docs-checked
description: "Apply last-resort Envoy patches with EnvoyFilter, scope them by workload selector and priority, and plan for breakage at every Istio upgrade."
sources: ["https://istio.io/latest/docs/reference/config/networking/envoy-filter/", "https://istio.io/latest/docs/ops/diagnostic-tools/proxy-cmd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
EnvoyFilter patches generated Envoy config directly, which is outside Istio's compatibility guarantees. Use it only when no first-class API exists.

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata: {name: add-header, namespace: shop}
spec:
  workloadSelector: {labels: {app: web}}
  configPatches:
  - applyTo: HTTP_FILTER
    match: {context: SIDECAR_INBOUND, listener: {filterChain: {filter: {name: envoy.filters.network.http_connection_manager}}}}
    patch: {operation: INSERT_BEFORE, value: {name: envoy.filters.http.lua}}
```

Gotchas: the reference says the API is deeply tied to Istio's networking internals and Envoy's xDS API, so envoy configuration provided this way should be carefully monitored across Istio proxy version upgrades. When several EnvoyFilters bind to the same workload in a namespace, patches are processed in order of creation time, and behaviour is undefined if they conflict. A filter defined in the config root namespace without a `workloadSelector` applies to all workloads (sidecars and gateways), so set `workloadSelector` unless that is intended.

Verify: `istioctl proxy-config listeners <pod> -o json` shows the patched filter, and `istioctl proxy-status` shows the proxy `SYNCED`.

## Checked

2026-11-03. Confirmed in the EnvoyFilter reference (NOTE 1 to 3, `configPatches`, `applyTo: HTTP_FILTER`, `context: SIDECAR_INBOUND`, `operation: INSERT_BEFORE`, `workloadSelector`) and the proxy-cmd page (`proxy-config listeners ... -o json`, `proxy-status` states). Removed: the `STALE`-after-bad-patch claim, `istioctl analyze` as a check, and the version-control advice.

Method: documentation only; no commands were run.
