---
id: computing-software.web-development.appwrite.appwrite-cli-install-and-ci
name: appwrite-cli-install-and-ci
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, cli, ci, non-interactive, deploy]
level: practitioner
status: docs-checked
description: "Install the Appwrite CLI, log in, and run non-interactive pushes in CI with a project API key."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/tooling/command-line/installation/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/tooling/command-line/non-interactive/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: operate Appwrite from the terminal and pipelines.

Install: `npm install -g appwrite-cli` (npm module), `brew install appwrite` (macOS), `iwr -useb https://appwrite.io/cli/install.ps1 | iex` or Scoop (Windows), or the installation script for macOS and Linux. A standalone binary also exists. If you will use the CLI to initialize Functions, Git must be installed. Confirm with `appwrite -v`.

Interactive: `appwrite login` signs in through your browser using device authorization. Add `--endpoint "https://<HOST>/v1"` for a self-hosted server (include the `/v1` path); self-hosted instances do not support the OAuth login, so the CLI asks for email and password. Then `appwrite init project` creates `appwrite.config.json`. If the CLI keeps pointing at a self-hosted instance, delete the saved `prefs.json` in the `.appwrite` folder of your home directory. `appwrite login --switch` returns to a saved account.

CI (non-interactive) with a project API key:
1. `appwrite client --endpoint https://<REGION>.cloud.appwrite.io/v1 --project-id <PROJECT_ID> --key <API_KEY>`. These global settings take precedence over `appwrite.config.json`, and the CLI can then work with only one project at a time. The key needs permissions for the commands you run.
2. Push without prompts using `--force`, which skips warnings: `appwrite push all --all --force`, `appwrite push functions --function-id <FUNCTION_ID> --force`, `appwrite push functions --all --force`, `appwrite push tables --all --force`, `appwrite push teams --all --force`, `appwrite push buckets --all --force`. The docs list functions, tables, buckets, teams and messaging topics as pushable.

Other commands: `pull` pulls project, functions, tables, buckets, teams and topics; `init` creates and initializes them; `run` runs projects locally. The CLI has a command for every Server API endpoint, in the form `appwrite [COMMAND] [OPTIONS]`.

Gotcha: `--force` skips warnings, so run it only from trusted pipelines. Keep `<API_KEY>` in the CI secret store.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages CLI Installation, CLI Non-interactive and CLI Commands: install methods, `appwrite -v`, login and `--endpoint` behaviour, `prefs.json` location, `client` flags and precedence, push forms, and the command table. Corrected: `appwrite init` is `appwrite init project`. Removed: the unverified "Console shows updated resources" check and the claim that `appwrite push all` covers more than the listed resource types.
Method: documentation only; no commands were run.
