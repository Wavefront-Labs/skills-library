---
id: computing-software.cloud-infrastructure-engineering.istio.istio-access-logging
name: istio-access-logging
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, access-logging, access-log, envoy-logs]
level: practitioner
status: docs-checked
description: "Turn on Envoy access logging with the Telemetry API, filter to errors, and avoid log volume spikes in the mesh."
sources: ["https://istio.io/latest/docs/tasks/observability/logs/access-log/", "https://istio.io/latest/docs/reference/config/telemetry/", "https://istio.io/latest/docs/ops/common-problems/network-issues/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable per workload or namespace with Telemetry and the built-in `envoy` provider.

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata: {name: errors-only, namespace: shop}
spec:
  accessLogging:
  - providers: [{name: envoy}]
    filter: {expression: "response.code >= 400"}
```

Read them with `kubectl logs <pod> -c istio-proxy`. The `meshConfig.accessLogFile=/dev/stdout` setting is the older mesh-wide switch.

Gotchas: `filter.expression` is a CEL expression (the reference gives `response.code >= 400` as an example). In the default log format the Envoy response flag follows the response code; with a custom format include `%RESPONSE_FLAGS%`. Common flags per the Istio troubleshooting page: `NR` no route configured (check the DestinationRule or VirtualService), `UO` upstream overflow from circuit breaking, `UF` failed to connect to upstream (check for an mTLS conflict).

Verify: a request answered with a status of 400 or more produces a line from `kubectl logs -l app=<app> -c istio-proxy`, and a successful request produces none under the filter.

## Checked

2026-11-03. Confirmed in the Istio access-log task (Telemetry API recommended, `meshConfig.accessLogFile` as the older route, `kubectl logs ... -c istio-proxy`), the Telemetry reference (`accessLogging`, CEL `expression` with `response.code >= 400`) and the traffic-management problems page (`%RESPONSE_FLAGS%`, `NR`, `UO`, `UF`). Removed: the `UH` and `URX` flag meanings and the claim that a namespace-level block overrides the mesh default (not on the pages read), volume/CPU and rollout advice.

Method: documentation only; no commands were run.
