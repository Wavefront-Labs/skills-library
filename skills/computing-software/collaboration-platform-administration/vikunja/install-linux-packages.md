---
id: computing-software.collaboration-platform-administration.vikunja.install-linux-packages
name: install-linux-packages
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, apt-repository, dnf-repository, alpine-apk, package-config-path]
level: practitioner
status: docs-checked
description: "Install Vikunja from the official deb, rpm and Alpine package repositories, choose stable or unstable, and find the packaged config file."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Package repositories are available from 2.4.0. All use a `stable` channel; replace it with `unstable` to track the main development branch.

Debian/Ubuntu (`amd64`, `arm64`, `armhf`): import `https://dl.vikunja.io/repos/gpg.key` with `gpg --dearmor` into `/usr/share/keyrings/vikunja.gpg`, add `deb [signed-by=/usr/share/keyrings/vikunja.gpg] https://dl.vikunja.io/repos/apt stable main` to `/etc/apt/sources.list.d/vikunja.list`, then `apt update && apt install vikunja`. A downloaded file installs with `dpkg -i vikunja.deb`.

Fedora/RHEL (`x86_64`, `aarch64`, `armv7`): a `/etc/yum.repos.d/vikunja.repo` with `baseurl=https://dl.vikunja.io/repos/rpm/stable/$basearch`, `gpgcheck=1`, `gpgkey=https://dl.vikunja.io/repos/gpg.key`, then `dnf install vikunja`. Direct file: `rpm -i vikunja.rpm`.

Alpine (`x86_64`, `aarch64`, `armv7`): download `https://dl.vikunja.io/repos/apk/vikunja-apk.rsa.pub` into `/etc/apk/keys/`, append `https://dl.vikunja.io/repos/apk/stable/main` to `/etc/apk/repositories`, `apk update && apk add vikunja`.

The deb installs to `/opt/vikunja`. Configure through `/etc/vikunja/config.yml`, and set `service.publicurl` or disable CORS.

## Checked

2026-11-04. Confirmed against the Vikunja Installing page (setup/install, Debian, RPM and Alpine sections): 2.4.0 availability, architectures, repository and key URLs, apt, dnf and apk steps, stable and unstable channels, direct package installs, /opt/vikunja and /etc/vikunja/config.yml. Nothing removed.

Method: documentation only; no commands were run.
