---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-docker-backend
name: woodpecker-docker-backend
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [docker-backend, resource-limits, network]
level: practitioner
status: docs-checked
description: "Configure the Woodpecker Docker backend: networks, volumes, limits, user and cleanup."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/backends/docker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Docker backend

The Docker backend, the original one, runs each step in a separate container on the agent. Agent settings, all prefixed `WOODPECKER_BACKEND_DOCKER_`:

- `NETWORK`: existing network attached to all step containers. Careful: it lets containers of different pipelines reach each other.
- `ENABLE_IPV6` (false): needs Docker daemon IPv6 support.
- `VOLUMES`: default volumes for all steps, comma-separated, such as `/etc/ssl/certs:/etc/ssl/certs:ro`.
- `APPARMOR_PROFILE`: AppArmor profile for step containers.
- `LIMIT_MEM`, `LIMIT_MEM_SWAP`, `LIMIT_SHM_SIZE`: bytes; 0 means no limit.
- `LIMIT_CPU_QUOTA` (microseconds per period), `LIMIT_CPU_SHARES`, `LIMIT_CPU_SET` (for example `1,2`).
- `STOP_TIMEOUT` (20): seconds before a container is killed.

Run user per step:

```yaml
steps:
  - name: example
    image: alpine
    backend_options:
      docker:
        user: 65534:65534
```

The syntax matches `docker run --user`. Without it the image default user is used.

Cleanup: the agent does not remove images. Schedule host jobs, for example removing dangling images and volumes with `docker volume ls --filter name=^wp_*`. These commands are destructive; test them first.

Registry credential helpers go in the Docker config file named by `WOODPECKER_DOCKER_CONFIG`. Podman is not officially supported.

## Checked

2026-11-03. Read the Woodpecker Docker backend page and confirmed the backend environment variables, defaults and behaviours described in the skill. Nothing removed. 

Method: documentation only; no commands were run.
