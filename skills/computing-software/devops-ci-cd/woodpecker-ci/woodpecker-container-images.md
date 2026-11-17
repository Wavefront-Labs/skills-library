---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-container-images
name: woodpecker-container-images
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [container-images, tags, versioning]
level: practitioner
status: docs-checked
description: "Pick Woodpecker container image tags and know which registries and variants exist."
sources: ["https://woodpecker-ci.org/docs/administration/general"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker container images and tags

There is no `latest` tag, to prevent accidental major upgrades. Use a SemVer tag, a rolling major or minor tag, or `next`.

- `vX.Y.Z` (plus `vX.Y` and `vX`): specific releases, scratch image with no entrypoint shell.
- `vX.Y.Z-alpine` (plus `vX.Y-alpine`, `vX-alpine`): rootless for Server and CLI as of v3.0.
- `next`: built from the `main` branch.
- `pull_<PR_ID>`: images built from pull request branches.

Images are pushed to DockerHub and Quay: woodpecker-server, woodpecker-agent and woodpecker-cli (both registries) and woodpecker-autoscaler (DockerHub only).

Examples from the docs use `woodpeckerci/woodpecker-server:v3` and `woodpeckerci/woodpecker-agent:v3`.

The plain tags are scratch images with no entrypoint shell; the `-alpine` tags are the alternative.

Pin a major tag such as `v3` for automatic minor and patch updates, or an exact tag when you need controlled upgrades. Avoid `next` in production, since it follows the main branch.

## Checked

2026-11-03. Read the Woodpecker general administration page and confirmed no latest tag, SemVer and rolling tags, -alpine rootless for server and CLI from v3.0, next, pull_<PR_ID>, DockerHub and Quay registries and the image names. Removed: the shell-based lint example and the namespaced autoscaler image name, which the page does not show. 

Method: documentation only; no commands were run.
