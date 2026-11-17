---
id: computing-software.cloud-infrastructure-engineering.vector.environment-variable-interpolation
name: environment-variable-interpolation
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [environment-variables, interpolation, security, defaults, envsubst, config, vector]
level: advanced
status: docs-checked
description: "Enable and use env var interpolation safely, knowing it is off by default and what it can leak."
sources:
  - https://vector.dev/docs/reference/environment_variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment variable interpolation is disabled by default (the default changed in v0.57.0). Enable it with `--dangerously-allow-env-var-interpolation` or `VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`. Only do so if you control every variable the process can see.

Syntax:

```yaml
.host = "${HOSTNAME}"                      # or $HOSTNAME
environment: "${ENV:-development}"         # default if unset or empty
tenant: "${TENANT:?tenant must be supplied}"  # exit if unset or empty
other: "${VAR-default}"                    # default only if unset
other2: "${VAR?err}"                       # exit only if unset
```

Escape with `$$`: `$${HOSTNAME}` is literal.

Risks the docs call out:

- Anyone who can read `/proc/<PID>/environ` can read the variables, regardless of interpolation. Prefer the secrets backend (see secrets-backends-exec-file-directory) for sensitive data.
- If an attacker controls a variable such as `LOG_PATH`, they can point a `file` source at a sensitive file and forward its contents.
- Vector rejects values containing newlines, but does not escape quotes, braces or brackets; these are substituted before parsing and can change structure.

For multi-line blocks, preprocess with `envsubst`, then inspect the result. envsubst expands only plain `$VAR` and `${VAR}`, not `:-` or `:?` forms.

Verify with `vector validate` on the rendered config.

## Checked

2026-11-03. Read reference/environment_variables. Confirmed: disabled by default since v0.57.0, the enabling flag and variable, all five default and required syntaxes, `$$` escaping, the `/proc/<PID>/environ` risk, the `LOG_PATH` example, newline rejection, unescaped structural characters, and the envsubst advice. Nothing removed.

Method: documentation only; no commands were run.
