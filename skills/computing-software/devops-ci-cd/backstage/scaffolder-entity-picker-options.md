---
id: computing-software.devops-ci-cd.backstage.scaffolder-entity-picker-options
name: scaffolder-entity-picker-options
category: computing-software
field: devops-ci-cd
product: backstage
tags: [entity-picker, catalog-filter, ui-options, backstage]
level: practitioner
status: docs-checked
description: "Configure EntityPicker and MultiEntityPicker fields with catalogFilter, allowedKinds, defaults and arbitrary values."
sources:
  - https://backstage.io/docs/features/software-templates/ui-options-examples
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`EntityPicker` lets a user choose a catalog entity in a template form. `MultiEntityPicker` allows several. Configure them with `ui:options`.

```yaml
parameters:
  - title: Ownership
    properties:
      owner:
        title: Owner
        type: string
        ui:field: EntityPicker
        ui:options:
          catalogFilter:
            - kind: [Group, User]
          defaultKind: Group
          defaultNamespace: default
          allowArbitraryValues: false
```

Documented options:

- `catalogFilter` narrows the offered entities by kind and fields, for example `kind: Group`.
- `allowedKinds` is deprecated; use `catalogFilter`. `defaultKind` and `defaultNamespace` fill in missing parts of a typed reference.
- `allowArbitraryValues` (default `true`) controls whether the user can enter a value that is not an existing entity; `false` validates input against real entities.
- `autoSelect` (default `true`) auto-selects on blur; `false` requires explicit selection.

The same page covers other fields, including those that capture an OAuth token for the signed-in user: the `secretsKey` option names where the credential is stored in the template secrets context, and `additionalScopes` requests extra permissions.

## Checked

2026-11-03. Confirmed against the Backstage UI Options Examples page: `catalogFilter`, `defaultKind`, `defaultNamespace`, `allowArbitraryValues`, `autoSelect`, `MultiEntityPicker`, `secretsKey`. Removed: the unsupported advice on pickers versus free text and `parseEntityRef`; corrected `allowedKinds` (deprecated).

Method: documentation only; no commands were run.
