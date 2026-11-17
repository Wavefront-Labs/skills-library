---
id: computing-software.messaging-and-integration.temporal.cli-dev-server-setup
name: cli-dev-server-setup
category: computing-software
field: messaging-and-integration
product: temporal
tags: [temporal-cli, start-dev, dev-server, db-filename, headless, https-proxy, docker, completion]
level: intro
status: docs-checked
description: "Install the Temporal CLI and run temporal server start-dev: default ports, db-filename, namespaces, headless, dynamic config values, Docker, proxy and completion."
sources:
  - https://docs.temporal.io/cli/setup-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install the `temporal` CLI with `brew install temporal`, from the CDN archive (macOS, Linux, Windows; put `temporal` or `temporal.exe` on PATH), or as the `temporalio/temporal` Docker image. Cloud users add the Public Preview extension with `brew install temporalio/brew/temporal-cloud`.

Dev server: `temporal server start-dev` starts a full Temporal Service with the Web UI, the `default` Namespace and an in-memory SQLite database. gRPC listens on `localhost:7233` and the UI on `http://localhost:8233`.
- Persist data: `--db-filename temporal.db`.
- Pre-register Namespaces: `--namespace foo --namespace bar`; later ones with `temporal operator namespace create --namespace foo`.
- Disable the UI: `--headless`.
- Set dynamic config inline: `--dynamic-config-value KEY=JSON_VALUE`, for example `system.forceSearchAttributesCacheRefreshOnRead=false` makes new Search Attributes visible immediately.
- In Docker, expose it to the host: `docker run --rm -p 7233:7233 -p 8233:8233 temporalio/temporal server start-dev --ip 0.0.0.0`.

Settings can come from environment variables or TOML config files; `temporal env` instead writes named key-value presets to a file. Behind a proxy set `HTTPS_PROXY=<host>:<port>` (gRPC also honors `NO_PROXY`). Shell completion: add `eval "$(temporal completion zsh)"` to `~/.zshrc`, or the same with `bash` in `~/.bashrc` (needs bash-completion); for fish write `eval "$(temporal completion fish)"` to `~/.config/fish/completions/temporal.fish`. Help: `temporal <command> <subcommand> --help`; the full command list is in the CLI command reference.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: cli/setup-cli (under https://docs.temporal.io/). Removed the everyday-commands list (workflow, schedule and cloud login examples) and the dead cli/cli-basics source; they were not on the page.

Method: documentation only; no commands were run.
