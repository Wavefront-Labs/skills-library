---
id: computing-software.data-engineering.kestra.script-dependencies
name: script-dependencies
category: computing-software
field: data-engineering
product: kestra
tags: [beforecommands, containerimage, pip, requirements, prebuilt-images]
level: practitioner
status: docs-checked
description: "Install dependencies for Kestra script tasks at runtime with beforeCommands, requirements.txt via inputFiles, and prebuilt images, and when to build your own."
sources:
  - https://kestra.io/docs/scripts/installing-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`beforeCommands` runs shell commands before the script, alongside `containerImage`:

```yaml
containerImage: python:3.11-slim
beforeCommands:
  - pip install requests kestra > /dev/null
```

Requirements file: either clone a repo containing it with `io.kestra.plugin.git.Clone` inside a `WorkingDirectory` (the `WorkingDirectory` task is usually only needed with `git.Clone`), or use the `inputFiles` property to add files to the script's working directory:

```yaml
env:
  PIP_ROOT_USER_ACTION: ignore
inputFiles:
  requirements.txt: |
    polars
    requests
    kestra
containerImage: python:3.11-slim
beforeCommands:
  - pip install -r requirements.txt > /dev/null
```

Other languages on the Process task runner (`io.kestra.plugin.core.runner.Process`): install the language toolchain in `beforeCommands` before executing the code; the page's example does this for Go.

Prebuilt images: the kestra-io/examples repository provides public images hosted on GitHub Container Registry, named `ghcr.io/kestra-io/packageName:latest`, for common packages such as pandas, dbt-core and requests. The R example uses `ghcr.io/kestra-io/rdata:latest`.

Caveats:

- Installing R libraries at runtime is time-consuming and might take up to 30 minutes, depending on the packages.
- Prebuilt images help you iterate faster; before moving to production, you can build custom images with the exact package versions you need.

## Checked

2026-11-04. Confirmed against "Use beforeCommands or Docker Images to Install Script Dependencies" (scripts/installing-dependencies): beforeCommands pip examples, requirements.txt via inputFiles and PIP_ROOT_USER_ACTION, WorkingDirectory note, Process runner for other languages, prebuilt image naming, rdata R example, 30 minute R install note. Reworded the slow-install caveat, which the page states only for R packages.
Method: documentation only; no commands were run.
