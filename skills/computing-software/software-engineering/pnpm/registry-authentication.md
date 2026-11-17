---
id: computing-software.software-engineering.pnpm.registry-authentication
name: registry-authentication
category: computing-software
field: software-engineering
product: pnpm
tags: [npmrc, auth-ini, auth-token, scoped-auth-token, token-helper, pnpm-login, auth-config-env, npmrc-env-expansion]
level: practitioner
status: docs-checked
description: "Configure pnpm registry credentials: .npmrc and auth.ini lookup order, _authToken and scoped tokens, tokenHelper, the _auth config.yaml map, CI tokens and env-var limits."
sources:
  - https://pnpm.io/npmrc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auth settings hold secrets; keep them out of the repository. Locally run `pnpm login` (writes `<pnpm config>/auth.ini`). In CI:

```sh
export pnpm_config__auth='{"https://registry.npmjs.org":{"@":{"authToken":"${NPM_TOKEN}"}}}'
```

INI lookup order, first file wins per key: `<workspace root>/.npmrc` (gitignore it), `<pnpm config>/auth.ini`, `~/.npmrc` (or the file named by `npmrcAuthFile`).

Keys:
- `//registry.npmjs.org/:_authToken=...`; scope-specific form `//npm.pkg.github.com/:@org-a:_authToken=...` with an unscoped fallback.
- `tokenHelper`: absolute path to a program, no arguments, output sent as `Authorization: Bearer`. Read only from user-level files.
- `_auth` map (global `config.yaml` or `pnpm_config__auth` JSON, never workspace or `.npmrc`): `"@"` is the registry-wide token, `"@org"` a scope, only `authToken`. Entries also route packages; `--registry` wins, then env entries, then global file only where no registry setting applies. `pnpm login` writes `auth.ini` since v12.16.0.

Env-var expansion `${NAME}` works in user-level files only. In the project `.npmrc`, registry and proxy URLs, `//` keys and credentials are ignored with a warning, because a repository could otherwise exfiltrate CI tokens (GHSA-3qhv-2rgh-x77r). Alternatives: `env "pnpm_config_//registry.npmjs.org/:_authToken=$NPM_TOKEN" pnpm install`, `pnpm config set //registry.npmjs.org/:_authToken "$NPM_TOKEN"`, or `PNPM_CONFIG_NPMRC_AUTH_FILE=.npmrc` for fully trusted repositories only.

## Checked

2026-11-04. Confirmed the auth file lookup order, _authToken forms, tokenHelper rules, the _auth map and its routing priority, the v12.16.0 login change, env-var expansion limits and the alternatives against pnpm.io/npmrc. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
