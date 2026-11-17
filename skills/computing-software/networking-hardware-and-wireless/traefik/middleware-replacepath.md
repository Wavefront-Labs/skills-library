---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-replacepath
name: middleware-replacepath
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, replacepath, replacepathregex, rewrite, original-path, middleware]
level: practitioner
status: docs-checked
description: "Rewrite the request path with replacePath or replacePathRegex; the original path is stored in the X-Replaced-Path header."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/replacepath.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/replacepathregex.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware replacepath
`replacePath` replaces the actual path with the one in its `path` option. `replacePathRegex` replaces the matching path using `regex` (required) and `replacement` (capture variables allowed). Both store the original path in the `X-Replaced-Path` header.

```yaml
http:
  middlewares:
    test-replacepath:
      replacePath:
        path: "/foo"
    test-replacepathregex:
      replacePathRegex:
        regex: "^/foo/(.*)"
        replacement: "/bar/${1}"
```
Gotchas: `$1x` is equivalent to `${1x}`, not `${1}x`, so use the `${1}` syntax. In YAML, escaped characters in the regex must be escaped twice (`example\\.com`).

## Checked
2026-11-03. Confirmed against the Traefik replacePath and replacePathRegex reference pages (docs/content/reference/routing-configuration/http/middlewares/replacepath.md and replacepathregex.md): options, X-Replaced-Path header, `${1}` warning, YAML escaping. Removed: the "confirm against your version" hedge, the incoherent "query-independent path" gotcha, the router-matching-order remark and the Verify step.
Method: documentation only; no commands were run.
