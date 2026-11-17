---
id: computing-software.devops-ci-cd.gitlab-runner.runner-security-hardening
name: runner-security-hardening
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [security, network-segmentation, git-strategy, host-hardening, ephemeral]
level: advanced
status: docs-checked
description: "Hardening measures: segmentation, ephemeral hosts and avoiding GIT_STRATEGY fetch."
sources: ["https://docs.gitlab.com/runner/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hardening self-managed runners

- `GIT_STRATEGY: fetch` reuses the local working copy; any user with access can add code that executes in other users' pipelines, and submodule contents remain reachable through the reflog even after deletion. Use it only when you trust all users of the shared environment.
- Privileged jobs: use isolated ephemeral VMs, dedicated runners and protected branches only.
- Network segmentation: put runner VMs in their own segment, block SSH from the Internet, restrict traffic between runner VMs and filter access to cloud metadata endpoints. Runners need outbound access to GitLab and usually the Internet.
- Secure the host: apply OS security best practices and remove files, such as SSH keys, that could help an attacker.

## Checked

2026-11-03. Confirmed against hardening bullets on the Security page.

Method: documentation only; no commands were run.
