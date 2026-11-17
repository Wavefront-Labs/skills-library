---
id: computing-software.systems-network-administration.headscale.community-and-source-installs
name: community-and-source-installs
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, community, arch, nixos, openbsd, source-build]
level: intro
status: docs-checked
description: "Where community-packaged Headscale exists (Arch, Fedora COPR, Nix, Gentoo, OpenBSD) and how the OpenBSD source and cross build is done."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/community.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/source.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Community packages and source builds

Community packages are alternatives to the official releases. They usually set up a dedicated local user, provide a default configuration and install headscale as a system service, but may be outdated or unmaintained; use the official releases for the current stable version.

| Platform | Route |
|---|---|
| Arch Linux | `pacman` |
| Fedora, RHEL, CentOS | third-party COPR repository |
| Nix/NixOS | `headscale` package |
| Gentoo | `emerge --ask net-vpn/headscale`, plus a community wiki guide |
| OpenBSD | `pkg_add headscale` (ports); installs the service with `rc.d` |

## Building on OpenBSD (community docs)

Community documentation, not verified by the headscale developers and possibly outdated or missing steps. Headscale builds from source with the latest Go and Buf (Protobuf generator).

1. Install Go and Git with `pkg_add go git`.
2. Clone the repo and check out a release tag (the latest tag may be a beta).
3. Build with `go build`, setting the version and commit through `-ldflags`.
4. Make the binary executable and copy it to `/usr/local/sbin`.

## Cross-compiling

Install a recent Go (see the `go` directive in `go.mod` for the exact minimum) and `gmake` (the Makefile is written in GNU make syntax), check out a release tag, run `make build GOOS=openbsd`, then copy the headscale binary to the OpenBSD machine and put it in `/usr/local/sbin`.

Note: in the docs' native `go build` command the quotes around the `-ldflags` value are unbalanced (around the `GitCommitHash` flag); fix them before use.

## Checked

2026-11-04. Confirmed against the Headscale docs pages for community packages and build from source (package commands, COPR, Gentoo, OpenBSD steps, cross-compile). Added the exact install commands and the quoting caveat of the native build command.

Method: documentation only; no commands were run.
