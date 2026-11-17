---
id: computing-software.cloud-infrastructure-engineering.istio.istio-envoy-admin-debugging
name: istio-envoy-admin-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, envoy-admin, istioctl-proxy-config, log-level]
level: practitioner
status: docs-checked
description: "Raise sidecar log levels temporarily, read stats and config dump through pilot-agent, and avoid leaving debug logging on."
sources: ["https://istio.io/latest/docs/ops/common-problems/security-issues/", "https://istio.io/latest/docs/ops/configuration/telemetry/envoy-stats/", "https://istio.io/latest/docs/ops/best-practices/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each sidecar exposes Envoy admin locally on 15000. Use `pilot-agent request` or istioctl rather than exposing the port.

```sh
istioctl proxy-config log deploy/web.shop --level connection:debug,rbac:debug
kubectl exec deploy/web -n shop -c istio-proxy -- pilot-agent request GET stats
kubectl exec deploy/web -n shop -c istio-proxy -- pilot-agent request GET config_dump > dump.json
istioctl proxy-config log deploy/web.shop --level warning
```

Gotchas: the security best-practices page says port 15000 provides debugging endpoints and is exposed over localhost only, so any application in the same pod can reach it (there is no trust boundary between sidecar and application). The Istio security-problems page uses `istioctl proxy-config log <workload> --level rbac:debug` to see why an AuthorizationPolicy allowed or denied a request, and `pilot-agent request GET config_dump` to dump the proxy configuration.

Verify: after `--level rbac:debug` a request logs an `rbac checking request` line, and the sidecar log shows the policy decision.

## Checked

2026-11-03. Confirmed in the Istio security-problems page (`istioctl proxy-config log ... --level rbac:debug`, `pilot-agent request GET config_dump`), the Envoy stats page (`pilot-agent request GET stats`) and the security best-practices page (port 15000 localhost-only). Removed: the `grep` filter on `rq_5xx|pending|ejections`, the CPU/disk and restart-reset claims, the secret-material claim, and the routine-inspection advice (not on the pages read).

Method: documentation only; no commands were run.
