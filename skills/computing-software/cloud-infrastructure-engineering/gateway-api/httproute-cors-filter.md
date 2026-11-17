---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-cors-filter
name: httproute-cors-filter
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, cors, allowcredentials, alloworigins, httproutecors, filter]
level: practitioner
status: docs-checked
description: "Configure the HTTPRoute CORS filter: allowOrigins with wildcards, allowCredentials, allowMethods, allowHeaders, exposeHeaders and maxAge (Standard since v1.5.0, extended)."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `CORS` filter in an `HTTPRouteRule` applies a Cross-Origin Resource Sharing policy. Extended feature `HTTPRouteCORS`; Standard channel since v1.5.0.

Origins:

- A specific origin: `https://app.example`.
- A single wildcard `"*"` allows any origin.
- Semi-specified origins put the wildcard after the scheme at the start of the hostname: `https://*.bar.com`.

Other fields:

- `allowCredentials`: whether the browser may include credentials (cookies, HTTP authentication).
- `allowMethods`: allowed HTTP methods.
- `allowHeaders`: allowed request headers.
- `exposeHeaders`: response headers exposed to the client.
- `maxAge`: seconds the browser may cache the preflight response.

For `allowMethods`, `allowHeaders` and `exposeHeaders` a single `"*"` can replace a list.

The guide's example manifests are included from separate files (such as `httproute-all-fields-set`) that the page text does not show, so look at them in the repository for exact value formats.

## Checked

2026-11-04. Confirmed on the Gateway API CORS guide (http-cors.md): extended feature name, Standard channel since v1.5.0, origin forms, allowCredentials, allowMethods/allowHeaders/exposeHeaders/maxAge, wildcard for the list fields. Removed the YAML sketch (values not on the page), the wildcard-with-credentials remark and the Ingress-NGINX migration note.

Method: documentation only; no commands were run.
