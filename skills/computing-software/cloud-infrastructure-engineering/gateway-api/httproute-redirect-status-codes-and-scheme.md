---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-redirect-status-codes-and-scheme
name: httproute-redirect-status-codes-and-scheme
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, requestredirect, redirect, statuscode, 301, 307, 308, 303]
level: practitioner
status: docs-checked
description: "Configure the RequestRedirect filter: supported status codes 301, 302, 303, 307, 308, which are Extended, what the default is, and how unchanged URL parts are preserved."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-redirect-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`RequestRedirect` makes the gateway emit a 3XX response to a matching request. The filter substitutes only the URL components you configure (scheme, hostname, port, path) and preserves the rest of the original URL.

Supported codes:

| Code | Meaning | Use |
|---|---|---|
| 301 | Moved Permanently | permanent moves, HTTP to HTTPS |
| 302 | Found | **default** if none specified; temporary |
| 303 | See Other | POST-Redirect-GET; Extended `HTTPRoute303RedirectStatusCode` |
| 307 | Temporary Redirect | preserves method; Extended `HTTPRoute307RedirectStatusCode` |
| 308 | Permanent Redirect | preserves method; Extended `HTTPRoute308RedirectStatusCode` |

```yaml
filters:
- type: RequestRedirect
  requestRedirect:
    scheme: https
    statusCode: 301
```

With that filter, `GET http://redirect.example/cinnamon` gets a 301 with `location: https://redirect.example/cinnamon`. Hostname, path and implicit port are unchanged.

Use 307 or 308 when the original method (POST, PUT) must be preserved; use 303 to turn a POST into a GET on a confirmation page.

Path redirects use a path modifier and are Extended (`HTTPRoutePathRedirect`): `ReplaceFullPath` replaces the whole path (`/cayenne/pinch` and `/cayenne/teaspoon` both redirect to `/paprika`), while `ReplacePrefixMatch` replaces only the matched prefix (`/cayenne/pinch` to `/paprika/pinch`).

Redirect and rewrite filters cannot be combined in one rule.

## Checked

2026-11-04. Confirmed on the Gateway API redirect and rewrite guide (http-redirect-rewrite.md): status codes and uses, default 302, Extended feature names, component preservation, path redirect results, redirect/rewrite incompatibility. Nothing removed.

Method: documentation only; no commands were run.
