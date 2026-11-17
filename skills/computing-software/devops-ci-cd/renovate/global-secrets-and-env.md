---
id: computing-software.devops-ci-cd.renovate.global-secrets-and-env
name: global-secrets-and-env
category: computing-software
field: devops-ci-cd
product: renovate
tags: [secrets, custom-env-variables, allowed-env, renovate]
level: advanced
status: docs-checked
description: "Handle secrets and child-process environment with secrets, customEnvVariables, allowedEnv and exposeAllEnv."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate controls which environment variables reach the tools it runs.

- `customEnvVariables` (global) sets variables applied after all others, so it can override defaults. Do not put secrets in it directly, as they may be logged. Define them in `secrets` first so logs redact them, then reference the secret.
- `allowedEnv` lets administrators permit repository config to set chosen variables through the `env` option. Only names matching the list (exact names, globs or regexes) are accepted. It constrains repositories and the presets they extend, not the administrator.
- `exposeAllEnv` passes all environment variables to package managers. Advanced use only: a malicious script could enumerate and leak secrets, so set it only for repositories you have reviewed and trust. Alternatively hand-pick variables with `customEnvVariables`.
- `secrets` holds secret name/value pairs set by the administrator, available for templating in repository configs as `{{ secrets.NAME }}`.

```json
{
  "secrets": { "NPM_TOKEN": "<token>" },
  "customEnvVariables": { "NPM_AUTH": "{{ secrets.NPM_TOKEN }}" },
  "allowedEnv": ["GOPROXY"]
}
```

Repository `env`:

```json
{
  "env": { "GOPROXY": "https://proxy.example.com" }
}
```

By default Renovate passes only a limited set of environment variables to package managers. The repository `env` option applies only when Renovate runs package manager commands, and its values override those from `customEnvVariables` and `process.env`. `executionTimeout` is the default timeout in minutes for child processes (15 by default).

## Checked

2026-11-09: read the allowedEnv, customEnvVariables, exposeAllEnv, executionTimeout and secrets sections of https://docs.renovatebot.com/self-hosted-configuration/ and the env section of https://docs.renovatebot.com/configuration-options/. Removed the `["*"]` claim and the unsourced note about who can read process environment.

Method: documentation only; no commands were run.
