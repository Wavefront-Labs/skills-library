---
id: computing-software.devops-ci-cd.packer.plugins-subcommands
name: plugins-subcommands
category: computing-software
field: devops-ci-cd
product: packer
tags: [plugins, install, installed, remove, required, cmd-plugins, cmd-plugins-install, cmd-plugins-remove]
level: practitioner
status: docs-checked
description: "Manage plugin binaries with packer plugins install, installed, remove and required."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/plugins/"
  - "https://developer.hashicorp.com/packer/docs/commands/plugins/install/"
  - "https://developer.hashicorp.com/packer/docs/commands/plugins/remove/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer plugins` groups subcommands for installing, uninstalling and viewing plugins:

- `install`: install the latest Packer plugin, optionally matching a version constraint.
- `installed`: list all installed plugin binaries.
- `remove`: remove plugins, optionally matching a version.
- `required`: list plugins required by a config.

`packer init <path>` is related but separate: it installs all plugins required by a config.

## install

Downloads and installs the most recent version of a plugin binary, without needing a template.

```bash
packer plugins install github.com/hashicorp/my-plugin 1.0.1
packer plugins install --path my-plugin github.com/hashicorp/my-plugin
```

- `<plugin-binary-source>`: a remote source; to download remotely the plugin must be hosted on GitHub. For local binaries also pass `--path`.
- `<plugin version>`: semantic version in `<major>.<minor>.<patch>` format; omitted means latest.
- `--path` installs from a local binary (required for local sources); `--force` forces reinstallation.
- Default plugin directory: `$HOME/.config/packer/plugins` on Unix and `%APPDATA%\packer.d\plugins` on Windows; override with the `PACKER_PLUGIN_PATH` environment variable.
- Installation needs temporary files under `TMPDIR`; if the system temp directory is non-writable or non-executable, set `TMPDIR` to override.
- HashiCorp only verifies plugins from GitHub under the `hashicorp/*` namespace; vet any third-party plugin yourself.
- From 1 August 2025 the source for many official HashiCorp plugins moved from GitHub releases to releases.hashicorp.com.

## remove

- A source address without a version constraint removes all versions of that plugin (for the current OS and architecture).
- A version constraint removes only the specified version.
- An absolute path to an installed binary removes just that binary; this syntax does not allow version matching.

```bash
packer plugins remove github.com/hashicorp/happycloud v1.2.3
packer plugins remove github.com/hashicorp/happycloud
packer plugins installed | xargs -n1 packer plugins remove
```

The last command (Unix with xargs) removes every installed plugin version.

## Checked

Method: docs-checked 2026-11-09 against the Packer `packer plugins` command group page, the `plugins install` page and the `plugins remove` page (all read in full as published page source). Dropped unconfirmed claims about SHA256SUM generation and how `installed` and `required` order and filter results.
