---
id: computing-software.collaboration-platform-administration.vikunja.build-from-source
name: build-from-source
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, pnpm-build, mage-build, go-toolchain, cross-compile]
level: advanced
status: docs-checked
description: "Build Vikunja from source: check out a release tag, build the frontend with pnpm, build the Go binary with Mage and cross-compile with mage release."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/build-from-source.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prepare: install git, clone `https://code.vikunja.io/vikunja`, and `git checkout VERSION`. Without a checkout you build the latest unstable code.

Frontend (in `frontend/`): install pnpm, run `pnpm install`, then `pnpm run build`. It produces a static bundle in `dist/`, which you can deploy directly or embed in the binary.

API: needs Go (at least 1.21 per the page) and Mage. If you did not build the frontend, create a dummy index: `mkdir -p frontend/dist && touch frontend/dist/index.html`. Run `mage build` in the repo root; it writes a binary there for your platform.

Other platforms: `mage release` or `mage release:{linux|windows|darwin}`; see the magefile docs for more.

## Checked

2026-11-04. Confirmed against the Vikunja Build from sources page (setup/build-from-source): clone and checkout, unstable build warning, pnpm install and build into dist/, Go 1.21 minimum, Mage, dummy index file, mage build output, mage release options. Removed: the VIKUNJA_FRONTEND_BASE subpath claim and the Go-requirement advice, which the page does not state.

Method: documentation only; no commands were run.
