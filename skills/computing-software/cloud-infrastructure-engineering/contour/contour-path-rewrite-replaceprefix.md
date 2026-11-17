---
id: computing-software.cloud-infrastructure-engineering.contour.contour-path-rewrite-replaceprefix
name: contour-path-rewrite-replaceprefix
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [pathrewritepolicy, replaceprefix, path-rewriting, httpproxy]
level: practitioner
status: docs-checked
description: "HTTPProxy path rewriting with pathRewritePolicy.replacePrefix: replacement semantics, multiple entries disambiguated by prefix for included proxies."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-rewriting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy path rewriting

`pathRewritePolicy` rewrites the request path after the routing decision; it never changes the destination.

```yaml
routes:
- conditions:
  - prefix: /v1/api
  services: [{name: s1, port: 80}]
  pathRewritePolicy:
    replacePrefix:
    - prefix: /v1/api
      replacement: /app/api/v1
    - prefix: /
      replacement: /app
```

Semantics:
- `replacement` substitutes the matched path prefix; if the request path is longer than the matched prefix, the remainder is kept (`/v1/api/users` becomes `/app/api/v1/users`).
- `replacePrefix` is an array. With one entry and no `prefix` field, the replacement applies to every prefix match on the route.
- With several entries, `prefix` disambiguates: an entry applies only to routes whose prefix condition matches it exactly.
- Multiple entries are mainly useful when one HTTPProxy is included into several parent documents.

## Checked

2026-11-08: read the Contour docs config/request-rewriting (Path Rewriting section). Confirmed: rewriting after the routing decision, never changing the destination, replacePrefix and replacement, the unchanged remainder, array semantics, prefix disambiguation by exactly matching prefix condition, and the included-proxy use case. Removed: the cookie-rewriting advice and the prefix concatenation remark.

Method: documentation only; no commands were run.
