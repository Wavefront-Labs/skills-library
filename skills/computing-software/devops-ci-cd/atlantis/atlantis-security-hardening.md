---
id: computing-software.devops-ci-cd.atlantis.atlantis-security-hardening
name: atlantis-security-hardening
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [security, repo-allowlist, webhook-secret, var-file-allowlist, basic-auth, fork-prs]
level: advanced
status: docs-checked
description: "Harden an Atlantis server with repo allowlists, webhook secrets, TLS, web basic auth and plan-time protections."
sources: ["https://www.runatlantis.io/docs/security", "https://www.runatlantis.io/docs/webhook-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis security hardening

Atlantis runs with credentials to your infrastructure, so deploy it carefully. Documented risks: malicious Terraform in a PR (a malicious provider or `external` data source runs during automatic `plan`), `local-exec` provisioners during `apply`, custom commands in an `atlantis.yaml` read from the PR branch, and unwanted `plan`/`apply` comments on valid PRs.

Mitigations:
- Avoid public repos; anyone can comment on public PRs.
- Leave `--allow-fork-prs` off (default false).
- Set `--repo-allowlist` to specific repos, `github.com/org/*`, with `!` exclusions; `*` is dangerous without a webhook secret.
- Protect planning: bake providers into the image and block production egress, run an internal provider registry, and validate the plan step in server-side config. Approvals alone do not stop code running at plan.
- `--var-file-allowlist` restricts `-var-file` in comments to repo files and listed paths (default is the Atlantis data dir; symlinks are resolved).
- Webhook secrets: `ATLANTIS_GH_WEBHOOK_SECRET` or `ATLANTIS_GITLAB_WEBHOOK_SECRET`, longer than 24 characters, the same for every repo. Generate with `ruby -rsecurerandom -e 'puts SecureRandom.hex(32)'`. Azure DevOps uses basic auth on the webhook over HTTPS instead.
- TLS via `--ssl-cert-file` and `--ssl-key-file`.
- Web UI auth: `--web-basic-auth=true`, `--web-username`, `--web-password` (or `ATLANTIS_WEB_*`).

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Security, Webhook Secrets. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
