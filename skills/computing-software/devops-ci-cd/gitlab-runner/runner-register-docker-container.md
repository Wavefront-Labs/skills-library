---
id: computing-software.devops-ci-cd.gitlab-runner.runner-register-docker-container
name: runner-register-docker-container
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [register, docker, container, config-volume]
level: practitioner
status: docs-checked
description: "Register a runner that lives in a container, with the correct config volume mount."
sources: ["https://docs.gitlab.com/runner/register/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Register a containerised runner

Two options exist:

1. A short-lived container with the same configuration volume used at install time:
   `docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner register`
   For a named volume: `-v gitlab-runner-config:/etc/gitlab-runner` with `gitlab/gitlab-runner:latest`.
2. The executable inside the active runner container: `docker exec -it gitlab-runner gitlab-runner register`.

If you used a configuration volume other than `/srv/gitlab-runner/config` during installation, update the command with the correct volume.

The prompts are the same as on a host install: GitLab URL, authentication token, description, tags, maintenance note and executor.

## Checked

2026-11-03. Confirmed against docker run register commands and the volume note on the Register page.

Method: documentation only; no commands were run.
