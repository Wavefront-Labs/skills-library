---
id: computing-software.data-engineering.prefect.job-variables-overrides
name: job-variables-overrides
category: computing-software
field: data-engineering
product: prefect
tags: [job-variables, env, work-pool, overrides, deployment]
level: practitioner
status: docs-checked
description: "Override Prefect work pool job variables per deployment in prefect.yaml or deploy(), and per flow run through the CLI, UI, Terraform or automations."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployments/customize-job-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change infrastructure settings such as `env` without a new pool.

Job variables are infrastructure settings on a work pool. Override them per deployment or per flow run.

Deployment, `prefect.yaml`:

```yaml
work_pool:
  name: local
  job_variables:
    env:
      EXECUTION_ENVIRONMENT: staging
```
Then `prefect deploy -n demo-deployment`. Template local environment variables with `"{{ $ENV_VAR_NAME }}"`.

Deployment, Python:

```python
my_flow.deploy(..., job_variables={"env": {"EXECUTION_ENVIRONMENT": "staging"}})
```

Flow run:
- UI: the custom run form accepts a dictionary of variables.
- CLI: `-jv` or `--job-variable`.
- Terraform: the page has a Terraform section, but no details are confirmed here.
- Automations: actions can set them, including Jinja-rendered values.

```bash
prefect deployment run --id "<deployment-id>" --job-variable MY_NEW_ENV_VAR=42
```

The page's examples use `env`. It does not list the other available keys.

## Checked

2026-11-09. Confirmed: Customize job variables page (customize-job-variables): prefect.yaml and deploy() overrides, {{ $ENV_VAR_NAME }} templating, UI custom run form, -jv/--job-variable, automations. Removed: the Terraform resource name and the generic list of keys, which the page does not state.

Method: documentation only; no commands were run.
