---
id: computing-software.devops-ci-cd.earthly.earthly-ci-vendor-configs
name: earthly-ci-vendor-configs
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, circleci, gitlab-ci, codebuild, bitbucket-pipelines, woodpecker, google-cloud-build, jenkins]
level: practitioner
status: docs-checked
description: "Earthly build snippets and caveats for CircleCI, AWS CodeBuild, GitLab CI, Bitbucket Pipelines, Woodpecker, Google Cloud Build and Jenkins, including EARTHLY_EXEC_CMD."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/circle-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/codebuild-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/gitlab-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/bitbucket-pipelines-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/woodpecker-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/google-cloud-build.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/jenkins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly on specific CI systems

Most examples build the `+build` target with `earthly --ci --push` (GitLab adds `-P`, Bitbucket adds `--sat` and `--org`, Cloud Build passes the same flags as step args).

## CircleCI
Use a `machine` executor (image ubuntu-2004:2023.02.1 in the example), `docker login`, download the earthly binary to /usr/local/bin/earthly, then run earthly.

## AWS CodeBuild
Enable the `Privileged` flag on the CodeBuild project so Earthly can build Docker images. In buildspec.yml: download the binary in `install`, `docker login` in `pre_build`, run earthly in `build`.

## GitLab CI/CD
```yaml
services:
  - docker:dind
variables:
  DOCKER_HOST: tcp://docker:2375
  FORCE_COLOR: 1
  EARTHLY_EXEC_CMD: "/bin/sh"
image: earthly/earthly:v0.8.13
before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
earthly:
  stage: build
  script:
    - earthly --ci --push -P +build
```
The image entrypoint starts BuildKit first; `EARTHLY_EXEC_CMD=/bin/sh` makes it present a shell instead of calling earthly, before `before_script` runs. For a registry mirror set a multi-line `EARTHLY_ADDITIONAL_BUILDKIT_CONFIG` under `variables` (`[registry."docker.io"]` with `mirrors = [...]`).

## Bitbucket Pipelines
Cannot run Earthly directly because of Bitbucket restrictions; use a remote runner such as a Satellite with image `earthly/earthly:v0.8.13`: `earthly --ci --push --sat $EARTHLY_SAT --org $EARTHLY_ORG +build`, with `EARTHLY_TOKEN` exported.

## Woodpecker CI
Mark the project trusted and allow the `earthly/earthly` image in privileged mode. Mount /var/run/docker.sock, set `FORCE_COLOR=1` and `EARTHLY_EXEC_CMD="/bin/sh"`, log in, then run earthly. Secret references use `$${NAME}`.

## Google Cloud Build
Works including `WITH DOCKER`, but Application Default Credentials are unavailable, so `gcloud`/`gsutil` in an Earthfile need a service account key. Only the "Cloud Build configuration file" trigger type works. Step: name `earthly/earthly:v0.8.13`, args `--ci`, `--push`, `+build`; load `EARTHLY_TOKEN` from Secret Manager via `availableSecrets`.

## Jenkins
Tested standalone and with the Docker Cloud provider (which needs an existing Docker daemon). Build your own runner image from `earthly/earthly`, and set `DOCKER_HOST` (tick "Expose Docker Host").

## Gotcha
Cloud Build and Jenkins: Earthly misreads the environment as a terminal; set `NO_COLOR` to `1` to hide ANSI codes.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: ci-integration/guides/circle-integration.md, ci-integration/guides/codebuild-integration.md, ci-integration/guides/gitlab-integration.md, ci-integration/guides/bitbucket-pipelines-integration.md, ci-integration/guides/woodpecker-integration.md, ci-integration/guides/google-cloud-build.md, ci-integration/guides/jenkins.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: replaced 'all examples' with the exact flags each example uses.

Method: documentation only; no commands were run.
