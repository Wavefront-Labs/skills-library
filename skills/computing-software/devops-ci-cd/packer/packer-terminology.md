---
id: computing-software.devops-ci-cd.packer.packer-terminology
name: packer-terminology
category: computing-software
field: devops-ci-cd
product: packer
tags: [terminology, concepts, artifacts, builders]
level: intro
status: docs-checked
description: "Packer's core terms: templates, builders, provisioners, post-processors, artifacts, data sources, builds and commands."
sources:
  - "https://developer.hashicorp.com/packer/docs/terminology/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Packer's docs define a small vocabulary.

- Templates: configuration files, HCL2 or legacy JSON, describing what to build.
- Builders: plugin components that create machines and produce images for a platform such as AWS or Docker. In HCL2 a builder is configured by a `source` block.
- Provisioners: install and configure software inside the running machine before it becomes an image.
- Post-processors: take the result of a builder or another post-processor and process it, for example compress or upload.
- Artifacts: the output of a build, whether an image id or a set of files.
- Builds: a single task that eventually produces an artifact for a single platform; multiple builds run in parallel.
- Data sources: components that fetch data from outside Packer for use in the template.
- Commands: sub-commands of the `packer` program, for example `build`.

## Checked
2026-11-03. Confirmed against the Terminology page: artifacts, builds, builders, commands, data sources, post-processors, provisioners and templates. Removed the communicators entry, the flow sentence and a closing tip, which the page does not contain.
Method: documentation only; no commands were run.
