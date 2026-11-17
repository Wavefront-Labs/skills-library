---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-cli-setup
name: woodpecker-cli-setup
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [cli, setup, contexts]
level: intro
status: docs-checked
description: "Install and configure woodpecker-cli: setup, contexts, token storage and precedence."
sources: ["https://woodpecker-ci.org/docs/cli/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker CLI installation and setup

Install the CLI from a Woodpecker release, package or the `woodpecker-cli` container image (installation steps are not covered in the cited page; check the release notes).

Connect to a server:

```shell
woodpecker-cli setup --server https://ci.example.test
woodpecker-cli info
```

`setup` opens the UI in your browser to confirm the login and saves the server and token as a context. Use `woodpecker-cli setup --context <name>` per server and switch with `woodpecker-cli context use`.

Contexts live in `~/.config/woodpecker/contexts.json` on Linux, with `XDG_CONFIG_HOME` overriding the base. Tokens are never written there; they go to the operating system keyring.

Precedence: flags (`--server`, `--token`, `--log-level`), then their `WOODPECKER_*` environment variables, then the stored context. Legacy `config.json` is deprecated.

## Checked

2026-11-03. Read the Woodpecker CLI configuration page and confirmed setup with --server and --token, info, contexts and context use, contexts.json location with XDG_CONFIG_HOME, tokens kept in the OS keyring, flag then environment then context precedence, legacy config.json deprecation. Removed: the release download, checksum, update and container-image installation steps, which the cited page does not document. 

Method: documentation only; no commands were run.
