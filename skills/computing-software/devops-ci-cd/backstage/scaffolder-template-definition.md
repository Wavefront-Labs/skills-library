---
id: computing-software.devops-ci-cd.backstage.scaffolder-template-definition
name: scaffolder-template-definition
category: computing-software
field: devops-ci-cd
product: backstage
tags: [software-templates, template-yaml, scaffolder, backstage]
level: practitioner
status: docs-checked
description: "Structure a software template with apiVersion scaffolder.backstage.io/v1beta3, parameters, steps and output."
sources:
  - https://backstage.io/docs/features/software-templates/writing-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A template is a catalog entity of `kind: Template` with `apiVersion: scaffolder.backstage.io/v1beta3`. The `spec` holds an owner, a type, input `parameters`, a list of `steps`, and an `output` block.

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: service-template
  title: New service
  description: Create a service repository
spec:
  owner: platform-team
  type: service
  parameters:
    - title: Details
      required: [name]
      properties:
        name:
          title: Name
          type: string
  steps:
    - id: fetchBase
      name: Fetch Base
      action: fetch:template
      input:
        url: ./template
        values:
          name: ${{ parameters.name }}
  output:
    links:
      - title: Open in catalog
        icon: catalog
        entityRef: ${{ steps['register'].output.entityRef }}
```

- `parameters` render as the form; each item is one step in the wizard.
- `steps` run in order on the scaffolder backend.
- `output.links` appear after the run, and can point at repository URLs or entity references from step outputs.

Values flow through `${{ ... }}` expressions: `parameters.*` for input, `steps.<id>.output.*` for earlier results.

## Checked

2026-11-03. Confirmed against the Backstage Writing Templates page: `apiVersion: scaffolder.backstage.io/v1beta3`, `kind: Template`, `spec` fields, parameters as form steps, `output.links`, expression syntax. Removed: the `backstage.io/time-saved` annotation and the `catalog.rules` advice (not in the page).

Method: documentation only; no commands were run.
