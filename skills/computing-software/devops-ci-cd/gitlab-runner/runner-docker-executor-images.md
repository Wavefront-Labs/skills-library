---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-executor-images
name: runner-docker-executor-images
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [docker-executor, allowed-images, image, allowed-services]
level: practitioner
status: docs-checked
description: "Restrict which job and service images the Docker executor may use."
sources: ["https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker executor images

In `[runners.docker]`, `image` sets the default image for jobs that do not specify one. Two allow-lists restrict what jobs may request:

- `allowed_images`: patterns for the `image:` keyword.
- `allowed_services`: patterns for the `services:` keyword.

For example `allowed_images = ["ruby:*", "python:*"]`.

## Checked

2026-11-03. Confirmed against image, allowed_images and allowed_services on Advanced configuration. Removed generic closing advice.

Method: documentation only; no commands were run.
