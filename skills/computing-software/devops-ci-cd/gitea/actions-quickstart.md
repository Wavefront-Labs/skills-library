---
id: computing-software.devops-ci-cd.gitea.actions-quickstart
name: actions-quickstart
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-quickstart, gitea, actions, workflow-yaml, enable-repository-actions, gitea-workflows-dir, runner-registration]
level: intro
status: docs-checked
description: "Get Gitea Actions running end to end: enable at instance and repository level, register a runner, add a workflow under .gitea/workflows, and avoid the MySQL emoji error."
sources: ["https://docs.gitea.com/usage/actions/quickstart/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Actions quick start

Needs Gitea 1.19.0 or higher. Since 1.21.0 Actions are on by default; before that, set `ENABLED=true` under `[actions]` in `app.ini`.

## Steps
1. Run a runner on a separate machine from Gitea to avoid starving it. Test it first as a plain command-line binary, then move to Docker or a service. Docker is recommended for job isolation, but the runner can also run jobs directly on the host.
2. Register: `gitea-runner register --no-interactive --instance <instance> --token <token>`. `instance` is the address that the runner and its job containers will connect to; it may differ from `ROOT_URL`, and loopback addresses (`127.0.0.1`, `localhost`) are a bad idea, so use the LAN address when unsure. One token can create many runners until it is reset.
3. Registration writes a `.runner` file in the working directory. Do not edit it; if missing or corrupt, delete it and register again.
4. Start: `gitea-runner daemon`. The runner then shows on the management page.
5. **A repository still has Actions disabled by default** even when the instance enables them: tick `Enable Repository Actions` in the repository settings.
6. Commit a workflow file, extension `.yaml`, into `.gitea/workflows/` (for example `.gitea/workflows/demo.yaml`). With `on: [push]`, uploading the file itself pushes a commit and triggers the first run, visible on the Actions tab.

The workflow syntax follows GitHub Actions, and the demo uses `runs-on: ubuntu-latest`, `actions/checkout@v4`, and the `gitea` context such as `${{ gitea.actor }}` and `${{ gitea.event_name }}`.

## Failure modes
- The docs' demo contains emojis. On MySQL without the `utf8mb4` charset the run fails with `Error 1366 (HY000): Incorrect string value`. Fix the database charset (see `gitea-database-prep`) or strip the emojis.
- Some actions, including `actions/checkout`, may misbehave in SHA256 repositories or when Gitea is served from a sub-path.

## Checked

2026-11-03: read https://docs.gitea.com/usage/actions/quickstart/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
