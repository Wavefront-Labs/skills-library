---
id: computing-software.cloud-infrastructure-engineering.portainer.git-stack-auto-updates-and-relative-mounts
name: git-stack-auto-updates-and-relative-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [gitops, stacks, webhooks, bind-mounts, relative-paths]
level: advanced
status: docs-checked
description: "Explain how Portainer detects Git changes for stack auto-updates, and why relative bind mounts can appear empty after an update."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/stacks-deployments-and-updates/how-do-automatic-updates-for-stacks-applications-work.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/stacks-deployments-and-updates/empty-relative-bind-mounts.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/relative-paths.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automatic updates for Git-deployed stacks or applications work by polling on an interval or by webhook. Portainer fetches the latest commit hash from the remote and compares it with the hash stored in its database (populated at first deployment, updated on every deployment). If equal, nothing happens. If different, it pulls the repository at the latest commit and processes the Compose path file plus any additional paths: for Docker Standalone this is a `docker-compose up` over those files in the cloned directory, for Swarm a `docker stack deploy`, for Kubernetes a `kubectl apply`. Portainer does not force a redeploy when the image has not changed, and a manual Pull and redeploy skips the commit-hash check and force-redeploys.

Problem: when the commit changes, Portainer re-clones the repository, removing and recreating the directory on the host. A container with a relative-path bind mount into that directory, and not itself recreated, then sees an empty mount. Containers are only recreated when their Compose or configuration changes, unless GitOps Updates with Force redeployment is enabled. Fix: update with Pull and redeploy with Re-pull image and redeploy enabled, which recreates all containers.

Relative path volumes (Business Edition) work via a temporary unpacker container that bind mounts your chosen local or network filesystem path, clones the repository under it, deploys the stack with the Compose file's directory as working directory, then is removed.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Clarified the fix wording; added Kubernetes and the manual-update behaviour.

Method: documentation only; no commands were run.
