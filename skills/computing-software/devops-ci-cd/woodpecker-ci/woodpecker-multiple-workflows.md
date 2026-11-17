---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-multiple-workflows
name: woodpecker-multiple-workflows
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [workflows, pipeline-folder, dot-woodpecker]
level: practitioner
status: docs-checked
description: "Split a Woodpecker pipeline into several workflow files in a .woodpecker folder."
sources: ["https://woodpecker-ci.org/docs/usage/workflows", "https://woodpecker-ci.org/docs/usage/project-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker multiple workflows

A single `.woodpecker.yaml` creates a pipeline with one workflow. Placing files in a `.woodpecker/` folder creates one workflow per file, named after the file. Only `.yml` and `.yaml` files count, and subfolders such as `.woodpecker/sub-folder/test.yaml` are ignored.

```text
.woodpecker/
  build.yaml
  deploy.yaml
  lint.yaml
  test.yaml
```

Benefits: lint and test status reaches the forge before the whole pipeline finishes, concerns stay separated (testing, linting, building, deploying), and more agents can work in parallel.

Each workflow reports its own status to the forge. Workflows run in parallel on separate agents and share nothing, including files. Pass artifacts between workflows with a storage plugin.

A custom folder such as `.my-ci/pipelines/` can be set in the project settings. The default resolution order is `.woodpecker/*.{yaml,yml}`, then `.woodpecker.yaml`, then `.woodpecker.yml`. For multiple workflows with a custom path, use a folder path ending in `/`.

When triggering a pipeline manually you can pick one workflow; only workflows whose `when` conditions match the `manual` event are selectable, and Woodpecker also runs the workflows it hard depends on.

## Checked

2026-11-03. Confirmed against: workflows (folder, file rules, status, benefits, manual trigger) and project-settings (custom path, resolution order). Removed: nothing.

Method: documentation only; no commands were run.
