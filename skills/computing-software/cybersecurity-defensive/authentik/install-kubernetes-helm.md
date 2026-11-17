---
id: computing-software.cybersecurity-defensive.authentik.install-kubernetes-helm
name: install-kubernetes-helm
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, kubernetes, helm, values-yaml, gateway-api, ingress]
level: practitioner
status: docs-checked
description: "Install authentik on Kubernetes with the Helm chart: values.yaml secrets, ingress or Gateway API HTTPRoute, external PostgreSQL for production and file storage."
sources:
  - https://docs.goauthentik.io/install-config/install/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy authentik with Helm. Requires Kubernetes and Helm.

Generate passwords with `pwgen -s 50 1` or `openssl rand 60 | base64 -w 0`. Minimal `values.yaml`:
```yaml
authentik:
    secret_key: "PleaseGenerateASecureKey"
    error_reporting:
        enabled: true
    postgresql:
        password: "ThisIsNotASecurePassword"

server:
    ingress:
        ingressClassName: nginx | traefik | kong
        enabled: true
        hosts:
            - authentik.domain.tld

postgresql:
    enabled: true
    auth:
        password: "ThisIsNotASecurePassword"
```
Gateway API instead of ingress: replace `server.ingress` with `server.route.main` (`enabled: true`, `hostnames`, `parentRefs` with `name: shared-gateway`, `namespace: default`). The chart creates an `HTTPRoute` only; create the `Gateway` yourself and make `parentRefs` match its name and namespace.

Install:
```shell
helm repo add authentik https://charts.goauthentik.io
helm repo update
helm upgrade --install authentik authentik/authentik -f values.yaml
```
Database migrations apply automatically at startup. Then open the server on port 9000 and set the `akadmin` password.

## Gotchas
- The bundled PostgreSQL is for demo and test only; production should use a separately managed database (CloudNativePG or Zalando Postgres Operator) configured via the PostgreSQL settings in the configuration reference.
- The chart mounts no storage for uploaded files by default: configure `global.volumes` and `global.volumeMounts`, or use S3.
- All configurable values are on ArtifactHub; replicas can be autoscaled.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/install-config/install/kubernetes/ (read in full).
