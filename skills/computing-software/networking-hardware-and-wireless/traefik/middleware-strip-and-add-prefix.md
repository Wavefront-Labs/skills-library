---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-strip-and-add-prefix
name: middleware-strip-and-add-prefix
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, stripprefix, stripprefixregex, addprefix, x-forwarded-prefix, middleware]
level: practitioner
status: docs-checked
description: "Remove or add URL path prefixes before a request reaches the backend with stripPrefix, stripPrefixRegex and addPrefix."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/stripprefix.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/stripprefixregex.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/addprefix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware strip and add prefix
`stripPrefix` takes `prefixes` (a list), strips the matching path prefix and stores it in the `X-Forwarded-Prefix` header; use it when the backend listens on `/` but is exposed under a prefix. `stripPrefixRegex` takes `regex` (a list) to match the prefix by pattern and also stores it in `X-Forwarded-Prefix`. `addPrefix` takes a required `prefix`, the string added before the current path, which should include a leading slash.

```yaml
http:
  middlewares:
    strip-api:
      stripPrefix:
        prefixes:
          - "/foobar"
          - "/fiibar"
    strip-regex:
      stripPrefixRegex:
        regex:
          - "/foo/[a-z0-9]+/[0-9]+/"
    add-foo:
      addPrefix:
        prefix: "/foo"
```
A backend serving assets can use `X-Forwarded-Prefix` to build relative URLs. For `stripPrefixRegex`, `/products` also matches `/products/shoes`. In YAML, escaped characters in a regex must be escaped twice (`example\\.com`).

## Checked
2026-11-03. Confirmed against the Traefik stripPrefix, stripPrefixRegex and addPrefix reference pages (docs/content/reference/routing-configuration/http/middlewares/stripprefix.md, stripprefixregex.md, addprefix.md): options, header, leading-slash note, regex list. Removed: "stripping the whole path leaves /", the chain-order advice, the PathPrefix rule advice, and the Verify step.
Method: documentation only; no commands were run.
