---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-step-environment
name: woodpecker-step-environment
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [environment, env-vars, persist-env]
level: intro
status: docs-checked
description: "Set Woodpecker step environment variables, global variables and share them between steps."
sources: ["https://woodpecker-ci.org/docs/usage/environment", "https://woodpecker-ci.org/docs/usage/advanced-usage", "https://woodpecker-ci.org/docs/usage/plugins/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker step environment variables

Pass variables to a step with `environment`:

```yaml
steps:
  - name: build
    image: golang
    environment:
      CGO: 0
      GOOS: linux
    commands:
      - go build
```

These cannot overwrite built-in variables. The `environment` section cannot expand other variables, so to extend `PATH` use `commands: - export PATH=$PATH:/go`.

Global variables: set `WOODPECKER_ENVIRONMENT` on the server to expose values to all pipelines, for example to manage an image tag shared by many projects:

```ini
WOODPECKER_ENVIRONMENT=GOLANG_VERSION:1.18
```

```yaml
image: golang:${GOLANG_VERSION}
```

This couples server configuration to every app that uses the variable, so keep it for truly global values.

Persist data between steps by writing a file into the shared workspace and sourcing it:

```yaml
steps:
  - name: init
    image: bash
    commands:
      - echo "FOO=hello" >> envvars
  - name: debug
    image: bash
    commands:
      - source ./envvars
      - echo $FOO
```

Setting `environment` on a plugin step makes it stop being treated as a plugin, so it loses plugin-only secrets.

## Checked

2026-11-03. Confirmed against: environment (environment key, built-ins not overwritten, WOODPECKER_ENVIRONMENT), advanced-usage (persisting variables) and plugins overview (environment on a plugin). Removed: the PATH example, now matching the docs form.

Method: documentation only; no commands were run.
