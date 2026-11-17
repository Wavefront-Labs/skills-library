---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-502-504-diagnosis
name: ingress-502-504-diagnosis
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, 502-bad-gateway, 504-gateway-timeout, ingress-troubleshooting, ingress-nginx, keepalive, troubleshooting]
level: practitioner
status: docs-checked
description: "Find the cause of Ingress 502/503/504 errors: read controller logs, map messages to keepalive races, wrong ports, backend protocol, header size, timeouts and rollouts."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/", "https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/", "https://kubernetes.github.io/ingress-nginx/user-guide/monitoring/", "https://github.com/kubernetes/ingress-nginx", "https://github.com/nginx/nginx/blob/master/src/http/ngx_http_upstream.c", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingress 502/504 diagnosis

ingress-nginx is retired upstream: its README says best-effort maintenance ended in March
2026, with no further releases, bug fixes or security updates afterwards, and recommends
choosing a Gateway API implementation instead. The method below applies to any proxy
(Gateway API implementations, Envoy, Traefik, cloud LBs); the log lines and settings are
nginx and ingress-nginx specific.

## First: who returned the error?
- Body/server header from the cloud LB (e.g. `awselb/2.0`) vs the ingress controller vs the app.
- Controller access log upstream fields tell you if a backend was even tried:
```bash
kubectl -n ingress-nginx logs deploy/ingress-nginx-controller --since=10m | grep ' 50[234] '
# default log format includes upstream_addr, upstream_response_length, upstream_response_time, upstream_status
```

## Status meanings in ingress-nginx
- **503** with empty upstream: the controller has no backend for the request, typically a
  Service with no ready endpoints. `kubectl get endpointslices -l kubernetes.io/service-name=<svc>`;
  look for failing readiness probes or a wrong selector.
- **502** = upstream connection failed or closed mid-response.
- **504** = upstream did not answer within `proxy-read-timeout` (ConfigMap default 60 s).

## Map error-log lines to causes
These are nginx's own error-log strings (present in nginx's upstream module source).
| Controller error log | Cause | Fix |
|---|---|---|
| `connect() failed (111: Connection refused)` | wrong `targetPort`, app listening on 127.0.0.1, pod not started | fix port; bind 0.0.0.0 |
| `upstream prematurely closed connection` | app idle timeout shorter than the proxy's keepalive; app crash | set the app's keepalive timeout above `upstream-keepalive-timeout` (ConfigMap default 60 s), or lower that setting |
| `upstream sent too big header` | large cookies/JWT headers | `nginx.ingress.kubernetes.io/proxy-buffer-size: "16k"` (annotation example in the docs uses `8k`) |
| `upstream timed out (110)` | slow endpoint | fix app, or raise `nginx.ingress.kubernetes.io/proxy-read-timeout` (unitless seconds, e.g. `"300"`) on that Ingress only |
| SSL handshake errors to upstream | backend serves HTTPS | `nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"` (or GRPC/GRPCS) |
| `no live upstreams` | every endpoint is currently marked failed | check pods and the failure settings (`max_fails`) |

## 502s only during deploys
Endpoints removal races with pod shutdown: the proxy can still send to a terminating pod.
Add `preStop: {sleep: {seconds: 10}}` (the `sleep` handler is in the PodLifecycleSleepAction
feature gate: beta and on by default from Kubernetes 1.30, stable from 1.34) or an `exec`
`sleep 10`. A `preStop` hook runs before SIGTERM and counts against
`terminationGracePeriodSeconds`, so keep that larger than hook time plus shutdown time;
make the app finish in-flight requests on SIGTERM, and set `maxUnavailable: 0`.

## 502s at a steady low rate
Keepalive race: the app closes an idle pooled connection at the same moment the proxy
reuses it. Many app servers default to idle timeouts shorter than the proxy's 60 s
(check your runtime's `keepAliveTimeout` equivalent). Set the app's keepalive above the
proxy's idle timeout.

## Reproduce
```bash
kubectl run t --rm -it --image=nicolaka/netshoot -- \
  curl -sv -H 'Host: shop.example.com' http://ingress-nginx-controller.ingress-nginx/path
kubectl port-forward svc/<backend> 8080:80   # bypass ingress: if this also fails it is the app
```

## Verify
- [ ] Error rate from controller metrics `nginx_ingress_controller_requests{status=~"5.."}` back to baseline
  (the request metrics carry a `status` label).

## Checked
2026-10-27. Documentation releases: ingress-nginx controller v1.15.1 (README, annotation and ConfigMap docs, monitoring docs, Lua balancer and metrics source), nginx upstream module source (master), Kubernetes website main (v1.38 dev tree; latest release v1.37.1).
Confirmed: retirement text; `proxy-read-timeout` and `upstream-keepalive-timeout` defaults (60); annotation names and units; 503 when no backend exists; the five error-log strings in nginx's source; `PodLifecycleSleepAction` stages (beta 1.30, stable 1.34); preStop timing semantics; request metric name and `status` label.
Method: documentation only; no commands were run.
