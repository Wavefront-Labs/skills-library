---
id: computing-software.collaboration-platform-administration.vikunja.stable-vs-unstable-releases
name: stable-vs-unstable-releases
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, stable-release, unstable-build, docker-tags, semantic-versioning]
level: practitioner
status: docs-checked
description: "Choose between Vikunja stable and unstable builds, read unstable version strings, and switch safely including the one-way risk of going back to stable."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/versions.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stable releases have fixed Semantic Versioning numbers, come out at irregular intervals and get few bugfixes and security patches.

Unstable builds are made on every merged PR or commit to the main branch, possibly several a day, so they are more likely to have bugs. Their version looks like the last stable version, the number of commits since, and the commit hash (for example `v0.20.2-75-6049427322`). It may look older than the latest release because only some changes are backported to patch releases; trust the commit hash.

Switch versions the way you upgrade: back up first, replace the binary, restart. With Docker use the `unstable` or `latest` tag.

Stable to unstable should work. Unstable back to stable might break your instance and is not recommended; wait for the next stable release after your unstable build and upgrade to that.

The demo at try.vikunja.io runs the latest unstable build.

Upgrades run database migrations automatically; read the changelog for manual steps.

## Checked

2026-11-04. Confirmed against the Vikunja Versions page (setup/versions) and the Installing page (Updating section): stable and unstable definitions, version string format and the backport explanation, demo instance, switching steps, Docker tags, the stable-to-unstable and back warning, and automatic migrations. Nothing removed.

Method: documentation only; no commands were run.
