---
id: computing-software.cloud-infrastructure-engineering.knative.http-protocol-redirect
name: http-protocol-redirect
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [http-protocol, https-redirect, redirected, config-network]
level: practitioner
status: docs-checked
description: "Force HTTPS redirection globally or per Service with the http-protocol setting."
sources:
  - https://knative.dev/docs/serving/services/http-protocol/
  - https://knative.dev/docs/serving/encryption/external-domain-tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make Services reject plain HTTP by redirecting clients to HTTPS.

Operators can force HTTPS redirection for all Services through the `http-protocol` setting, described alongside external domain encryption. You can also override the default for one Service or change the global configuration.

Setting:
- Global key: `http-protocol`, in the `config-network` ConfigMap in `knative-serving`.
- Per-service annotation: `networking.knative.dev/http-protocol`.
- Values: `enabled`, where Services accept HTTP traffic; `redirected`, where Services send a 301 redirect for all HTTP connections and ask clients to use HTTPS instead.
- Default: `enabled`.

The two official pages disagree. The HTTP page above (and its examples) uses lower-case `enabled` and `redirected` and says the redirect is a 301. The external domain encryption page uses `Enabled` and `Redirected` and says the redirect is a `302`. Check your installed version's `config-network` ConfigMap and the actual response before relying on the status code or the capitalisation.

Per-Service example:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: example
  namespace: default
  annotations:
    networking.knative.dev/http-protocol: "redirected"
```

Global example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-network
  namespace: knative-serving
data:
  http-protocol: "redirected"
```

With the Operator, put the key under `spec.config.network` of the `KnativeServing` resource.

Redirection only helps when HTTPS is actually served for the external domain; see the external domain encryption skill for enabling certificates. The default `enabled` leaves both schemes working.

## Checked

2026-11-04. Confirmed against the Configuring HTTP page and the Configure external domain encryption page (knative/docs source): global key `http-protocol`, per-service annotation `networking.knative.dev/http-protocol`, the two values, default `enabled`, the per-Service, ConfigMap and Operator examples (`spec.config.network`), and that the external domain page covers `http-protocol` for HTTPS. Conflict between pages: the HTTP page says 301 and lower-case values, the external domain page says `302` and `Enabled`/`Redirected`; the skill now states both. Nothing removed.

Method: documentation only; no commands were run.
