---
id: computing-software.web-development.bun.scoped-registries
name: scoped-registries
category: computing-software
field: web-development
product: bun
tags: [scoped-registry, install-scopes, private-registry, registry-token]
level: practitioner
status: docs-checked
description: "Point Bun at a private or scoped npm registry in bunfig.toml with tokens or username and password, environment variable references and URL encoding rules."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/scopes-registries.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```toml
[install]
registry = { url = "https://registry.npmjs.org", token = "123456" }

[install.scopes]
"@myorg1" = "https://username:password@registry.myorg.com/"
"@myorg2" = { username = "myusername", password = "$NPM_PASS", url = "https://registry.myorg.com/" }
"@myorg3" = { token = "$npm_token", url = "https://registry.myorg.com/" }
```

Rules:
- The default registry is `registry.npmjs.org`. A global registry goes under `[install]`; per-organization registries under `[install.scopes]`.
- Each scope takes a URL string or a table with `url` plus `username`/`password` or `token`.
- A `$` prefix references an environment variable. Bun also reads `.npmrc`.

Gotchas:
- An unset env var warns and is treated as empty; Bun then falls back to credentials `.npmrc` has for that registry.
- Credentials embedded in a URL must be percent-encoded (`p@ss` becomes `p%40ss`); Bun decodes them.
- The `username`, `password` and `token` fields are sent exactly as written, so do not percent-encode them.

## Checked

2026-11-04. Confirmed against bun docs pm/scopes-registries.mdx: default registry, [install] and [install.scopes] forms, environment variable references, unset-variable behaviour with .npmrc fallback, percent-encoding of URL credentials, fields sent as written.

Method: documentation only; no commands were run.
