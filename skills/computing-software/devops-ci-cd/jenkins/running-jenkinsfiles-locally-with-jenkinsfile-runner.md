---
id: computing-software.devops-ci-cd.jenkins.running-jenkinsfiles-locally-with-jenkinsfile-runner
name: running-jenkinsfiles-locally-with-jenkinsfile-runner
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkinsfile-runner, pipeline-dev-tools, jenkinsfile]
level: advanced
status: docs-checked
description: "Run a Jenkinsfile without a full controller using jenkinsfile-runner: CLI form, Docker image and custom images."
sources: ["https://github.com/jenkinsci/jenkinsfile-runner"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Jenkinsfiles locally with jenkinsfile-runner

jenkinsfile-runner runs a Jenkinsfile in a stripped-down Jenkins without a full controller. The README gives the CLI form `jenkinsfile-runner -w <path to war> -p <path to plugins> -f <path to Jenkinsfile>`, and a Docker image is published as `jenkins/jenkinsfile-runner` on Docker Hub (it must be extended to run real-world pipelines).

## Custom image with your plugins
The README describes building a custom image with the plugins you need, and Custom War Packager is the alternative (images it generates map the workspace to `/build`). Follow the README's current build instructions rather than copying older Dockerfiles.

## Limits
Do not assume features of a full controller (agents, credentials, shared libraries) are available without configuration; read the README's limitations before relying on it.

## Verify
- [ ] The README's `Print hello` sample Jenkinsfile runs to completion.

## Checked
2026-10-28. Confirmed in the jenkinsfile-runner README: `-w`, `-p`, `-f` CLI form, the `jenkins/jenkinsfile-runner` image on Docker Hub, the need to extend the image for real pipelines, Custom War Packager and its `/build` workspace mapping, and the `Print hello` sample Jenkinsfile.
Removed (not confirmed): the `-a` parameter flag, the Dockerfile with plugin-manager and `CASC_JENKINS_CONFIG`, the Docker socket and `checkout scm` limits, the maintenance remark, the alternatives table, the DOCKER.md source (404).

Method: documentation only; no commands were run.
