---
id: computing-software.devops-ci-cd.backstage.catalog-rules
name: catalog-rules
category: computing-software
field: devops-ci-cd
product: backstage
tags: [catalog-rules, allowed-kinds, location-rules, backstage]
level: advanced
status: docs-checked
description: "Restrict which entity kinds each location may add using catalog.rules and per-location rules."
sources:
  - https://backstage.io/docs/features/software-catalog/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default the catalog only ingests entities of kind Component, API and Location. Control this with `catalog.rules`.

```yaml
catalog:
  rules:
    - allow: [Component, API, Location, Template]
  locations:
    - type: url
      target: https://github.com/example-org/org-data/blob/main/groups.yaml
      rules:
        - allow: [Group]
```

- `catalog.rules` is a list of `allow` entries naming kinds. If the key is present it replaces the default rules entirely, so list every kind you want.
- A per-location `rules` list is added to statically configured locations, for example to let one file define Groups.
- The page also shows `rules: []`.

Rules are added either under a separate `catalog.rules` key or on statically configured locations.

## Checked

2026-11-03. Confirmed on the catalog configuration page: the default allowed kinds (Component, API, Location), rules added under `catalog.rules` or on static locations, the example with `allow: [Component, API, Location, Template]` and a per-location `allow: [Group]`, and that a present `catalog.rules` key replaces the default value. Removed: the claim that `rules: []` allows nothing (the page shows the form without explaining it), the log-reason sentence and the trust advice.

Method: documentation only; no commands were run.
