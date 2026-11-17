---
id: computing-software.cloud-infrastructure-engineering.contour.contour-global-external-authorization
name: contour-global-external-authorization
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [globalextauth, ext-authz, contour-authserver, global-auth, http-virtual-hosts, authpolicy-disabled]
level: advanced
status: docs-checked
description: "Global external authorization via the globalExtAuth config block (Contour 1.25+): HTTP and HTTPS hosts, per-vhost disable, HTTPS override, and caveats."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/external-authorization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global external authorization

Since Contour 1.25 one auth configuration can cover every virtual host, including plain HTTP ones (per-vhost authorization otherwise requires TLS). Deploy an ExtensionService first (the guide uses `contour-authserver` htpasswd on port 9443).

Config file:

```yaml
globalExtAuth:
  extensionService: projectcontour-auth/htpasswd
  failOpen: false
  authPolicy:
    context:
      header1: value1
      header2: value2
  responseTimeout: 1s
```

Behaviour verified in the guide:
- An HTTPProxy with no `authorization` block now returns `401` with `www-authenticate: Basic realm="default"` until credentials are supplied; with `curl --user` the app receives injected `Auth-*` headers, including `Auth-Context-Header1` from the context map.
- Exclude a vhost by setting `authorization.authPolicy.disabled: true`.
- Override on an HTTPS vhost by adding its own `authorization.extensionRef` block. Overrides are only possible on HTTPS vhosts.

Caveats:
1. Only one external authorization server per virtual host.
2. HTTP hosts are supported only through global external authorization.
3. It cannot be used with the TLS fallback certificate, because SNI is required.

contour-authserver stores htpasswd data in a Secret (key `auth`, annotation `projectcontour.io/auth-type=basic`) in its namespace.

## Checked

2026-11-08: read the Contour docs guides/external-authorization in full. Confirmed: global external authorization from Contour 1.25 for HTTP and HTTPS hosts, the globalExtAuth block, contour-authserver htpasswd on port 9443, the 401 with www-authenticate Basic realm default, Auth-prefixed and context headers, authPolicy disabled, HTTPS-only override via extensionRef, the three caveats, and the Secret key and annotation.

Method: documentation only; no commands were run.
