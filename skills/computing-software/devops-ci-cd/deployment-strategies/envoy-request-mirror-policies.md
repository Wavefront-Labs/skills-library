---
id: computing-software.devops-ci-cd.deployment-strategies.envoy-request-mirror-policies
name: envoy-request-mirror-policies
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, envoy-mirror, request-mirror-policies, traffic-mirroring, shadow-traffic, istio-mirror, runtime-fraction]
level: practitioner
status: docs-checked
description: "Mirror live traffic to a shadow service with Envoy request_mirror_policies: config, sampling with runtime_fraction, Istio mirror, shadow host headers, and side-effect safety."
sources:
  - https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto#config-route-v3-routeaction-requestmirrorpolicy
  - https://istio.io/latest/docs/tasks/traffic-management/mirroring/
  - https://gateway-api.sigs.k8s.io/guides/http-request-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envoy request mirror policies

Envoy copies requests to a second cluster fire-and-forget: responses from the mirror are discarded, so users see only the primary.

## Envoy route config
```yaml
route_config:
  virtual_hosts:
  - name: api
    domains: ["api.example.com"]
    routes:
    - match: { prefix: "/" }
      route:
        cluster: api-v1
        request_mirror_policies:
        - cluster: api-v2-shadow
          # runtime_fraction: set this to mirror only a fraction of requests (see the RuntimeFractionalPercent type in the Envoy API)
```
- The mirrored request's `Host`/`:authority` gets `-shadow` appended (`api.example.com-shadow`), so the shadow service can tell mirrored traffic apart (and so must accept that host). This can be disabled with `disable_shadow_host_suffix_append`.
- Multiple mirror policies are allowed (shadow several versions).

## Istio
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: { name: api }
spec:
  hosts: [api]
  http:
  - route: [{ destination: { host: api, subset: v1 }, weight: 100 }]
    mirror: { host: api, subset: v2 }
    mirrorPercentage: { value: 10.0 }
```
Gateway API: `RequestMirror` filter in an HTTPRoute (`filters: [{ type: RequestMirror, requestMirror: { backendRef: { name: api-v2, port: 80 } } }]`).

## Side effects: the real risk
The shadow receives real writes. Make it safe:
- Point the shadow at a separate datastore or run it in read-only/dry-run mode (feature flag keyed off the `-shadow` host).
- Stub outbound calls that charge cards, send emails, publish events.
- Idempotency keys don't save you if the shadow writes to the same DB first.
- Auth tokens in mirrored requests reach the shadow: keep it in the same trust zone.

## Comparing results
Since responses are dropped, compare via logs/metrics: error rates and latency by cluster, or log request IDs and response hashes from both versions (Diffy-style) and diff offline.

## Verify
- [ ] Shadow receives the configured share of traffic and primary latency is unchanged.
- [ ] No external side effects from the shadow during a test window.

## Checked

2026-10-28. Confirmed from the Envoy RouteAction reference (`request_mirror_policies` list, mirror policy fields `cluster`, `runtime_fraction`, `trace_sampled`, `disable_shadow_host_suffix_append`; the host/authority header gets `-shadow` appended), the Istio mirroring task (`mirror`, `mirrorPercentage`, `-shadow` suffix, fire and forget, responses discarded, `networking.istio.io/v1`) and the Gateway API request mirroring guide (`RequestMirror` filter). Removed (not found): the `runtime_fraction` sub-fields and runtime key, bandwidth claim, Gateway API `percent` field, the Envoy cluster metric name.

Method: documentation only; no commands were run.
