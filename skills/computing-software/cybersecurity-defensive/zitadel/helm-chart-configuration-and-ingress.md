---
id: computing-software.cybersecurity-defensive.zitadel.helm-chart-configuration-and-ingress
name: helm-chart-configuration-and-ingress
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, kubernetes, helm, ingress, login-v2, security-context]
level: practitioner
status: docs-checked
description: "Configure the ZITADEL Helm chart replicas, images, security context, external domain and separate ingresses for the API and Login UI."
sources:
  - https://zitadel.com/docs/self-hosting/deploy/kubernetes/configuration
  - https://zitadel.com/docs/self-hosting/deploy/kubernetes/ingress
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Helm chart configures ZITADEL through `values.yaml`.

Global settings: `replicaCount` for replicas, `image` (repository `ghcr.io/zitadel/zitadel`, tag, pull policy) and a separate `login.image` for the Login container. The guide's example pod and container security contexts use non-root user 1000, a RuntimeDefault seccomp profile, a read-only root file system, no privilege escalation and all capabilities dropped.

ZITADEL settings go under `zitadel.configmapConfig`:

```yaml
zitadel:
  configmapConfig:
    ExternalDomain: "zitadel.example.com"
    ExternalPort: 443
    ExternalSecure: true
    TLS:
      Enabled: false
```

TLS terminates at the ingress controller; the containers do not terminate TLS. `FirstInstance` configures the initial admin user.

Ingress: two separate Ingress resources, usually with the same host and certificate. The ZITADEL ingress serves everything at `/`. The Login ingress is configured under `login.ingress` and serves `/ui/v2/login`. The example uses Traefik with `websecure` entrypoints and a TLS secret.

The guide's `FirstInstance` admin password is an example placeholder; set your own and do not keep example credentials.

## Checked

2026-11-08. Read in full: the Kubernetes configuration page and the ingress page. The security context values are the guide's example settings, not stated chart defaults; the text now says so.

Method: documentation only; no commands were run.
