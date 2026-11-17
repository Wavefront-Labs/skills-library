---
id: computing-software.data-engineering.databricks.bundle-templates
name: bundle-templates
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, bundle-templates, asset-bundles, bundle-init, project-scaffolding]
level: advanced
status: docs-checked
description: "Scaffold Databricks Asset Bundles from built-in templates and write custom org templates: template schema, Go templating, helper functions and distribution via git."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/bundles/templates
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bundle templates

**Goal:** every new data project starts with the same structure, CI, targets and conventions.

## Built-in templates
```bash
databricks bundle init                      # interactive: default-python, default-sql, dbt-sql, mlops-stacks, ...
databricks bundle init default-python --config-file answers.json   # non-interactive
```

## Custom template layout
```
my-template/
  databricks_template_schema.json
  template/
    {{.project_name}}/
      databricks.yml.tmpl
      src/{{.project_name}}/__init__.py
      resources/{{.project_name}}_job.yml.tmpl
```
```json
{
  "properties": {
    "project_name": {"type": "string", "description": "Project name", "order": 1,
                     "pattern": "^[a-z0-9_]+$", "pattern_match_failure_message": "lowercase, digits, underscores"},
    "use_serverless": {"type": "string", "enum": ["yes", "no"], "default": "yes", "order": 2}
  },
  "success_message": "Created {{.project_name}}."
}
```
`.tmpl` files are rendered with Go templates and the suffix is dropped:
```yaml
bundle:
  name: {{.project_name}}
workspace:
  host: {{workspace_host}}
{{- if eq .use_serverless "yes"}}
# serverless by default
{{- end}}
```
Helpers include `{{workspace_host}}`, `{{user_name}}`, `{{short_name}}`, `{{uuid}}`.

## Use it
```bash
databricks bundle init https://github.com/<org>/databricks-templates --template-dir python-job
databricks bundle init ./my-template
```

## Practices
- Bake in: targets dev/staging/prod with `mode: development`/`production`, run-as service principal, CI workflow, tests folder, cluster policy references.
- Version the template repo; projects record the template version in a file for later upgrades.
- Files to skip conditionally: `{{skip "path"}}` in templates.

## Verify
`databricks bundle init` with answers file produces a project where `databricks bundle validate -t dev` passes.

## Checked
2026-10-28 Confirmed on the Databricks bundle templates page: `databricks bundle init` with `--config-file` and `--template-dir`, built-in templates (default-python, default-sql, dbt-sql, mlops-stacks), `databricks_template_schema.json` with `properties`, `pattern_match_failure_message`, `success_message`, `.tmpl` rendering, helpers `workspace_host`, `user_name`, `short_name`, `uuid`, and `skip`. The template folder names and property names such as `use_serverless` are examples. Replaced the example template URL (it returned 404) with a placeholder.
Method: documentation only; no commands were run.
