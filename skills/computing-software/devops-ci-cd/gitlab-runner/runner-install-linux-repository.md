---
id: computing-software.devops-ci-cd.gitlab-runner.runner-install-linux-repository
name: runner-install-linux-repository
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [install, linux, apt, rpm, package-repository]
level: intro
status: docs-checked
description: "Install GitLab Runner on Linux from the official GitLab deb or rpm package repository."
sources: ["https://docs.gitlab.com/runner/install/linux-repository/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install from the GitLab package repository

Packages are published for Debian, Raspbian, Linux Mint and Ubuntu (deb) and for Amazon Linux, RHEL, Fedora, Oracle Linux, openSUSE and SUSE Linux Enterprise Server (rpm). Distributions not listed have no repository packages; download the DEB or RPM manually from the S3 bucket instead.

1. Download the repository script (`script.deb.sh` or `script.rpm.sh` from `https://packages.gitlab.com/install/repositories/runner/gitlab-runner/`), inspect it with `less`, then run it with `sudo bash`.
2. Install the latest version with `sudo apt install gitlab-runner` (or the rpm equivalent), or install a specific version.

The skel directory usage is disabled by default to prevent `No such file or directory` job failures.

After installation the service file is created automatically (systemd: `/etc/systemd/system/gitlab-runner.service`). The runner does nothing until you register it.

## Checked

2026-11-03. Confirmed against supported distributions, S3 fallback and skel note on Install from the package repository.

Method: documentation only; no commands were run.
