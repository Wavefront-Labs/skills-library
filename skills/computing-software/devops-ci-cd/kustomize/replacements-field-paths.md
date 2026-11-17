---
id: computing-software.devops-ci-cd.kustomize.replacements-field-paths
name: replacements-field-paths
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replacements, fieldpath, wildcard, list-index, regexp]
level: advanced
status: docs-checked
description: "Write replacements fieldPath and fieldPaths with dots, escaped keys, list indexes, key=value matches and wildcards."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`fieldPath` and `fieldPaths` use a `.`-separated path. The default is `metadata.name`.

Escaping a dot inside a key (here the annotation `config.kubernetes.io/local-config`):

- backslash: `metadata.annotations.config\.kubernetes\.io/local-config`
- brackets: `metadata.annotations.[config.kubernetes.io/local-config]`

Sequence nodes can be addressed three ways:

- by number: `spec.template.spec.containers.1.image`
- by key-value pair: `spec.template.spec.containers.[name=nginx].image`. If the pair matches several elements, all matching elements are targeted.
- by wildcard: `spec.template.spec.containers.*.env.[name=TARGET_ENV].value`, which targets every element of the list.

After kustomize v4.5.3 the key-value match uses a regular expression. For an exact match write anchors: `spec.template.spec.containers.[name=^nginx$].image`.

Selectors:

```yaml
labelSelector: "environment=production,tier=frontend"
labelSelector: "environment in (production),tier notin (frontend, backend)"
```

Both equality-based and set-based requirements work; `annotationSelector` follows the same rules.

Tips: prefer `[name=...]` over numeric indexes so reordering containers does not silently retarget; use a wildcard when the same field must be set in all containers. Add `options.create: true` to create a missing target field.

Test each fieldPath by building and reading the target field, and escape or bracket dots inside keys.

## Checked

2026-11-03. Confirmed against: the replacements reference page.
Removed or reworded: the claim that unmatched source paths report an error.

Method: documentation only; no commands were run.
