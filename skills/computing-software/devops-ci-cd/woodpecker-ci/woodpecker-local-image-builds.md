---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-local-image-builds
name: woodpecker-local-image-builds
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [local-images, docker-socket, single-agent]
level: advanced
status: docs-checked
description: "Build and use a local image inside one Woodpecker pipeline via the Docker socket."
sources: ["https://woodpecker-ci.org/docs/usage/registries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker local image builds

You can build an image in one step and use it in the next without a registry by mounting the Docker socket. This needs privileged rights that only admins have, and it only works when a single agent is used, because the image exists only on that agent's Docker host.

With a `Dockerfile` at the project root:

```yaml
steps:
  - name: build-image
    image: docker
    commands:
      - docker build --rm -t local/project-image .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  - name: build-project
    image: local/project-image
    commands:
      - ./build.sh
```

Pushing to a registry still requires setting credentials for the appropriate plugin; registry credentials set in the UI are only used by the agent to pull images and are never exposed to steps.

## Checked

2026-11-08. Read the Woodpecker registries page in full (raw markdown) and confirmed the Local Images warning (admin-only privileged rights, single agent only), the Docker socket volume example, and the push-credentials note. Removed: the trusted-repository requirement, the multi-agent failure explanation, and the image cleanup advice, which the page does not state.

Method: documentation only; no commands were run.
