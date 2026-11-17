---
id: computing-software.messaging-and-integration.dapr.sentry-jwks-token-validator
name: sentry-jwks-token-validator
category: computing-software
field: messaging-and-integration
product: dapr
tags: [sentry, jwks, token-validator, spiffe, jwt, configuration, mtls]
level: sme
status: docs-checked
description: "Configure the Sentry jwks token validator to admit non-Kubernetes clients or replace the insecure self-hosted one: sub and audience SPIFFE rules, remote or static keys."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sentry validates the identity of clients requesting certificates. On Kubernetes it checks bound service account tokens; in self-hosted mode the default validator is an insecure allow-all. Extra validators join non-Kubernetes clients to a Kubernetes-mode cluster, or replace the insecure default. The page says you rarely need this outside exotic deployments, and `jwks` is the only validator currently supported.

Rules for the JWT:

- the `sub` claim must match the SPIFFE identity of the Dapr client, format `spiffe://<trust-domain>/ns/<namespace>/<app-id>`;
- the audience must be the SPIFFE ID of Sentry, for example `spiffe://cluster.local/ns/dapr-system/dapr-sentry`;
- normal JWT signature and expiry checks apply.

Remote key source over HTTPS (`caCertificate` is the root of trust for that source):

```yaml
kind: Configuration
apiVersion: dapr.io/v1alpha1
metadata:
  name: sentryconfig
spec:
  mtls:
    enabled: true
    tokenValidators:
      - name: jwks
        options:
          minRefreshInterval: 2m
          requestTimeout: 1m
          source: "https://localhost:1234/"
          caCertificate: "<optional ca certificate bundle string>"
```

Static keys instead (replace `source`):

```yaml
          source: |
            {"keys":[ "12345.." ]}
```

Both live under `spec.mtls.tokenValidators` of the configuration Sentry loads.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
