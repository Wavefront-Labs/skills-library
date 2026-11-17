---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-steps-and-commands
name: woodpecker-steps-and-commands
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [steps, commands, workflow-yaml]
level: intro
status: docs-checked
description: "Define Woodpecker CI workflow steps, how commands run as one shell script, and how to skip a commit."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/linter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker steps and commands

A workflow file lists `steps`. Each step runs in a container named by `image`, and steps run serially in the order defined. A non-zero exit code ends the workflow and the pipeline with an error, except for steps whose `status` condition includes `failure`.

```yaml
steps:
  - name: backend
    image: golang
    commands:
      - go build
      - go test
```

`name` is optional; unnamed steps are numbered. A map form is also valid, where the key is the name (`steps: { backend: { image: golang } }`).

Key behaviours:

- `commands` are converted into a simple shell script that starts with `set -e`, then executed as the container entrypoint. Only build steps can define `commands`, not plugins or services.
- With `commands` set, the default entrypoint is `["/bin/sh", "-c", "echo $CI_SCRIPT | base64 -d | /bin/sh -e"]`. A custom `entrypoint` must be a list of the command and its arguments.
- The commit is cloned into a workspace volume mounted on every step, so files written by one step are visible to the next.
- `directory` sets a repository subdirectory or an absolute container path in which commands run.
- Add `[SKIP CI]` or `[CI SKIP]` (case-insensitive) to a commit message to skip that commit.

Validate a file with `woodpecker-cli lint <files>` before pushing.

## Checked

2026-11-03. Confirmed against: workflow-syntax (steps, commands, entrypoint, directory, skip commits) and linter (woodpecker-cli lint). Removed: nothing.

Method: documentation only; no commands were run.
