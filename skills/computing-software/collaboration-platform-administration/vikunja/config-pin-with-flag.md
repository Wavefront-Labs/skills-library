---
id: computing-software.collaboration-platform-administration.vikunja.config-pin-with-flag
name: config-pin-with-flag
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, config-flag, rootpath-anchoring, working-directory, doctor-migrate]
level: advanced
status: docs-checked
description: "Use vikunja --config to pin one config file for CLI commands so rootpath, files and the SQLite database resolve inside the install, not the shell's directory."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--config <file>` pins one specific config file and skips the search path. It works on every command and has no shorthand.

```
vikunja doctor --config /opt/vikunja/config.yml
vikunja migrate --config /opt/vikunja/config.yml
```

If the file cannot be read, Vikunja exits with an error instead of falling back to defaults.

Why use it: run from a different working directory than the install, Vikunja may find no config, use defaults and resolve relative paths against your shell directory, making a working install look empty.

Anchoring rules for a pinned config:
- If `service.rootpath` is unset, it defaults to the directory containing the config file, so relative paths such as `files.basepath` resolve inside the install.
- A relative `service.rootpath` is resolved against the config file's directory.
- If `database.path` is unset, its default resolves against that anchored rootpath, keeping SQLite with the install.
- Environment variables still win: `VIKUNJA_SERVICE_ROOTPATH` and `VIKUNJA_DATABASE_PATH` override these, and values set explicitly in the pinned file beat the anchored defaults.

## Checked

2026-11-04: every statement checked against the config page, section "Pinning a config file with --config".

Method: documentation only; no commands were run.
