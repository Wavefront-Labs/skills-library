---
id: computing-software.systems-network-administration.restic.install-packages
name: install-packages
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, installation, packages, package-manager, windows, macos]
level: intro
status: docs-checked
description: "Install restic from OS package managers or official binaries and confirm the install with restic version."
sources:
  - https://restic.readthedocs.io/en/stable/020_installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install restic from packages

If a distribution package is outdated, the docs say to use an official binary instead.

Commands per platform:

- Alpine: `apk add restic`
- Arch: `pacman -S restic`
- Debian: `apt-get install restic`
- Fedora: `dnf install restic`
- Gentoo: `emerge restic`
- macOS: `brew install restic` (alternatives: `pkgx install restic`, `sudo port install restic`)
- OpenBSD: `pkg_add restic`; FreeBSD: `pkg install restic`
- openSUSE: `zypper install restic`
- RHEL and CentOS Stream: `dnf install epel-release`, then `dnf install restic`
- Solus: `eopkg install restic`
- Mise: `mise use -g restic@latest`
- Windows: `scoop install restic`, or `winget install --exact --id restic.restic --scope Machine`

On NixOS add `pkgs.restic` to `environment.systemPackages` in `configuration.nix`.

## WinGet scope

The default WinGet scope is User. `--scope Machine` installs under `%ProgramFiles%` and needs an elevated shell.

## Official binaries

Stable releases and unstable builds are published as binaries. Release files come with a `SHA256SUMS` checksum list and a `SHA256SUMS.asc` PGP signature, so check both before running a downloaded binary.

Run `restic version` to see which build you have.

## Checked

2026-11-03. Confirmed in the restic docs page Installation (Packages, Windows, Official binaries): every install command listed above, the pkgx and MacPorts alternatives, the NixOS snippet, the WinGet User default and `--scope Machine` to `%ProgramFiles%` needing elevation, `SHA256SUMS` and `SHA256SUMS.asc`. Removed: the advice to prefer distribution packages and the `which restic` shadowing tip (not in the docs).

Method: documentation only; no commands were run.
