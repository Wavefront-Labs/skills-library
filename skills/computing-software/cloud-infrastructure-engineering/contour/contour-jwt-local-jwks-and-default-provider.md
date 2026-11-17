---
id: computing-software.cloud-infrastructure-engineering.contour.contour-jwt-local-jwks-and-default-provider
name: contour-jwt-local-jwks-and-default-provider
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [jwt, localjwks, default-provider, jwtverificationpolicy, disabled, inclusion, secret]
level: advanced
status: docs-checked
description: "HTTPProxy JWT with localJWKS from a Secret, default provider applied to all routes, disabling per route, and defaults flowing into included child proxies."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/jwt-verification.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JWT local JWKS and default providers

Local keys: instead of `remoteJWKS`, point to a Secret.

```yaml
jwtProviders:
- name: provider-1
  issuer: example.com
  localJWKS:
    secretName: my-jwks
    key: jwks.json
```

The Secret must be `Opaque`, in the same namespace as the HTTPProxy, and the `key` entry must contain a valid JWKS JSON object. Each provider specifies exactly one of `remoteJWKS` or `localJWKS`.

Default provider: `default: true` on a provider applies it to every route automatically, so routes need no `require`. Opt a route out with:

```yaml
- conditions: [{prefix: /css}]
  jwtVerificationPolicy:
    disabled: true
  services: [{name: s1, port: 80}]
```

Inclusion: put the default provider on the root HTTPProxy; all routes in included child HTTPProxies (for example mounted at `/blog`) inherit verification without the child owner configuring anything.

## Checked

2026-11-08. Read the Contour main-branch config page jwt-verification.md in full. Confirmed: `localJWKS` fields, the Opaque and same-namespace Secret rule, exactly one of `remoteJWKS` or `localJWKS`, `default: true` behaviour, `jwtVerificationPolicy.disabled`, and the default provider on the root flowing to included children. Removed the claim that routes can still `require` a different provider alongside a default, and an editorial remark about enforcing authentication across teams.

Method: documentation only; no commands were run.
