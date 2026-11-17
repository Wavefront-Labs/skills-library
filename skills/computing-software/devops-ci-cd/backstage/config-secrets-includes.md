---
id: computing-software.devops-ci-cd.backstage.config-secrets-includes
name: config-secrets-includes
category: computing-software
field: devops-ci-cd
product: backstage
tags: [env-substitution, file-include, config-secrets, backstage]
level: practitioner
status: docs-checked
description: "Keep secrets out of app-config with ${ENV}, $env, $file and $include substitutions."
sources:
  - https://backstage.io/docs/conf/writing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Config values can be loaded from other sources so secrets stay out of version control.

```yaml
backend:
  database:
    connection:
      password: ${POSTGRES_PASSWORD}
auth:
  providers:
    github:
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret:
          $env: AUTH_GITHUB_CLIENT_SECRET
techdocs:
  publisher:
    googleGcs:
      credentials:
        $file: ./my-secret.txt
integrations:
  github:
    - host: github.com
      token:
        $include: ./my-secrets.json#deployment.key
```

- `${NAME}` interpolates an environment variable inside a string.
- `$env` reads an environment variable as the whole value.
- `$file` reads the contents of a file, relative to the config file itself.
- `$include` loads a value from an external JSON or YAML file, with an optional `#path` into it.

In the provided project setup `app-config.local.yaml` is git-ignored, which makes it a good place for local overrides and development secrets. All includes are loaded at startup, so later changes to files or environment variables are not seen at runtime.

`${VAR:-default}` supplies a fallback when the variable is unset or empty, and `$${...}` escapes the syntax so it resolves to a literal `${...}`.

## Checked

2026-11-03. Confirmed against the Backstage Writing Configuration page: `${NAME}` substitution, `$env`, `$file` (relative to the config file), `$include` with `#path`, startup loading, default and escape syntax. Removed: the secret-manager advice and the claim that a missing variable invalidates the config.

Method: documentation only; no commands were run.
