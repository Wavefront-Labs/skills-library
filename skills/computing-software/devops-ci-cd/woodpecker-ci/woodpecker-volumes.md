---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-volumes
name: woodpecker-volumes
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [volumes, docker-socket, trusted-repos]
level: advanced
status: docs-checked
description: "Mount host paths or named volumes into Woodpecker steps on trusted repositories."
sources: ["https://woodpecker-ci.org/docs/usage/volumes", "https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes", "https://woodpecker-ci.org/docs/administration/configuration/backends/docker", "https://woodpecker-ci.org/docs/usage/project-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker volumes

The `volumes` key mounts host files or folders into step containers. It is available only to trusted repositories and should only be used in private environments; an instance admin enables it through the project setting `Trusted`.

```yaml
steps:
  - name: build
    image: docker
    commands:
      - docker build --rm -t octocat/hello-world .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

Rules:

- Volumes are mounted from the host machine, so host paths must be absolute. A relative path such as `./certs:/etc/ssl/certs` is an error; write `/etc/ssl/certs:/etc/ssl/certs`.
- With the Docker backend you can also use named volumes like `some_volume_name:/var/run/volume`.
- On the Kubernetes backend a volume references a PersistentVolumeClaim created beforehand, for example `woodpecker-cache:/woodpecker/src/cache`.
- To mount defaults into every step on the Docker backend, set `WOODPECKER_BACKEND_DOCKER_VOLUMES` on the agent.

## Checked

2026-11-03. Confirmed against: volumes (trusted only, absolute paths, named volumes), Kubernetes backend (PVC volumes) and Docker backend (WOODPECKER_BACKEND_DOCKER_VOLUMES). Removed: a closing paragraph on the Docker socket and Buildx not stated on the volumes page.

Method: documentation only; no commands were run.
