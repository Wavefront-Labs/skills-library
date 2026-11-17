---
id: computing-software.devops-ci-cd.kustomize.replacements-overview
name: replacements-overview
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replacements, source, targets, fieldpath]
level: practitioner
status: docs-checked
description: "Copy a field from one source resource into one or many target fields with replacements, inline or from a file."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Replacements copy fields from one source into any number of targets. They can live inline or in a file:

```yaml
replacements:
- path: replacement.yaml
- source:
    kind: Deployment
    fieldPath: metadata.name
  targets:
  - select:
      name: my-resource
```

Schema highlights: `source` (group, version, kind, name, namespace, `fieldPath`, `options`) or `sourceValue` (a scalar), and `targets`, each with `select`, optional `reject`, `fieldPaths` and `options`. Required: either `source` or `sourceValue`, `targets` and `select`. Defaults: `fieldPath` and `fieldPaths` default to `metadata.name`.

Rules:

- `source` selection must resolve to a single resource; all its subfields are optional.
- `source` and `sourceValue` are mutually exclusive.
- Targets are all resources matched by `select` and not by `reject`, at every listed `fieldPaths`.
- Subfields of `select` and `reject` that identify a resource accept strings and regular expressions.

Task-page example: copy the Service `my-nginx` `metadata.name` (after `namePrefix: dev-` and `nameSuffix: "-001"` it is `dev-my-nginx-001`) into `spec.template.spec.containers.0.command.2` of the Deployment. That keeps the name correct however the prefix changes, replacing the deprecated `vars`.

## Checked

2026-11-03. Confirmed against: the replacements reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
