---
id: computing-software.devops-ci-cd.semaphore-ui.install-deb-rpm-package
name: install-deb-rpm-package
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [package, deb, rpm, dpkg, installation, semaphore-ui]
level: intro
status: docs-checked
description: "Install the Semaphore .deb or .rpm release package on Debian, Ubuntu or CentOS and run setup."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/package-manager
  - https://semaphoreui.com/docs/introduction/prerequisites
  - https://semaphoreui.com/docs/admin-guide/upgrading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install the Semaphore package

Goal: install Semaphore from the release `.deb` or `.rpm`.

Download the file from the GitHub Releases page; `*.deb` is for Debian and Ubuntu, `*.rpm` for CentOS and Red Hat.

```bash
wget https://github.com/semaphoreui/semaphore/releases/download/v2.17.15/semaphore_2.17.15_linux_amd64.deb
sudo dpkg -i semaphore_2.17.15_linux_amd64.deb
# CentOS / RHEL
sudo yum install semaphore_2.17.15_linux_amd64.rpm
```

Use the `arm64` files on ARM machines. Then configure and start:

```bash
semaphore setup
semaphore server --config=./config.json
```

`setup` generates `config.json` interactively. The server answers on port 3000.

Gotchas:
- The package does not create a service for you; create the systemd unit manually (see the systemd service skill).
- Ansible, Python and git must be present; see the manual installation guide for the environment.
- Upgrading is the same operation: install the newer package over the old one (see the upgrade skill).

Verify: the UI loads on port 3000 after `semaphore setup` and `semaphore server`.

## Checked

2026-11-04: checked against the package manager installation, prerequisites and upgrading pages. Every claim is stated there.

Method: documentation only; no commands were run.
