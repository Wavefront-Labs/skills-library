---
id: computing-software.web-development.bun.npmrc-config
name: npmrc-config
category: computing-software
field: web-development
product: bun
tags: [npmrc, registry-auth-token, env-expansion, ca-certificates]
level: advanced
status: docs-checked
description: "Use .npmrc with Bun: load order versus bunfig.toml, supported keys, environment variable expansion, credential matching, boolean parsing and CA settings."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/npmrc.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Load order, later overriding earlier: `~/.npmrc`, project `./.npmrc`, `bunfig.toml`, `BUN_CONFIG_REGISTRY`/`NPM_CONFIG_REGISTRY` and token variables, then CLI flags like `--registry`.

```ini
registry=http://localhost:4873/
@myorg:registry=http://localhost:4873/
//localhost:4873/:_authToken=${NPM_TOKEN}
omit[]=dev
```

Supported keys include `registry`, `@scope:registry`, `//host/path/:_authToken|username|_password|_auth`, `save-exact`, `ignore-scripts`, `dry-run`, `cache`, `ca`/`cafile`, `omit`/`include`, `install-strategy`/`node-linker`, and hoist settings for the isolated linker.

Gotchas:
- `${NAME}` stays literal if unset; `${NAME?}` becomes empty.
- An unquoted value ends at the first `;` or `#`; escape them as `\;`.
- Only `false`, `null`, `undefined` and `0` turn a boolean off. `ignore-scripts=` (empty) turns it ON.
- If both `ca` and `cafile` are set, only `cafile` is used. `include` overrides `omit`.
- Credentials are never sent to another host; they go only to http and https URLs.
- Credentials set next to the registry URL (bunfig token, `BUN_CONFIG_TOKEN`) win over `.npmrc` lines.
- Auto-install reads only registry, scope and credential settings.

## Checked

2026-11-04. Confirmed against bun docs pm/npmrc.mdx: load order, listed keys, environment expansion forms, unquoted ; and # handling, boolean parsing (empty value turns on), ca and cafile precedence, include over omit, credential matching and http/https-only rule, auto-install scope.

Method: documentation only; no commands were run.
