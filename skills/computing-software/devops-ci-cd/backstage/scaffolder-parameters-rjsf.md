---
id: computing-software.devops-ci-cd.backstage.scaffolder-parameters-rjsf
name: scaffolder-parameters-rjsf
category: computing-software
field: devops-ci-cd
product: backstage
tags: [template-parameters, json-schema, ui-field, backstage]
level: practitioner
status: docs-checked
description: "Define template input forms with JSON Schema, ui keywords and built-in pickers such as OwnerPicker and RepoUrlPicker."
sources:
  - https://backstage.io/docs/features/software-templates/writing-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each item under `spec.parameters` is a JSON Schema form step rendered with react-jsonschema-form. Backstage merges the library's `uiSchema` into the schema as `ui:*` properties.

```yaml
parameters:
  - title: Fill in some steps
    required: [name]
    properties:
      name:
        title: Name
        type: string
        description: Unique name of the component
        ui:autofocus: true
        ui:options:
          rows: 5
      owner:
        title: Owner
        type: string
        ui:field: OwnerPicker
        ui:options:
          catalogFilter:
            kind: Group
  - title: Choose a location
    required: [repoUrl]
    properties:
      repoUrl:
        title: Repository Location
        type: string
        ui:field: RepoUrlPicker
        ui:options:
          allowedHosts:
            - github.com
```

- Split input over several parameter items to get a multi-step wizard.
- `ui:field` selects a custom or built-in field such as `OwnerPicker`, `EntityPicker` or `RepoUrlPicker`.
- `RepoUrlPicker` with `allowedHosts` restricts where a repository may be created (hosts listed in `integrations`); `allowedOwners` and `allowedRepos` narrow it further.
- Standard JSON Schema keywords such as `required`, `enum`, `pattern`, `minLength` and `default` give validation.

## Checked

2026-11-03. Confirmed against the Backstage Writing Templates page: react-jsonschema-form with merged `ui:*` properties, multi-step parameters, `OwnerPicker` with `catalogFilter`, `RepoUrlPicker` options, `minLength`. Removed: the playground advice.

Method: documentation only; no commands were run.
