---
id: computing-software.devops-ci-cd.backstage.scaffolder-steps-and-outputs
name: scaffolder-steps-and-outputs
category: computing-software
field: devops-ci-cd
product: backstage
tags: [template-steps, fetch-template, step-outputs, backstage]
level: practitioner
status: docs-checked
description: "Chain scaffolder actions in steps, pass values with expressions, and publish links in the template output."
sources:
  - https://backstage.io/docs/features/software-templates/writing-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`spec.steps` is the ordered list of actions the backend runs. Each step needs an `id`, a `name`, an `action` and usually an `input`.

```yaml
steps:
  - id: fetchBase
    name: Fetch Base
    action: fetch:template
    input:
      url: ./template
      values:
        name: ${{ parameters.name }}
  - id: publish
    name: Publish
    action: publish:github
    input:
      repoUrl: ${{ parameters.repoUrl }}
      defaultBranch: main
  - id: register
    name: Register
    action: catalog:register
    input:
      repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
      catalogInfoPath: '/catalog-info.yaml'
output:
  links:
    - title: Repository
      url: ${{ steps['publish'].output.remoteUrl }}
    - title: Open in catalog
      icon: catalog
      entityRef: ${{ steps['register'].output.entityRef }}
```

- `fetch:template` is the builtin templating action that makes `values` available to the skeleton; `fetch:plain` also fetches content.
- `publish:github` creates the repository, and `catalog:register` adds the new `catalog-info.yaml` to the catalog.
- Outputs of a step are read with `steps.<id>.output.<key>`.
- `output` is saved along with the job for use in the frontend; `links` entries take a `title` and either `url` or `entityRef`, with an optional `icon`.
- A step can have an `if` condition and an `each` iterable.

## Checked

2026-11-03. Confirmed against the Backstage Writing Templates page: step fields, the fetch/publish/register example, `steps.<id>.output.<key>`, output links. Removed: the claim that `fetch:plain` does not template and the skeleton advice.

Method: documentation only; no commands were run.
