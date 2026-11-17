---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-workspace
name: woodpecker-workspace
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [workspace, base-path, shared-volume]
level: practitioner
status: docs-checked
description: "Configure the Woodpecker workspace base and path shared by all steps."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/workflows", "https://woodpecker-ci.org/docs/usage/plugins/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker workspace

The workspace is the shared volume and working directory of all steps in a workflow. The default base is `/woodpecker` and the path is `src/{url-without-schema}`, giving for example `/woodpecker/src/github.com/octocat/hello-world`.

Customize it with a top-level block:

```yaml
workspace:
  base: /go
  path: src/github.com/octocat/hello-world

steps:
  - name: build
    image: golang:latest
    commands:
      - go get
      - go test
```

- `base` is a volume mounted into every step, so sources, dependencies and compiled binaries persist across steps.
- `path` is the working directory where the code is cloned and where each step starts. It must be relative and is joined to `base`.
- Plugins always see the workspace base at `/woodpecker`, and their working directory is adjusted for you.

File changes persist between steps of the same workflow because one volume is mounted everywhere. Files are not shared between different workflows; to pass artifacts between workflows, use a storage plugin such as an S3 plugin.

Each workflow has its own isolated workspace.

## Checked

2026-11-03. Confirmed against: workflow-syntax (workspace base and path), workflows (files not shared between workflows) and plugins overview (base /woodpecker). Removed: nothing.

Method: documentation only; no commands were run.
