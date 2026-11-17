---
id: computing-software.cybersecurity-defensive.authelia.kubernetes-deployment-notes
name: kubernetes-deployment-notes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, kubernetes, helm-chart, enableservicelinks, external-traffic-policy, secrets, ingress]
level: advanced
status: docs-checked
description: "Avoid Authelia's Kubernetes pitfalls: disable service links, preserve client source IP, load secrets from a Secret, and use stateless session and storage."
sources:
  - https://www.authelia.com/integration/kubernetes/introduction/
  - https://www.authelia.com/integration/kubernetes/secrets/
  - https://www.authelia.com/configuration/session/introduction/
  - https://www.authelia.com/configuration/first-factor/file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three things commonly go wrong on Kubernetes.

1. Service links. Authelia's configuration system conflicts with Kubernetes service-link environment variables, so set `enableServiceLinks: false` in the PodSpec:

```yaml
spec:
  enableServiceLinks: false
```

2. Client IP. If the service in front of your ingress does not use `externalTrafficPolicy: Local`, Authelia and your applications may see an invalid remote IP. An invalid IP would undermine IP-based regulation and `networks` access control rules (a consequence of the page's warning, not stated there). See the Kubernetes documentation on preserving the client source IP.

3. Statefulness. The memory session provider and SQLite are stateful and not recommended where replicas exist. Use Redis for sessions and PostgreSQL or MySQL for storage.

Secrets are normally kept in a Kubernetes Secret with keys like `JWT_SECRET`, `SESSION_SECRET`, `STORAGE_PASSWORD`, `STORAGE_ENCRYPTION_KEY`, `LDAP_PASSWORD`, `SMTP_PASSWORD`, `REDIS_PASSWORD`, `REDIS_SENTINEL_PASSWORD`, `DUO_SECRET_KEY`, `OIDC_HMAC_SECRET` and `OIDC_ISSUER_PRIVATE_KEY`, mounted as files (a Secret volume, read-only) and referenced with the `_FILE` environment variables. Manifest (`stringData` or base64 `data`) and Kustomize `secretGenerator` forms are shown. The Helm chart generates and injects its own secrets automatically. Include only the secrets you actually use; the page says the examples are not meant to be used as is.

Do not copy the page's Usage env list blindly: it contains mismatches. It points `AUTHELIA_STORAGE_POSTGRES_PASSWORD_FILE` at the `STORAGE_ENCRYPTION_KEY` file, uses the legacy name `AUTHELIA_JWT_SECRET_FILE` (the current key is `AUTHELIA_IDENTITY_VALIDATION_RESET_PASSWORD_JWT_SECRET_FILE`), and writes the sentinel variable as `AUTHELIA_REDIS_HIGH_AVAILABILITY_SENTINEL_PASSWORD_FILE` without the `SESSION_` part. Verify each name against the secrets reference table.

Sizing: with file-based authentication the Kubernetes page warns that the default argon2id settings use about 1 GB of RAM per hash, so allow for it or tune the provider or you risk an out-of-memory kill at login. (The file backend reference lists a default `memory` of 65536 KiB, which is about 64 MiB, so treat the 1 GB figure as a conservative note and measure.)

Check: `kubectl logs` shows Authelia listening, and the client IP in the Authelia log matches a real client.

## Checked

2026-11-08. Read in full: integration/kubernetes/introduction and secrets, session introduction, first-factor/file. Removed uncited healthcheck and ingress-guide claims; noted env-name mismatches in the page's own example and the RAM warning.

Method: documentation only; no commands were run.
