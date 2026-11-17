---
id: computing-software.cloud-infrastructure-engineering.zot.oidc-workload-identity-bearer
name: oidc-workload-identity-bearer
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, bearer-oidc, workload-identity, image-pull-secret, issuer-audiences, token-endpoint]
level: advanced
status: docs-checked
description: "Accept OIDC ID tokens from workloads in Zot via http.auth.bearer.oidc: issuer and audiences, lazy init, token-service login and Kubernetes pull secrets."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
"bearer": { "realm": "https://zot.example.com/zot/auth/token", "service": "zot.example.com",
  "oidc": [ { "issuer": "https://kubernetes.default.svc.cluster.local", "audiences": ["zot", "https://zot.example.com"] } ] }
```

Attributes: `issuer` (required), `audiences` (at least one), `claimMapping` (CEL), `certificateAuthority` or `certificateAuthorityFile` (mutually exclusive), `skipIssuerVerification` (testing only, default `false`).

Behaviour:
- Tokens carry identity only; access comes from `accessControl`. Users in no policy get 403.
- Opaque access tokens are rejected; the token must be a JWT.
- Since v2.1.23 tokens route to their configured issuer and unknown issuers are rejected without network calls.
- Providers initialise lazily, so an unreachable issuer does not block startup. Discovery and key fetches time out after 10 seconds; failed refreshes keep cached keys.
- OIDC can coexist with `cert` or `awsSecretsManager`; Zot tries OIDC first.

Token-service login: `realm` must be the absolute URL of Zot's token endpoint (GET and POST). The client sends the JWT as the HTTP Basic password (username has no identity meaning and must not contain a colon); Zot returns it as `token` and `access_token`, and the client retries with `Authorization: Bearer`.

For Kubernetes, put the identity token in a `kubernetes.io/dockerconfigjson` imagePullSecret `password` field.

## Checked

2026-11-04. Read against the zot authn-authz article (OIDC Bearer section); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
