---
id: computing-software.systems-network-administration.incus.install-client-macos-windows
name: install-client-macos-windows
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, client, macos, windows, homebrew, colima, chocolatey, winget]
level: intro
status: docs-checked
description: "Install only the Incus client on macOS (Homebrew, Colima) or Windows (Chocolatey, Winget) or from GitHub binaries."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/installing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incus client on macOS and Windows

Builds for other operating systems include only the client, not the server. Point the client at a server with `incus remote add`.

- macOS, Homebrew: `brew install incus`.
- macOS, Colima (Incus is supported as a runtime): `brew install colima`, then `colima start --runtime incus`.
- Windows, Chocolatey: `choco install incus`.
- Windows, Winget: `winget install LinuxContainers.Incus`.
- Any platform: native client builds for Linux, FreeBSD, macOS and Windows (aarch64 and x86_64) are linked from the installing page on GitHub.
- FreeBSD: `pkg install incus-client`.

## Checked

2026-11-09. Confirmed against the Incus doc installing.md (Other operating systems): client-only note, Homebrew, Colima, Chocolatey, Winget, FreeBSD package and native build links. Removed: the Linux-server-only claim, the Colima Linux VM wording and the client config path line, which this page does not state.

Method: documentation only; no commands were run.
