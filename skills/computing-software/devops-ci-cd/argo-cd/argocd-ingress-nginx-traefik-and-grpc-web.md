---
id: computing-software.devops-ci-cd.argo-cd.argocd-ingress-nginx-traefik-and-grpc-web
name: argocd-ingress-nginx-traefik-and-grpc-web
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd-ingress, grpc-web-ingress, ssl-passthrough, argocd-cli-grpc]
level: practitioner
status: docs-checked
description: "Expose Argo CD UI and CLI through ingress: nginx SSL passthrough vs TLS termination with server.insecure, separate gRPC ingress, Traefik h2c routes, and --grpc-web."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD ingress (nginx, Traefik, gRPC-web)

`argocd-server` serves the UI (HTTPS) and the CLI's gRPC API on the **same port**. Ingress has to handle both.

## 1. ingress-nginx with SSL passthrough (simplest)
Controller must run with `--enable-ssl-passthrough`.
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server
  namespace: argocd
  annotations:
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  rules:
    - host: argocd.example.com
      http: { paths: [{ path: /, pathType: Prefix, backend: { service: { name: argocd-server, port: { name: https } } } }] }
```
Argo CD serves its own certificate (the docs show cert-manager for issuing it).

## 2. TLS terminated at ingress
Set `server.insecure: "true"` in argocd-cmd-params-cm, then either:
- one HTTP ingress for the UI and use the CLI with `--grpc-web` (for proxies that do not support HTTP/2), or
- two ingress objects, because the nginx `backend-protocol` annotation accepts only one value (HTTP, HTTPS, GRPC or GRPCS): one for the UI and one for gRPC.
```bash
argocd login argocd.example.com --grpc-web
```

## 3. Traefik (IngressRoute)
```yaml
spec:
  entryPoints: [websecure]
  routes:
    - kind: Rule
      match: Host(`argocd.example.com`)
      priority: 10
      services: [{ name: argocd-server, port: 80 }]
    - kind: Rule
      match: Host(`argocd.example.com`) && Header(`Content-Type`, `application/grpc`)
      priority: 11
      services: [{ name: argocd-server, port: 80, scheme: h2c }]
  tls: { certResolver: default }
```

## Gotchas
- If the CLI cannot connect through a proxy that does not support HTTP/2, add `--grpc-web`.
- With TLS terminated at the ingress, run the API server with TLS disabled (`server.insecure`).

## Verify
- [ ] UI loads over HTTPS; `argocd app list` works from a laptop (with or without `--grpc-web` as designed).

## Checked
2026-10-28. Confirmed on the Argo CD ingress operator manual page: gRPC and HTTPS share one port; nginx `ssl-passthrough` annotation needs `--enable-ssl-passthrough` on the controller; `server.insecure: "true"` in `argocd-cmd-params-cm`; `backend-protocol` accepts a single value (HTTP, HTTPS, GRPC, GRPCS) so two ingress objects are needed; `--grpc-web` for proxies without HTTP/2; the Traefik v3.0 `IngressRoute` example (priority 10/11, `application/grpc` header match, `scheme: h2c`) matches the page.
Removed (not confirmed): the `argocd-server-tls` secret name, the `grpc.argocd.example.com` host, `--sso`, the error message strings, the redirect-loop and webhook gotchas.

Method: documentation only; no commands were run.
