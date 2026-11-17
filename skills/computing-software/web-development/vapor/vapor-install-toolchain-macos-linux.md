---
id: computing-software.web-development.vapor.vapor-install-toolchain-macos-linux
name: vapor-install-toolchain-macos-linux
category: computing-software
field: web-development
product: vapor
tags: [vapor, swiftly, vapor-toolbox, install, swift, homebrew, macos, linux]
level: intro
status: docs-checked
description: "Install Swift (Xcode, Swiftly or toolchain) and the Vapor Toolbox on macOS or Linux, via Homebrew or a Makefile build."
sources:
  - https://docs.vapor.codes/install/macos/
  - https://docs.vapor.codes/install/linux/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get Swift 5.9 or newer plus the optional `vapor` CLI (Vapor Toolbox).

## Swift on macOS
Swift ships inside Xcode. Install Xcode from the Mac App Store, open it once to finish installation (can take a while), then run `swift --version` in Terminal. Vapor 4 requires Swift 5.9 or greater.

## Swift on Linux
- Recommended: Swiftly, the CLI from the Swift Server Workgroup (install per https://swiftlang.github.io/swiftly/), then `swiftly install latest` and `swift --version`.
- Alternative: toolchains from Swift.org (see its "Using Downloads" guide).
- Fedora: `sudo dnf install swift-lang`. On Fedora 35 add EPEL 8 to get Swift 5.9 or newer.
- Docker: Swift's official images come with the compiler preinstalled.
- Vapor supports the Linux distributions and versions that Swift 5.9+ supports (see swift.org/platform-support). Unsupported distros may run Swift compiled from source, but Vapor cannot vouch for stability.

## Vapor Toolbox (both OSes, not required, helps create projects)
Homebrew:
```sh
brew install vapor
vapor --help
```
Makefile (from source; pick a version from the toolbox GitHub releases):
```sh
git clone https://github.com/vapor/toolbox.git
cd toolbox
git checkout <desired version>
make install
vapor --help
```
`vapor --help` should list the available commands.

Next: create the first app (see vapor-new-project-build-run).

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) install/macos, install/linux, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
