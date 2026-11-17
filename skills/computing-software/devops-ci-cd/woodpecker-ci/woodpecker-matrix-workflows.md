---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-matrix-workflows
name: woodpecker-matrix-workflows
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [matrix, build-matrix, interpolation]
level: practitioner
status: docs-checked
description: "Test multiple configurations in Woodpecker with matrix workflows and interpolation."
sources: ["https://woodpecker-ci.org/docs/usage/matrix-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker matrix workflows

A `matrix` runs a separate workflow for each combination of values.

```yaml
matrix:
  GO_VERSION:
    - 1.4
    - 1.3
  DATABASE:
    - mysql:8
    - mariadb:10.1

steps:
  - name: build
    image: golang:${GO_VERSION}
    commands:
      - go test

services:
  - name: database
    image: ${DATABASE}
```

Matrix variables are interpolated with `${VARIABLE}` before the YAML is parsed, and also injected into each step as environment variables.

Select explicit combinations with `include`:

```yaml
matrix:
  include:
    - GO_VERSION: 1.4
      REDIS_VERSION: 2.8
    - GO_VERSION: 1.6
      REDIS_VERSION: 3.0
```

Limits: at most 64 workflows are generated per matrix and at most 10 values per axis. A larger matrix is rejected with an error.

Run one step for one permutation with `when: matrix:`. Build for several architectures by combining a `platform` axis with `labels: platform: ${platform}`, and use `when: platform: linux/arm*` to restrict steps. On the Kubernetes backend, control the architecture with `nodeSelector` (see nodeSelector in the Kubernetes backend docs).

## Checked

2026-11-03. Confirmed against: matrix-workflows (limits of 64 and 10, include, interpolation, platform example, nodeSelector note). Removed: the pointer to non-existent Kubernetes skills.

Method: documentation only; no commands were run.
