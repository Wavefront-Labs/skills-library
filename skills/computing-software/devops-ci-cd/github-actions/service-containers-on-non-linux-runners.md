---
id: computing-software.devops-ci-cd.github-actions.service-containers-on-non-linux-runners
name: service-containers-on-non-linux-runners
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, linux-only-services, service-containers, container-jobs]
level: practitioner
status: docs-checked
description: "Work around service containers and container jobs only running on Linux runners: native installs on macOS/Windows, setup actions, and testcontainers caveats."
sources: ["https://docs.github.com/en/actions/tutorials/use-containerized-services/use-docker-service-containers", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idservices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service containers only run on Linux

The workflow documentation says you must use a Linux environment when using service containers or container jobs, so
`services:` and `container:` cannot be used on macOS or Windows runners.

## Workarounds for macOS/Windows test legs
1. **Split the matrix**: run integration tests (needing databases) only on Linux; run unit tests on all OSes.
   ```yaml
   - run: npm run test:integration
     if: runner.os == 'Linux'
   ```
2. **Install the dependency natively** on the runner as part of the job (package manager or a setup action),
   and make connection settings configurable.
3. **Testcontainers and similar tools** need a Docker daemon, so plan for Linux runners for those tests.

## Connection details (Linux)
- A job running directly on the runner reaches a service container at `localhost:<port>` or `127.0.0.1:<port>`
  and must map the service's ports to the host.
- A job running in a container reaches a service by its label as the hostname and needs no port mapping.
- Because native services use localhost, make connection strings configurable instead of hard-coding the
  service-container hostname.

## Verify
- [ ] Matrix legs on macOS/Windows pass without `services:` and still exercise the DB path where needed.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Service containers and container jobs require a Linux environment; localhost and port mapping for jobs on the runner, label-as-hostname for container jobs: confirmed in the Docker service containers tutorial.
- Removed all unconfirmed claims: the quoted error text, per-OS installation commands and actions, Docker on macOS and Windows behaviour, Docker group requirement.

Method: documentation only; no commands were run.
