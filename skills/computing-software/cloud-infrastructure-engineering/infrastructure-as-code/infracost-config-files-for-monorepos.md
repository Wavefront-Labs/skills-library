---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.infracost-config-files-for-monorepos
name: infracost-config-files-for-monorepos
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-cost, infracost-config, infracost, monorepo]
level: practitioner
status: docs-checked
description: "Write infracost.yml config files to estimate costs for many Terraform projects in a monorepo, with per-project vars files, usage files and a matchPaths template."
sources: ["https://www.infracost.io/docs/features/config_file/", "https://www.infracost.io/docs/features/usage_based_resources/", "https://www.infracost.io/docs/features/cli_commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Infracost config files for monorepos

Auto-detection works for simple repos; monorepos with environments and var files need an explicit config. Commit `infracost.yml` (static) or `infracost.yml.tmpl` (template) at the repo root and `infracost scan` picks it up.

```yaml
# infracost.yml
version: 0.1
projects:
  - path: stacks/network
    name: network-prod
    terraform_var_files: [../../env/prod.tfvars]
    usage_file: usage/network-prod.yml
  - path: stacks/app
    name: app-prod
    terraform_var_files: [../../env/prod.tfvars]
    terraform_vars:
      instance_count: 6
  - path: stacks/app
    name: app-staging
    terraform_var_files: [../../env/staging.tfvars]
    terraform_workspace: staging
```
Template form for many similar directories (`infracost.yml.tmpl`); the template is expanded against the directory tree on each run, so the rendered file need not be committed:
```
version: 0.1
projects:
{{- range $project := matchPaths "stacks/:stack/env/:env.tfvars" }}
  - path: stacks/{{ $project.stack }}
    name: {{ $project.stack }}-{{ $project.env }}
    terraform_var_files: [env/{{ $project.env }}.tfvars]
{{- end }}
```

## Tips
- Set `name` so project identity is stable in all outputs; it defaults to the code path, workspace or module.
- `terraform_workspace` only for multi-workspace repos; otherwise Terraform may error with "workspaces not supported".
- Usage files per project capture usage-based costs (requests, GB transferred); `usage_file` can also be set at the top level for all projects.
- Debug a template with `infracost scan --json --log-level=debug` and read the rendered project list.

## Gotchas
- `path` and `usage_file` are relative to the directory you run infracost from (normally the repo root); `terraform_var_files` are relative to the project `path`.
- The CI command set changed with the `infracost scan` CLI: check the current CLI commands page before copying older `breakdown`/`diff`/`comment` pipelines.

## Checked
2026-11-01. Confirmed against the Infracost config file page, usage-based-resources page and CLI commands page: `projects`, `path`, `name`, `terraform_var_files`, `terraform_vars`, `terraform_workspace`, `usage_file`, `version: 0.1`, `infracost.yml.tmpl`, `matchPaths`, relative-path rules, and `infracost scan` auto-discovery. Removed: the breakdown/diff/comment CI commands and flags, the env var tips (INFRACOST_PARALLELISM, Terraform Cloud token), the JSON-errors gotcha and the grep verify step, none of which appear in the pages read.
Method: documentation only; no commands were run.
