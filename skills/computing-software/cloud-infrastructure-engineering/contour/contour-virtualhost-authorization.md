---
id: computing-software.cloud-infrastructure-engineering.contour.contour-virtualhost-authorization
name: contour-virtualhost-authorization
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [authorization, extensionref, authpolicy, failopen, context, ext-authz]
level: advanced
status: docs-checked
description: "HTTPProxy virtualhost.authorization: extensionRef, failOpen for migrations, authPolicy enable/disable with context key/values per virtual host and route."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/client-authorization.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/external-authorization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy virtual host authorization

Bind an ExtensionService to a TLS-terminating vhost:

```yaml
spec:
  virtualhost:
    fqdn: local.projectcontour.io
    tls:
      secretName: ingress-conformance-echo
    authorization:
      extensionRef:
        name: htpasswd
        namespace: projectcontour-auth
      failOpen: false
      authPolicy:
        context:
          realm: default
  routes:
  - conditions: [{prefix: /public}]
    authPolicy:
      disabled: true
    services: [{name: s1, port: 80}]
  - conditions: [{prefix: /}]
    authPolicy:
      context:
        realm: admin
    services: [{name: s1, port: 80}]
```

- One ExtensionService per vhost; different vhosts may use different ones. Requires TLS termination and is incompatible with the fallback certificate.
- `failOpen: true` lets requests through when the auth server fails; handy while migrating from per-application authorization.
- `authPolicy` on the vhost sets whether authorization is enabled and the initial `context` map (key/values sent with every check request, for example a basic-auth realm or OIDC parameters).
- If the vhost disables authorization, routes without their own `authPolicy` have it disabled by default; a route `authPolicy` (`.spec.routes[].authPolicy`) can enable or disable independently of the vhost, and a route's `context` overwrites the vhost value for the same key.

## Checked

2026-11-08. Read the Contour main-branch config page client-authorization.md in full, and lines 180-345 of the external-authorization guide (the ExtensionService and HTTPProxy `authorization.extensionRef` example); the rest of the guide was not read. Confirmed: one ExtensionService per vhost, TLS termination required, incompatibility with the fallback certificate, `failOpen` for migrations, `authPolicy` enable and context semantics at vhost and route level, and `extensionRef` with name and namespace. Removed `responseTimeout` and the `extensionRef`-independent example values that were not on those pages; the realm values and host name are illustrative.

Method: documentation only; no commands were run.
