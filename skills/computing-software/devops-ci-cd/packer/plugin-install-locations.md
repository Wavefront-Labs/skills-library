---
id: computing-software.devops-ci-cd.packer.plugin-install-locations
name: plugin-install-locations
category: computing-software
field: devops-ci-cd
product: packer
tags: [plugin-path, config-dir, xdg, tmpdir, plugins-install, configure]
level: practitioner
status: docs-checked
description: "Where Packer looks for and installs plugins, and the env vars PACKER_PLUGIN_PATH, PACKER_CONFIG_DIR and TMPDIR."
sources:
  - https://developer.hashicorp.com/packer/docs/plugins/install
  - https://developer.hashicorp.com/packer/docs/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Plugins are installed to a `plugins` directory under the Packer config directory.

- Unix default config directory: `$HOME/.config/packer/`. Packer follows the XDG base directory spec, so this is used when `PACKER_CONFIG_DIR` is unset or empty. With `PACKER_CONFIG_DIR` set (or a legacy `.packer.d`-style layout) XDG is ignored.
- Windows: `%APPDATA%\packer.d\`.
- Example: with `PACKER_CONFIG_DIR` set to a directory D on Unix, the config directory is `D/.packer.d/`; on Windows it is `D\packer.d\`.
- Default plugin directories: `$HOME/.config/packer/plugins` on Unix and `%APPDATA%\packer.d\plugins` on Windows; `PACKER_PLUGIN_PATH` selects a different one and takes precedence over `PACKER_CONFIG_DIR/plugins` for discovery.
- Installation needs temporary files under `TMPDIR` (Unix) or `TMP`, `TEMP`, `USERPROFILE` (Windows). If the temp directory is non-writable or non-executable, set `TMPDIR` elsewhere.

When you build, Packer checks the plugin directory against `required_plugins`; manually installed plugins must still satisfy the template's constraints. `packer plugins installed` lists the installed plugins.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Packer 1.15 "Installing plugins" and "Configure Packer" pages. Removed as not on those pages: the CI cache advice and the closing troubleshooting paragraph.
