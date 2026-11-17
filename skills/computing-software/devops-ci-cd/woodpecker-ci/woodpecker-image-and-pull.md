---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-image-and-pull
name: woodpecker-image-and-pull
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [image, pull, registry-images]
level: intro
status: docs-checked
description: "Choose container images for Woodpecker steps and control when they are pulled."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/registries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker step images and pull policy

`image` names the container used as the environment for a step. It applies to build steps, plugins and service containers alike.

```yaml
steps:
  - name: build
    image: golang:1.7
  - name: prettier
    image: woodpeckerci/plugin-prettier
services:
  - name: database
    image: mysql
```

Any valid Docker image reference from any registry works, for example `golang`, `library/golang:1.7` or `index.docker.io/library/golang:1.7`. Images from private registries need credentials registered in the repository settings (see the registries page).

By default Woodpecker does not upgrade images automatically. It pulls an image only when it is not already present on the agent. To refresh a moving tag, set `pull: true` on the step:

```yaml
steps:
  - name: build
    image: golang:latest
    pull: true
```

With the `local` backend, `image` instead names the shell (such as Bash or Fish) used to run the commands, not a container image.

## Checked

2026-11-03. Confirmed against: workflow-syntax (image, pull, local backend shell) and registries. Removed: the generic advice paragraph on pinning tags.

Method: documentation only; no commands were run.
