---
id: computing-software.devops-ci-cd.skaffold.cli-commands-overview
name: cli-commands-overview
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [cli, commands, flags, help]
level: intro
status: docs-checked
description: "The Skaffold command list and the flags that most pipelines rely on."
sources:
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The CLI reference groups the commands like this:

- End-to-end pipelines: `run`, `dev`, `debug`.
- Pipeline building blocks: `build`, `test`, `deploy`, `delete`, `render`, `apply`, `verify`.
- Getting started: `init`.
- Other: `completion` (bash, fish or zsh), `config`, `diagnose`, `exec` (run a custom action), `fix`, `schema`, `version`, and `options` (lists the global flags).

Flags worth knowing, with the commands where they apply:

- `build`: `-b` / `--build-image` (build only artifacts whose image name contains the substring), `--cache-file` (default `$HOME/.skaffold/cache`), `--dry-run` (only compute tags), `--file-output`, `-q` / `--quiet`, `--platform`, `--push`, `-t` / `--tag`.
- `deploy`, `render`, `test` and `verify`: `-a` / `--build-artifacts` (a build result file, for example from `build --file-output`). `deploy`, `apply`, `run` and `dev`: `--status-check`.
- `delete`: `--dry-run`.
- Common to most commands: `-f` / `--filename` (config file, default `skaffold.yaml`), `-p` / `--profile`, `-n` / `--namespace`, `--kube-context`, `-m` / `--module`, `-d` / `--default-repo`.

Each command's reference section lists an environment variable form `SKAFFOLD_<FLAG>` for its flags, for example `SKAFFOLD_DEFAULT_REPO` for `--default-repo` and `SKAFFOLD_PROFILE` for `--profile`.

Support commands:

- `skaffold diagnose` searches for configuration issues and prints the effective configuration; `skaffold diagnose --yaml-only --profile PROFILE` prints only the effective `skaffold.yaml` for that profile.
- `skaffold fix` updates an old configuration to a newer schema version.
- `skaffold schema` lists the JSON schemas used to validate `skaffold.yaml` (`schema get` prints one).
- `skaffold completion` outputs shell completion.
- `skaffold version` prints the version information.

Run `skaffold <command> --help` for the exact flags of your version.

Tip: keep flags that rarely change in `skaffold.yaml` or `SKAFFOLD_` environment variables, and reserve the command line for values that differ per run, such as the profile, the tag and the namespace.

## Checked

2026-11-04. Read the Skaffold CLI reference (command groups, and the sections for build, deploy, render, test, verify, apply, delete, diagnose and schema). Confirmed the command list, the flag names and defaults above, the env var naming pattern and the diagnose example. Removed: the claim that every flag has a `SKAFFOLD_` form (the page lists them per command), and the "fix upgrades the apiVersion" wording (the page says it updates configuration to a newer schema version).
Method: documentation only; no commands were run.
