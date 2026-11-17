---
id: computing-software.devops-ci-cd.atlantis.atlantis-comment-commands
name: atlantis-comment-commands
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [atlantis, plan, apply, import, state-rm, unlock, cancel, pull-request-comments]
level: practitioner
status: docs-checked
description: "Run Atlantis plan, apply, import, state rm, unlock, cancel and approve_policies from pull request comments with the right targeting flags."
sources: ["https://www.runatlantis.io/docs/using-atlantis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis comment commands

Atlantis runs commands from pull request comments. A command can be prefixed with `atlantis`, `run`, or `@GithubUser`.

- `atlantis plan [options] -- [terraform plan flags]` plans the PR branch. With no options it plans the projects Atlantis detects as modified (using `when_modified` if an `atlantis.yaml` exists). A bare `atlantis plan` discards plans previously created with `-p`, `-d` or `-w`.
- Targeting: `-d directory` (relative to repo root, `.` for root), `-p project` (name from `atlantis.yaml`; cannot be combined with `-d` or `-w`), `-w workspace` (default `default`). `--verbose` appends the Atlantis log.
- Extra Terraform flags go after `--`. Blocked after `--`: `-chdir`, `-plugin-dir`, `-out`, `-generate-config-out`, `-state`, `-state-out`, `-backup` and anything in `--blocked-extra-args`. `-var-file` paths must be inside the repo or in `--var-file-allowlist`.
- If `env/{workspace}.tfvars` exists relative to the project directory, Atlantis passes it as `-var-file` automatically.
- `-- -destroy` makes a destroy plan; applying it can cause data loss.

`atlantis apply` applies the plan matching the directory, project or workspace; with no targeting it applies all unapplied plans on the PR. Flags that change the plan (`-target`, `-var`) are ignored at apply because the saved plan file is used; set them at plan time. Options: `--auto-merge-disabled`, `--auto-merge-method method` (GitHub only).

`atlantis import ADDRESS ID` and `atlantis state rm ADDRESS...` need `--allow-commands` on the server, discard the plan result (re-plan afterwards) and require the project's requirements. Quote `for_each` addresses such as `'aws_instance.example["foo"]'`.

`atlantis cancel` cancels queued (not running) commands. `atlantis unlock` removes all locks on the PR and discards its plans. `atlantis approve_policies` approves current policy failures. `atlantis version` prints the Terraform version.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Using Atlantis. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
