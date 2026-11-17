---
id: computing-software.cloud-infrastructure-engineering.openbao.install-openbao
name: install-openbao
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, install, package-manager, container-images, precompiled-binary]
level: intro
status: docs-checked
description: "Install OpenBao via package manager, container image, precompiled bao binary or source build, and confirm it works with bao -h."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing OpenBao

## Package managers

- macOS Homebrew: `brew install openbao`
- FreeBSD: `pkg install openbao`
- Arch Linux: `pacman -Sy openbao` (plugins: `pacman -Ss ^openbao-plugin`)
- RHEL and derivatives: `dnf install -y epel-release` then `dnf install -y openbao`
- Amazon Linux, Debian, Fedora, RHEL and Ubuntu packages are on the downloads page.

## Containers

Alpine-based images: `ghcr.io/openbao/openbao`, `quay.io/openbao/openbao`, `docker.io/openbao/openbao`. RHEL UBI images use the same registries with the name `openbao-ubi`.

## Binary

Download the zip for your system and unzip it. The `bao` binary (`bao.exe` on Windows) is all you need; put it on your `PATH`.

## From source

For a development build only (release binaries follow the packaging guide). Needs Go with `GOPATH` set and `git`. Clone into `$GOPATH/src/github.com/openbao`, run `make bootstrap`, then `make dev`; the local-environment binary lands in `./bin/`.

## Verify

```
bao -h
```

Help output means the install works. Before trusting a download, check signatures (see verify-release-signatures) and consider swap hardening (see disable-swap).

## Checked

2026-11-04. Confirmed against the Installing OpenBao page: package manager commands, the six container image registries, binary download, source build steps and the bao -h check. Nothing removed.

Method: documentation only; no commands were run.
