---
id: computing-software.devops-ci-cd.gitlab-runner.runner-install-docker-container
name: runner-install-docker-container
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [install, docker, container, volume, session-server]
level: practitioner
status: docs-checked
description: "Run GitLab Runner itself in a container with a persistent config volume."
sources: ["https://docs.gitlab.com/runner/install/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run GitLab Runner in a container

Every runner command has a `docker run` equivalent: `docker run <options> gitlab/gitlab-runner <runner command>`. For example `docker run --rm -t -i gitlab/gitlab-runner --help`.

Docker Engine and runner image versions do not have to match; the images are backwards and forwards compatible.

Mount a permanent volume so `config.toml` survives restarts: a local directory such as `/srv/gitlab-runner/config:/etc/gitlab-runner`, or a named Docker volume.

Optional flags:
- `-p 8093:8093` when you use a `session_server`.
- `--env TZ=<TIMEZONE>` to set the container time zone.
- `-v /srv/gitlab-runner/docker-machine-config:/root/.docker/machine` to keep Docker Machine state for autoscaling.

For a FIPS-compliant image based on `redhat/ubi9-micro`, use the `gitlab/gitlab-runner:ubi-fips` tags.

Isolation guarantees break if the runner container shares a Docker daemon with other payloads, because each runner container gets full control of the daemon.

## Checked

2026-11-03. Confirmed against docker run usage, version compatibility, config volume, session_server port, TZ, docker-machine volume and ubi-fips tags on Install in Docker. Removed the unsourced registration sentence.

Method: documentation only; no commands were run.
