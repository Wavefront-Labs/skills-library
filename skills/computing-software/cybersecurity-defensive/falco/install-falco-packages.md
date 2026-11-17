---
id: computing-software.cybersecurity-defensive.falco.install-falco-packages
name: install-falco-packages
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-deb, falco-rpm, falco-driver-choice, falco-frontend, falcoctl-enabled]
level: intro
status: docs-checked
description: "Install the Falco package with apt, yum or zypper and use FALCO_DRIVER_CHOICE, FALCO_FRONTEND and FALCOCTL_ENABLED to automate the setup."
sources:
  - https://falco.org/docs/setup/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco runs on Linux, x86_64 and aarch64. The bundled plugins need GLIBC 2.28 or newer; check with `ldd --version`.

Environment variables for the package manager run:
- `FALCO_FRONTEND=noninteractive` disables the `dialog` prompts. Default is `dialog`.
- `FALCO_DRIVER_CHOICE=kmod` or `modern_ebpf` picks a driver; `none` disables service installation. Empty means automatic selection.
- `FALCOCTL_ENABLED=no` disables automatic rules updates from falcoctl; any other value keeps them.
- `FALCOCTL_DRIVER_VERSION` pins the driver version during an upgrade.

```shell
FALCO_FRONTEND=noninteractive FALCOCTL_ENABLED=no apt-get install -y falco
```

apt: trust the key with `curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | sudo gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg`, add `deb [signed-by=/usr/share/keyrings/falco-archive-keyring.gpg] https://download.falco.org/packages/deb stable main` under `/etc/apt/sources.list.d/falcosecurity.list`, run `apt-get update -y`, install `dkms make linux-headers-$(uname -r)`, then `apt-get install -y falco`.

yum: `rpm --import https://falco.org/repo/falcosecurity-packages.asc`, fetch `https://falco.org/repo/falcosecurity-rpm.repo` to `/etc/yum.repos.d/falcosecurity.repo`, install `dkms make` and `kernel-devel-$(uname -r)`, then `yum install -y falco`.

Gotcha: with UEFI SecureBoot, enrol the DKMS key with `mokutil --import /var/lib/dkms/mok.pub`, reboot, choose Enroll MOK, then `insmod` the module.

## Checked

2026-11-08. Read the cited packages page in full (including the Kernel Upgrades, package signing and troubleshooting sections) and found the draft accurate; no content change.

Method: documentation only; no commands were run.
