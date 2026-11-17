---
id: computing-software.devops-ci-cd.gitea.actions-runner
name: actions-runner
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-act-runner, gitea, runner-registration-token, runner-levels, generate-runner-token, runner-token-file, instance-level-runner]
level: practitioner
status: docs-checked
description: "Register Gitea runners at instance, organization or repository level, get registration tokens from the UI, CLI or environment variable, and know how token reset works."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/actions/runner.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea runner registration

The runner is Gitea Runner (`gitea-runner`); installation and configuration have their own docs. This page covers where to register and the token.

## Levels
- **Instance**: runs jobs for all repositories. Token from the admin page `<host>/-/admin/actions/runners`.
- **Organization**: runs jobs for that organization's repositories. Token from `<host>/<org>/settings/actions/runners`.
- **Repository**: runs that repository's jobs. Token from `<host>/<owner>/<repo>/settings/actions/runners`.

A repository with its own runners can still be served by instance or organization runners; the docs say a future release may add control over that. If the settings page is missing, check your permissions and that Actions are enabled.

## Getting a token
- UI at the URLs above.
- CLI on the Gitea host: `gitea --config /etc/gitea/app.ini actions generate-runner-token`.
- Fixed global token at startup, via `GITEA_RUNNER_REGISTRATION_TOKEN` or `GITEA_RUNNER_REGISTRATION_TOKEN_FILE` (the file holds the token):
```
openssl rand -hex 24 > /some-dir/runner-token
export GITEA_RUNNER_REGISTRATION_TOKEN_FILE=/some-dir/runner-token
./gitea --config ...
```
The environment token stays valid until someone resets the token (creating a new one) in the web UI or via the API.

A token can register many runners until revoked and replaced with the reset link, so reset it after a leak or when you want to stop new registrations. Then follow the runner docs to install, configure and start it (`gitea-runner register` then `gitea-runner daemon`, see `gitea-actions-quickstart`).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
