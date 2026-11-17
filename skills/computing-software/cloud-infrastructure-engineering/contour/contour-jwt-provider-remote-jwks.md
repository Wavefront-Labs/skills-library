---
id: computing-software.cloud-infrastructure-engineering.contour.contour-jwt-provider-remote-jwks
name: contour-jwt-provider-remote-jwks
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [jwt, jwtproviders, remotejwks, jwtverificationpolicy, issuer, audiences, forwardjwt, 401]
level: advanced
status: docs-checked
description: "HTTPProxy JWT verification: jwtProviders issuer/audiences/remoteJWKS, jwtVerificationPolicy require per route, JWKS TLS validation, TLS-only and fallback-cert limits."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/jwt-verification.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy JWT verification with remote JWKS

Contour programs Envoy's jwt_authn filter. It checks issuer, audiences, signature (via JWKS) and time claims (expiry, not-before). Failures return 401. Only TLS-terminating virtual hosts are supported, and it is incompatible with the fallback certificate feature.

```yaml
spec:
  virtualhost:
    fqdn: example.com
    tls:
      secretName: example-com-tls-cert
    jwtProviders:
    - name: provider-1
      issuer: example.com
      audiences: [audience-1, audience-2]
      remoteJWKS:
        uri: https://example.com/jwks.json
        timeout: 1s
        cacheDuration: 5m
      forwardJWT: true
  routes:
  - conditions: [{prefix: /}]
    jwtVerificationPolicy:
      require: provider-1
    services: [{name: s1, port: 80}]
  - conditions: [{prefix: /css}]
    services: [{name: s1, port: 80}]
```

- A route with `jwtVerificationPolicy.require` must present a token matching that provider; routes without a policy (here `/css`) skip verification.
- `forwardJWT: true` passes the JWT to the backend in `Authorization`.
- By default the JWKS server certificate is not validated. Set `remoteJWKS.validation` with mandatory `caSecret` (`<namespace>/<secret>` allowed) and `subjectName`; then `uri` must be `https`. A CA Secret in another namespace needs TLS certificate delegation.

## Checked

2026-11-08. Read the Contour main-branch config page jwt-verification.md in full. Confirmed: checked properties (issuer, audiences, signature, time restrictions), 401 on failure, TLS-terminating hosts only, incompatibility with the fallback certificate, the provider example fields, per-route `require`, `forwardJWT` via the `Authorization` header, and JWKS TLS validation with its `https` requirement and delegation note. No claims removed.

Method: documentation only; no commands were run.
