---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-nginx-annotations-and-configmap-tuning
name: ingress-nginx-annotations-and-configmap-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress-nginx, nginx-annotations, rewrite-target, ingress-rate-limit, proxy-body-size, ingress-nginx-tuning, configmap-nginx]
level: practitioner
status: docs-checked
description: "Configure ingress-nginx per Ingress via annotations (rewrite, body size, timeouts, rate limits) and globally via its ConfigMap, avoiding snippet-annotation risks."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/", "https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/", "https://kubernetes.github.io/ingress-nginx/examples/rewrite/", "https://github.com/kubernetes/ingress-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ingress-nginx annotations and ConfigMap tuning

Note: the community ingress-nginx project is retired (its README: best-effort maintenance until
March 2026, then no further releases, bugfixes or security updates, and the repository is archived);
plan migration to Gateway API, but these settings remain what you operate today.

## Per-Ingress annotations (prefix `nginx.ingress.kubernetes.io/`)
```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"        # ConfigMap default is 1m
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"     # unitless seconds; default 60
    nginx.ingress.kubernetes.io/proxy-send-timeout: "120"
    nginx.ingress.kubernetes.io/limit-rps: "20"               # per client IP per controller replica; burst = 5x by default
    nginx.ingress.kubernetes.io/limit-connections: "10"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "GRPC"      # HTTP|HTTPS|GRPC|GRPCS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/auth-url: "https://oauth2.example.com/oauth2/auth"
    nginx.ingress.kubernetes.io/affinity: "cookie"
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api(/|$)(.*)
        pathType: ImplementationSpecific
        backend: {service: {name: api, port: {number: 80}}}
```
Rewrite: capture groups in `path` need `use-regex: "true"` and `pathType: ImplementationSpecific`;
`/api/users` → `/users`. Regex matching applies to **all paths of the same host**: using
`use-regex`, or `rewrite-target` on any Ingress for the host, enforces case-insensitive regex
location matching on every path of that host.

## Global ConfigMap (`ingress-nginx-controller` in the controller namespace / Helm `controller.config`)
```yaml
data:
  proxy-body-size: "10m"
  use-forwarded-headers: "true"        # only behind a trusted L7 LB
  compute-full-forwarded-for: "true"
  enable-real-ip: "true"
  proxy-real-ip-cidr: "10.0.0.0/8"
  keep-alive-requests: "10000"
  upstream-keepalive-connections: "320"
  worker-shutdown-timeout: "240s"      # graceful reloads/terminations
  ssl-protocols: "TLSv1.2 TLSv1.3"
  hsts: "true"
  log-format-escape-json: "true"
  allow-snippet-annotations: "false"   # default false
  annotations-risk-level: "High"       # default High; annotations of a higher risk level are rejected (values: Critical, High, Medium, Low)
```
Per-Ingress annotations override the matching ConfigMap setting.

## Security
`configuration-snippet`/`server-snippet` let Ingress authors inject raw nginx config; the docs
warn this can be dangerous in multi-tenant clusters because people with limited permissions could
retrieve secrets (see CVE-2021-25742). Keep `allow-snippet-annotations` false unless you trust
everyone who can create Ingress objects. The README also says not to use ingress-nginx in
multi-tenant production installs, since it assumes Ingress authors are cluster administrators.

## Verify
```bash
kubectl -n ingress-nginx exec deploy/ingress-nginx-controller -- nginx -T | grep -A3 "server_name app.example.com"
```
- [ ] An upload above the old limit succeeds; requests beyond the rate limit plus burst get the `limit-req-status-code` (default 503); rewrite verified with curl.

## Checked
2026-10-26. Checked against the ingress-nginx docs source (repository kubernetes/ingress-nginx, archived read-only, last commit 2026-03-23). Confirmed: the retirement notice (best-effort maintenance until March 2026, then no releases or security fixes); `proxy-body-size` default 1m; `proxy-read-timeout` default 60 with unitless seconds; `limit-rps` is per client IP per controller replica with burst equal to the limit times a multiplier (default 5) and `limit-req-status-code` default 503; `use-regex` default false and `rewrite-target` on any Ingress of a host enforces case-insensitive regex on all paths of that host; ConfigMap keys `use-forwarded-headers`, `compute-full-forwarded-for`, `enable-real-ip`, `proxy-real-ip-cidr`, `keep-alive-requests` (default 1000), `upstream-keepalive-connections` (default 320), `worker-shutdown-timeout` (default 240s), `ssl-protocols`, `hsts`, `log-format-escape-json`; `allow-snippet-annotations` default false; `annotations-risk-level` accepts Critical, High, Medium or Low with default High; CVE-2021-25742 is referenced in the ConfigMap docs. Removed as unconfirmed: the version gates for those two options, the 413 response, the reload-without-restart note, IngressNightmare CVE-2025-1974 and the 40 MB and 21st-request test.
Method: documentation only; no commands were run.
