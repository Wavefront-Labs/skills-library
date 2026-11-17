---
id: computing-software.cloud-infrastructure-engineering.linkerd.expose-viz-dashboard-nginx
name: expose-viz-dashboard-nginx
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, viz, dashboard, ingress, nginx]
level: advanced
status: docs-checked
description: "Expose the Viz dashboard through an NGINX Ingress with basic auth and the upstream-vhost and header settings it needs."
sources:
  - https://linkerd.io/2.19/tasks/exposing-dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of running `linkerd viz dashboard` each time, you can expose the Viz web service through an ingress. The ingress also exposes Grafana if Viz is linked to it through `grafana.url`.

For NGINX with basic auth, create a Secret in `linkerd-viz` with an `auth` key holding htpasswd data, and an Ingress for the `web` Service on port 8084:

```yaml
metadata:
  name: web-ingress
  namespace: linkerd-viz
  annotations:
    nginx.ingress.kubernetes.io/upstream-vhost: $service_name.$namespace.svc.cluster.local:8084
    nginx.ingress.kubernetes.io/configuration-snippet: |
      proxy_set_header Origin "";
      proxy_hide_header l5d-remote-ip;
      proxy_hide_header l5d-server-id;
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: web-ingress-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required"
spec:
  ingressClassName: nginx
  rules:
    - host: dashboard.example.com
```

The sample secret uses admin/admin, so replace it using the ingress-nginx authentication documentation. A stronger option than basic auth is an authentication proxy such as oauth2-proxy, deployed in front of the dashboard.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/exposing-dashboard/.

Removed or reworded: Annotation explanations and the tap-data warning, which the page does not give.

Method: documentation only; no commands were run.
