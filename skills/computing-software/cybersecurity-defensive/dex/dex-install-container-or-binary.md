---
id: computing-software.cybersecurity-defensive.dex.dex-install-container-or-binary
name: dex-install-container-or-binary
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [install, container, binary, helm]
level: intro
status: docs-checked
description: "Install Dex from the ghcr.io or docker.io image, a Helm chart or a source build, and start it with a single YAML config file."
sources:
  - https://dexidp.io/docs/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex is distributed mainly as a container image, published to `ghcr.io/dexidp/dex` and `docker.io/dexidp/dex`. Two variants exist, one based on Alpine Linux and one on Distroless. A reference Helm chart is published at charts.dexidp.io.

To build from source you need a Go toolchain (the docs name Go 1.19 or newer):

```bash
git clone https://github.com/dexidp/dex.git
cd dex/
make build
```

Dex takes all configuration from a config file only. Start it with the bundled development example, which uses a sqlite3 data store and predefined OAuth2 clients:

```bash
./bin/dex serve examples/config-dev.yaml
```

The example file documents many options through inline comments, so read it for options not covered in the docs pages.

Gotcha: Dex exclusively pulls configuration options from a config file, the YAML file passed to `dex serve`.

## Checked

2026-11-08: Read the Dex Getting Started page in full. Confirmed the image locations, the two image variants, the Helm chart location, the Go 1.19 requirement, the build commands, config-file-only configuration and the `dex serve examples/config-dev.yaml` command. Removed the discovery check, which that page attributes to the example app only.
Method: documentation only; no commands were run.
