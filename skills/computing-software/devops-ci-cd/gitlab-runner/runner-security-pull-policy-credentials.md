---
id: computing-software.devops-ci-cd.gitlab-runner.runner-security-pull-policy-credentials
name: runner-security-pull-policy-credentials
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [security, pull-policy, if-not-present, credential-helpers, docker-auth-config]
level: advanced
status: docs-checked
description: "Why if-not-present leaks private images and how credential helpers are gated."
sources: ["https://docs.gitlab.com/runner/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pull policy and credential helper security

With `if-not-present`, user A's build pulls a private image with credentials; the image stays on the host; user B's build on the same instance runner finds it locally and runs it without access. On shared runners use `always` (users can pull any image from any registry) or `never` (only images you pre-pulled). Keep `if-not-present` for specific runners used by trusted builds.

Credential helpers referenced through a job's `DOCKER_AUTH_CONFIG` execute as binaries on the runner manager host. By default the runner executes none of them. List trusted helpers and the registries they may serve with `allowed_docker_credential_helpers`.

That setting does not restrict the host's own `~/.docker/config.json` and `~/.dockercfg`; their credentials are available to every job. On shared runners do not run `docker login` as the runner user.

## Checked

2026-11-03. Confirmed against pull policy risk and credential helper behaviour on the Security page.

Method: documentation only; no commands were run.
