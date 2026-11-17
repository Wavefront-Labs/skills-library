---
id: computing-software.digital-privacy-hygiene.password-managers.bitwarden-secrets-manager-for-machine-secrets
name: bitwarden-secrets-manager-for-machine-secrets
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bitwarden-secrets-manager, password-manager-cli, secrets-management]
level: practitioner
status: docs-checked
description: "Move API keys and CI secrets out of a personal vault into Bitwarden Secrets Manager: projects, machine accounts, bws CLI and env injection."
sources:
  - "https://bitwarden.com/help/secrets-manager-cli/"
  - "https://bitwarden.com/help/machine-accounts/"
  - "https://bitwarden.com/help/github-actions-integration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bitwarden Secrets Manager for machine secrets

**Goal:** scripts and CI get the secrets they need via scoped tokens, without your master password or personal
vault being involved.

## Concepts
- **Projects** group secrets (`homelab`, `website-prod`).
- **Machine accounts** (called service accounts before the 2024.4.1 release) represent applications or deployment
  pipelines. Each is given access to chosen projects with a permission level and issues **access tokens** for
  programmatic access.
- Permission levels per project: **Can read** (retrieve secrets) or **Can read, write** (also edit secrets, create new
  secrets in assigned projects, or create new projects).
- The `bws` CLI authenticates with a machine account's access token, so it can only touch the secrets and projects that
  account can reach.

## Setup
1. Create a project and add secrets in the Secrets Manager web vault.
2. New > Machine account, then in its **Projects** tab add the project and choose **Can read**. Create an access token
   for it and store that token in the CI's encrypted secret store or the host's protected environment file.
3. Install `bws` (installer scripts at bws.bitwarden.com, or releases on the Bitwarden SDK GitHub repo; or the Docker
   image `ghcr.io/bitwarden/bws`) and test:
   ```
   export BWS_ACCESS_TOKEN=<access token>
   bws secret list                   # secrets this machine account can reach
   bws secret get <secret-id>
   bws run -- 'npm run start'        # injects secrets as environment variables
   ```
4. EU or self-hosted servers must be configured first, for example `bws config server-base https://vault.bitwarden.eu`.

## Useful bws options
- `bws run --project-id <id> -- <command>` injects secrets from one project only.
- `--uuids-as-keynames` (or `BWS_UUIDS_AS_KEYNAMES=true`) names variables by secret ID with hyphens turned to
  underscores and a leading underscore, so names are POSIX-safe.
- `--no-inherit-env` drops most shell environment variables but still inherits `$PATH`; it is not a sandbox.
- `-o, --output` takes `json` (default), `yaml`, `table`, `tsv`, `none` or `env`.
- `bws secret create <KEY> <VALUE> <PROJECT_ID>` (optional `--note`) and `bws secret edit <SECRET_ID> --key ... --value ...`.

## GitHub Actions
Save the access token as a repository secret (for example `BW_ACCESS_TOKEN`), then use `bitwarden/sm-action@v2` with
`access_token: ${{ secrets.BW_ACCESS_TOKEN }}` and a `secrets:` list of `<secret-id> > ENV_NAME` lines. Retrieved
secrets are injected as masked environment variables. For self-hosted servers set `base_url`.

## Hygiene
- Give each system its own machine account with only **Can read** on the projects it needs.
- Only run commands you trust under `bws run`: it executes them in your shell with the secrets available.
- The CLI can keep an encrypted state file, so it may keep working with a revoked access token until the stored session
  expires; delete the state file (or set `state_opt_out`) to force re-authentication.
- Many separate sessions from one IP address in a short time can hit rate limits.
- Deleting a machine account does not delete its secrets. Event logs on the machine account record accessed secrets.

## Gotchas
- Secrets are referenced by ID; keep a mapping of names to IDs in the repo README, not the values.
- Non-POSIX secret names are still set as variables but may not be readable by POSIX-limited programs; with `env`
  output they are commented out.

## Checked
Confirmed 2026-11-08 against the three cited Bitwarden help pages: machine account rename and permission levels,
access-token authentication, `BWS_ACCESS_TOKEN`, `bws run` and its options, output formats, server config, state-file
behaviour, rate-limit warning, and the `bitwarden/sm-action@v2` inputs. Removed: the "shown once" token claim, the
web-vault menu path for creating projects, token expiry advice, and the CI-log tip, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
