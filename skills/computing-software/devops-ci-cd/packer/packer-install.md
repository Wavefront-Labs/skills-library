---
id: computing-software.devops-ci-cd.packer.packer-install
name: packer-install
category: computing-software
field: devops-ci-cd
product: packer
tags: [install, homebrew, apt, binary]
level: intro
status: docs-checked
description: "Install Packer with Homebrew, the HashiCorp apt or yum repositories, or a binary download, and enable shell autocomplete."
sources:
  - "https://developer.hashicorp.com/packer/install"
  - "https://developer.hashicorp.com/packer/docs/commands"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The install page offers a package manager or a binary download per platform.

macOS, with Homebrew (the install page also lists Homebrew for Linux):

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/packer
```

Ubuntu and Debian add HashiCorp's apt repository and signing key (copy the exact lines from the install page), then:

```bash
sudo apt update && sudo apt install packer
```

CentOS and RHEL:

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install packer
```

Fedora downloads `https://rpm.releases.hashicorp.com/fedora/hashicorp.repo` into `/etc/yum.repos.d/hashicorp.repo` and then runs `sudo dnf -y install packer`. Amazon Linux installs `yum-utils` and `shadow-utils`, adds `https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo` with `yum-config-manager`, and runs `sudo yum install packer`.

Binary downloads are offered per operating system and architecture, including FreeBSD, NetBSD and OpenBSD; choose the right one from the install page, unzip it and put `packer` on your `PATH`.

Afterwards, `packer version` prints the installed version. To enable shell completion run `packer -autocomplete-install`; the commands page says you must restart your shell afterwards.

## Checked

2026-11-09. Checked against the Packer install page (Homebrew, apt, CentOS/RHEL, Fedora and Amazon Linux command lists, OS sections including FreeBSD, NetBSD and OpenBSD) and the Packer commands page (autocomplete).

Removed: the per-architecture list of binary builds (the page lists architectures per OS and changes with releases), the `required_version` pinning advice, and the repeated advice about re-running `packer version` in CI images, none of which the install page states. The sources list the install page's current URL.

Method: documentation only; no commands were run.
