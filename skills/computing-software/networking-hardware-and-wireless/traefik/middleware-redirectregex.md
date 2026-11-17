---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-redirectregex
name: middleware-redirectregex
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, redirectregex, regex, redirect, replacement, middleware]
level: practitioner
status: docs-checked
description: "Redirect with regex capture groups using redirectRegex, noting the $1x versus ${1} pitfall and YAML escaping."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/redirectregex.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware redirectregex
`redirectRegex` redirects a request using regex matching and replacement. Options: `regex` (required; matches and captures elements of the request URL), `replacement` and `permanent` (default false).

```yaml
http:
  middlewares:
    test-redirectregex:
      redirectRegex:
        regex: "^http://localhost/(.*)"
        replacement: "http://mydomain/${1}"
        permanent: true
```
Gotchas: `$1x` is equivalent to `${1x}`, not `${1}x`, so always use the `${1}` syntax (see Go `Regexp.Expand`). In YAML, escaped characters in the regex must be escaped twice (`example\\.com`). In docker-compose labels all dollar signs must be doubled.

## Checked
2026-11-03. Confirmed against the Traefik redirectRegex reference page (docs/content/reference/routing-configuration/http/middlewares/redirectregex.md): options, defaults, `$1x` warning, YAML double escaping, label dollar-doubling. Removed: the `^https?://` www example (replaced by the docs example), the "Go regular expression syntax" claim beyond the Expand reference, and the curl Verify step.
Method: documentation only; no commands were run.
