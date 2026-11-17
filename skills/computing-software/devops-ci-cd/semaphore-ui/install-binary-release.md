---
id: computing-software.devops-ci-cd.semaphore-ui.install-binary-release
name: install-binary-release
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [binary, tar-gz, installation, setup, semaphore-ui]
level: intro
status: docs-checked
description: "Install Semaphore from the release tarball or zip on Linux or Windows, run setup, and start the server."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/binary-file
  - https://semaphoreui.com/docs/introduction/prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Semaphore from a release archive

Goal: run Semaphore without containers or a package manager.

Download the archive for your platform from the GitHub Releases page of `semaphoreui/semaphore`:

```bash
wget https://github.com/semaphoreui/semaphore/releases/download/v2.17.15/semaphore_2.17.15_linux_amd64.tar.gz
tar xf semaphore_2.17.15_linux_amd64.tar.gz
./semaphore setup
```

Use `linux_arm64` for ARM. On Windows download the `windows_amd64.zip`, expand it with `Expand-Archive` and run `./semaphore setup`.

`setup` generates `config.json` interactively. Then start the server:

```bash
./semaphore server --config=./config.json
```

The UI listens on port 3000 by default.

Prerequisites: a binary install gives you Semaphore alone, so install Git, Python, Ansible and any collections yourself (the manual installation guide covers the Python/Ansible/systemd environment). The v2.17.15 in the URL is the docs example; pick the release you want. The docs page prints the URL as https://localhost:3000, but the server serves plain HTTP unless TLS is configured.

Gotchas:
- Run `server` with an explicit `--config` so restarts use the same file.
- For production, create a service (see the systemd skill) rather than a shell session.

Verify: `curl -I http://localhost:3000` returns a response and the login page opens.

## Checked

2026-11-04: checked against the binary installation and prerequisites pages. Corrected the prerequisites and setup wording. The install pages print an https URL although the server serves HTTP by default; the skill notes this.

Method: documentation only; no commands were run.
