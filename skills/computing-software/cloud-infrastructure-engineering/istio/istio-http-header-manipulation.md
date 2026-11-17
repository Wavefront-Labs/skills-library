---
id: computing-software.cloud-infrastructure-engineering.istio.istio-http-header-manipulation
name: istio-http-header-manipulation
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, header-manipulation, rewrite, corspolicy]
level: practitioner
status: docs-checked
description: "Manipulate request and response headers and rewrite paths in VirtualService routes, including redirect and CORS policy."
sources: ["https://istio.io/latest/docs/reference/config/networking/virtual-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTP routes support header edits (`headers`), URI/authority `rewrite`, `redirect` and `corsPolicy`.

```yaml
http:
- match: [{uri: {prefix: /api/v1}}]
  rewrite: {uri: /}
  headers:
    request: {set: {x-env: prod}, remove: [x-debug]}
    response: {add: {x-served-by: mesh}}
  route: [{destination: {host: api}}]
```

Semantics from the reference: `set` overwrites the named headers, `add` appends (a comma-separated list), `remove` deletes them. Header rules can be given for the whole route or for one route destination (the reference removes a response header only for the v1 subset). `rewrite.uri` replaces the matched prefix when the match was a prefix match; `rewrite.authority` rewrites the Host/Authority header; rewrite is applied before forwarding.

Gotchas: `rewrite` cannot be used with `redirect`. A rule returns a `directResponse`, a `redirect` or forwards (default); `redirect` sends an HTTP 301 to another URI or authority. On a redirect, `uri` replaces the entire path, whereas `prefixRewrite` replaces only the matched prefix (the reference warns that prefix `/foo` rewritten to `/` turns `/foo/baz` into `//baz`; match `/foo/` to get `/baz`). Header keys in a `match` must be lowercase with hyphens.

## Checked

2026-11-03. Confirmed against the VirtualService reference: Headers `set`/`add`/`remove`, HTTPRewrite `uri`/`authority`, HTTPRedirect and its `uri`/`prefixRewrite` semantics, direct response, match header key rules. Removed: the claim that `/api/v1/x` maps to `/x` (the reference only documents the `//baz` caveat for redirects), the unconfirmed `Authorization` and ordering remarks, the curl verify step and the commenting advice.
Method: documentation only; no commands were run.
