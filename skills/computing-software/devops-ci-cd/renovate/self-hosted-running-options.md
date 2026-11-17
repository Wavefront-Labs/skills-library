---
id: computing-software.devops-ci-cd.renovate.self-hosted-running-options
name: self-hosted-running-options
category: computing-software
field: devops-ci-cd
product: renovate
tags: [self-hosted, distributions, npm-cli, renovate]
level: practitioner
status: docs-checked
description: "Choose a Renovate distribution and responsibilities when self-hosting, from npm CLI to Docker to the Mend products."
sources:
  - https://docs.renovatebot.com/getting-started/running/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Self-hosting makes you the administrator: you provide the infrastructure Renovate runs on, provision its global config, make sure it runs regularly, and keep Renovate itself updated.

Distributions:

- The npm package `renovate` (the open source CLI) runs in any Node.js environment, even via `npx`, processes all repositories it is configured with, then exits. You must install tools like Ruby, Python, Composer, Bundler and Poetry yourself.
- Docker images on Docker Hub (`renovate/renovate`) and GitHub container registry (`ghcr.io/renovatebot/renovate`), for `linux/amd64` and `linux/arm64` (the arm64 image may still have some bugs). Windows and macOS containers are not supported.
- The `renovatebot/github-action` GitHub Action and the "Renovate Runner" project for GitLab CI, which run on their own CI infrastructure.
- Mend Renovate Community and Enterprise Editions (closed source, stateful, do not exit after a run), documented in the `mend/renovate-ce-ee` repository. Mend Remediate is for Mend commercial customers.
- Forking Renovate, a sister app to the Mend Renovate App that needs only read access and submits PRs from a fork. It works on public repositories only and lacks `automerge` and `baseBranchPatterns`.

Docker image flavors: the default image holds only Node.js and installs tools at runtime (recommended for most users); the `-full` image pre-installs one version of most, but not all, package managers, weighs several gigabytes, and suits users who do not want runtime installs.

Scheduling: for the npm package and Docker images you need VM or container infrastructure and a cron-like capability to schedule runs; the docs recommend running Renovate hourly if possible. The long-lived Mend CE, EE and Remediate containers have this built in.

Global config can come from a config file (default `config.js`, or another `*.js`, `*.ts`, `*.json`, `*.json5`, `*.yaml` or `*.yml` file named by `RENOVATE_CONFIG_FILE`), an additional file via `RENOVATE_ADDITIONAL_CONFIG_FILE` (higher priority than the default file), `RENOVATE_`-prefixed environment variables such as `RENOVATE_TOKEN`, a stringified `RENOVATE_CONFIG`, or CLI parameters. Keep as much non-global config as possible in repository config files so end users can see it.

On Windows, you can run Renovate natively if all needed tools are preinstalled, and the docs ask you to read the self-hosting on Windows notes about line endings.

## Checked

2026-11-08: read the whole Running Renovate page (raw source of docs.renovatebot.com/getting-started/running). Confirmed the distributions, image flavors and their trade-offs, the platform and architecture notes, the hourly scheduling recommendation, the Mend editions, Forking Renovate limits, and the global config sources and file names. Removed the `docker run` example, the claim that repository `schedule` never triggers runs, and the run-time scaling claim, which the page does not state.
Method: documentation only; no commands were run.
