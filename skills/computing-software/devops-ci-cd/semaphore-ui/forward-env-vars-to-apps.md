---
id: computing-software.devops-ci-cd.semaphore-ui.forward-env-vars-to-apps
name: forward-env-vars-to-apps
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [env-vars, forwarded-env-vars, ansible, terraform, semaphore-ui]
level: practitioner
status: docs-checked
description: "Pass static or forwarded environment variables from the Semaphore server to Ansible, Terraform and git processes."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/env-vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pass environment variables to app processes

Goal: make variables from the server environment visible to Ansible, Terraform, scripts and git.

Semaphore does not hand its whole environment to the processes it starts. Two options control it:

- `env_vars` / `SEMAPHORE_ENV_VARS`: static key-value pairs set for app processes.
- `forwarded_env_vars` / `SEMAPHORE_FORWARDED_ENV_VARS`: names of variables copied from the server's own environment.

```json
{
  "env_vars": {
    "HTTP_PROXY": "http://proxy.internal:3128",
    "ANSIBLE_STDOUT_CALLBACK": "yaml"
  },
  "forwarded_env_vars": [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS"
  ]
}
```

Equivalent environment variables take JSON: `SEMAPHORE_ENV_VARS='{"HTTP_PROXY":"..."}'` and `SEMAPHORE_FORWARDED_ENV_VARS='["AWS_ACCESS_KEY_ID"]'`.

Rules:
- Forwarding is explicit; only listed names are inherited.
- The same list applies to the `git` processes that clone and update repositories.
- Supply secrets via Docker or Kubernetes secrets and forward them, rather than writing values into the config.

Per-project secrets belong in Variable Groups (secrets tab), not here.

Verify: run a Bash template that prints the variable name list with `env | sort` and confirm only the expected names appear.

## Checked

2026-11-04: checked against the environment variables page and the configuration reference. Every claim is stated there.

Method: documentation only; no commands were run.
