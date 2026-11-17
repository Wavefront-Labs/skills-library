---
id: computing-software.devops-ci-cd.packer.plugin-creation-overview
name: plugin-creation-overview
category: computing-software
field: devops-ci-cd
product: packer
tags: [plugin-development, sdk, go, rpc, plugin-creation]
level: advanced
status: docs-checked
description: "How Packer plugins are built in Go with the plugin SDK and what component types they can provide."
sources:
  - "https://developer.hashicorp.com/packer/docs/plugins/creation/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Packer plugins must be written in Go. A plugin is a Go binary that Packer runs as a separate process; the plugin processes talk to the Packer core over an RPC defined in the packer-plugin SDK, and the core launches and cleans them up. The docs call this an advanced topic.

A plugin can supply builders, provisioners, post-processors and data sources. Each has a Go interface. To make a plugin you implement the interface and serve it with the server in `github.com/hashicorp/packer-plugin-sdk`, using two SDK packages:

- `github.com/hashicorp/packer-plugin-sdk/packer` holds the interfaces you implement.
- `github.com/hashicorp/packer-plugin-sdk/plugin` holds the code that serves the plugin and handles inter-process communication.

`main` builds a set with `plugin.NewSet()`, registers components (`RegisterBuilder`, `RegisterPostProcessor`, `RegisterProvisioner`) and calls `Run()`. A component registered with a name gets the plugin name prepended: in a plugin named `packer-plugin-my`, a builder registered as `example` is the `my-example` builder. Registering with `plugin.DEFAULT_NAME` makes it available as just `my`. Because plugins are separate processes, dependency versions cannot collide; the docs recommend locking dependencies with `go mod`.

Naming: name the plugin application `packer-plugin-NAME`.

Releasing for `packer init`: there is no central registry. Publish the plugin in a GitHub repository named `packer-plugin-*` and create a GitHub release with the specific assets `packer init` downloads. The docs recommend the GoReleaser configuration and GitHub Actions release workflow from the `packer-plugin-scaffolding` repository, with `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE` repository secrets, then pushing a version tag that is a valid semantic version preceded by `v` (for example `v1.2.3`).

Local testing: install a built binary with `packer plugins install --path <path-to-binary> <hostname>/<namespace>/<plugin-name>`, then optionally list it in `required_plugins`.

Debugging: plugins can use the standard Go `log` package. Output goes to the Packer log, visible on stderr when `PACKER_LOG` is set, with each line prefixed by the plugin path.

Discovery: to be listed as a Packer Integration the plugin needs the scaffolding documentation layout, a `metadata.hcl` in `.web-docs`, and an integration request issue with the Packer team.

## Checked

2026-11-09. Checked against the Packer v1.15 "Create custom plugins to extend Packer" page: Go requirement, process and RPC architecture, the two SDK packages, name registration and `plugin.DEFAULT_NAME` behaviour, `packer-plugin-*` naming, release workflow and secrets, the `--path` install command, `PACKER_LOG` logging and the integration registration steps.

Removed as unsupported by that page: the requirement for a shasums file alongside the binaries (the page only says specific assets, produced by the GoReleaser configuration), the claim that a crash is isolated from the core, and the remark about the older `packer-builder-*` custom-binary pattern.

Method: documentation only; no commands were run.
