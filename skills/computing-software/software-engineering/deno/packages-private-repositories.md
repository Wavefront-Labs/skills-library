---
id: computing-software.software-engineering.deno.packages-private-repositories
name: packages-private-repositories
category: computing-software
field: software-engineering
product: deno
tags: [packages, private-repositories, deno-auth-tokens, bearer-token, basic-auth, github]
level: practitioner
status: docs-checked
description: "Load remote modules from private hosts with DENO_AUTH_TOKENS: bearer and basic formats, multiple tokens, GitHub raw access and debugging 404s."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/private_repositories.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno reads `DENO_AUTH_TOKENS` for tokens to send when fetching remote modules. Separate tokens with `;`. Each is either a bearer token `{token}@{hostname[:port]}` or basic auth `{username}:{password}@{hostname[:port]}`.

```sh
DENO_AUTH_TOKENS=a1b2c3d4e5f6@deno.land
DENO_AUTH_TOKENS=username:password@deno.land
DENO_AUTH_TOKENS=a1b2c3d4e5f6@deno.land;f1e2d3c4b5a6@example.com:8080;username:password@deno.land
```

When the hostname of the remote module matches, Deno sets `Authorization` to `Bearer {token}` or `Basic {base64EncodedData}`.

GitHub private repos: issue a personal access token with the `repo` scope (Settings -> Developer settings -> Personal access tokens) and scope it to `raw.githubusercontent.com`:

```sh
DENO_AUTH_TOKENS=a1b2c3d4e5f6@raw.githubusercontent.com
```

GitHub answers a bad token or missing access with `404 Not Found`, not unauthorized, so a "not found" error means check the variable and the token settings.

`deno run -L debug` prints how many tokens were parsed and errors on malformed ones, without revealing token details.

Private npm registries and `.npmrc` are covered in the npm support (Node) docs.

## Checked

2026-11-04. Confirmed against the Deno Private repositories page: `DENO_AUTH_TOKENS` formats and separator, Authorization header forms, GitHub `repo` scope and raw.githubusercontent.com host, 404 behaviour, `deno run -L debug`. Nothing removed.

Method: documentation only; no commands were run.
