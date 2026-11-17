---
id: computing-software.devops-ci-cd.atlantis.atlantis-custom-workflows
name: atlantis-custom-workflows
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [workflows, run-step, env-step, multienv, extra-args, planfile, terragrunt]
level: advanced
status: docs-checked
description: "Build Atlantis custom workflows with plan, apply, import and state_rm stages and run, env and multienv steps."
sources: ["https://www.runatlantis.io/docs/custom-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis custom workflows

Custom workflows override the commands Atlantis runs. Define them in server-side config or repo `atlantis.yaml` (repos may select a server workflow only with `allowed_overrides: [workflow]`, and define their own only with `allow_custom_workflows: true`).

Stages and defaults: `plan` (`init`, `plan`), `apply` (`apply`), `import` (`init`, `import`), `state_rm` (`init`, `state_rm`). An empty `steps` list runs nothing.

Step types:
- Built-in string (`init`, `plan`, `apply`, `import`, `state_rm`), optionally with `extra_args`. Each argument is passed as-is: no shell parsing, so `;`, `&&`, `|` and redirects do nothing (variables like `$WORKSPACE` still expand).
- `run`: compact `- run: cmd` or full form with `command`, `shell` (default `sh`), `shellArgs` (default `-c`), and `output` (`show`, `hide`, `strip_refreshing`, or `filter_regex`).
- `env`: set `name` with a fixed `value` or a `command` whose output is the value, for all later steps.
- `multienv`: a command printing `A=1,B=2` which adds several variables; failure stops the workflow.

Useful variables: `WORKSPACE`, `DIR`, `PLANFILE`, `SHOWFILE`, `PROJECT_NAME`, `REPO_REL_DIR`, `PULL_NUM`, `HEAD_BRANCH_NAME`, `COMMENT_ARGS`, `ATLANTIS_TERRAFORM_VERSION`.

Caveats: a plan written by the built-in `plan` step must be at `$PLANFILE`; Atlantis hashes it after the plan stage and refuses to apply a changed file (including changes by pre-workflow hooks). A non-zero exit stops the workflow. Redirect output when starting background processes. Changing backend config needs `rm -rf .terraform` first.

```yaml
workflows:
  staging:
    plan:
      steps:
      - run: rm -rf .terraform
      - init:
          extra_args: [-backend-config=staging.backend.tfvars]
      - plan:
          extra_args: [-var-file=staging.tfvars]
```

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Custom Workflows (reference and plan file integrity). Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
