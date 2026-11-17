---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-yaml-anchors
name: woodpecker-yaml-anchors
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [yaml-anchors, variables, dry]
level: practitioner
status: docs-checked
description: "Remove duplication from Woodpecker workflows using YAML anchors, aliases and merge keys."
sources: ["https://woodpecker-ci.org/docs/usage/advanced-usage", "https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker YAML anchors and merges

Woodpecker supports YAML anchors and aliases as variables. Define them in a top-level `variables` section and reference them with `*`:

```yaml
variables:
  - &golang_image 'golang:1.18'

steps:
  - name: test
    image: *golang_image
    commands: go test ./...
  - name: build
    image: *golang_image
    commands: build
```

Map merges combine settings and let later keys overwrite:

```yaml
variables:
  - &base-plugin-settings
    target: dist
    recursive: false
    try: true
  - &special-setting
    special: true

steps:
  - name: main
    image: some/plugin
    settings:
      <<: *base-plugin-settings
      try: false      # overwrite
      ongoing: false  # add
```

Merge several maps with `<<: [*base-plugin-settings, *special-setting]`.

Sequence merges prepend or append lists of commands:

```yaml
commands:
  - <<: *pre_cmds
  - echo do the step
  - <<: *post_cmds
```

Woodpecker supports most of YAML 1.2 but keeps some YAML 1.1 behaviour for backward compatibility.

## Checked

2026-11-03. Confirmed against: advanced-usage (anchors, map merges, sequence merges) and workflow-syntax (YAML 1.2 note, variables). Removed: a closing paragraph of generic practical uses.

Method: documentation only; no commands were run.
