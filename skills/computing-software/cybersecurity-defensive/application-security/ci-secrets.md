---
id: computing-software.cybersecurity-defensive.application-security.ci-secrets
name: ci-secrets
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [ci-secrets, cicd-secrets, oidc-federation, github-actions, gitlab-ci, secrets-management]
level: practitioner
status: docs-checked
description: "Handle secrets in CI/CD: replace static cloud keys with OIDC tokens, scope secrets by environment, mask logs, and keep them from forked workflows."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions", "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html", "https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD secrets handling

Secrets in CI/CD are numerous and some give substantial access. The OWASP CI/CD cheat sheet's two aims: make secrets
hard to steal in usable form, and reduce the impact if they are stolen.

## 1. Prefer OIDC over stored cloud credentials
- **GitHub Actions**: with a trust relationship configured at a cloud provider that supports OIDC, a workflow requests
  a short-lived access token instead of using a long-lived GitHub secret. Each job gets a unique JWT from GitHub's
  OIDC provider (issuer `https://token.actions.githubusercontent.com`); the cloud role's trust definition matches
  claims such as `sub` (for example `repo:octo-org/octo-repo:environment:prod`), `aud`, `ref` and `repository`. The
  cloud token is valid only for the job. Repositories created after July 15, 2026 use an immutable default `sub`
  format including owner and repository IDs; check the OIDC reference for yours.
- **GitLab**: declare `id_tokens:` on the job with an `aud` per service, for example
  `id_tokens: { FIRST_ID_TOKEN: { aud: https://first.service.com } }`, and use the token in `script`. Different
  audiences per service reduce the damage of a compromised token because services can reject a token whose `aud` does
  not match. Tokens carry claims such as `project_path`, `ref_type`, `ref_protected`, `environment` and
  `environment_protected`; bound-claim checks on the receiving side (for example in HashiCorp Vault) can use them.

## 2. Scope the secrets that remain
- GitHub secrets exist at repository, environment and organization level. Organization secrets can be limited by an
  access policy (all repositories, private only or a selected list). Prefer the narrowest scope.
- With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a
  forked repository. They are also not automatically passed to reusable workflows or available to workflows triggered
  by Dependabot events.
- Apply least privilege: credentials limited to the operations and resources a pipeline needs, not shared between
  pipelines of different sensitivity, and OS accounts running pipelines without root.

## 3. Keep secrets out of logs and command lines
- Mask sensitive values that are not GitHub secrets with `::add-mask::VALUE`.
- Avoid passing secrets on the command line (visible to other users via `ps` or captured by audit events); use
  environment variables or STDIN, and quote the variable in the shell.
- GitHub secrets cannot be referenced directly in `if:` conditionals; set them as job-level environment variables.
- Base64 is encoding, not encryption. The documented workaround for secrets over 48 KB (gpg-encrypted file plus
  passphrase secret) means GitHub does not redact printed values.
- Never hardcode secrets in repositories or CI config, detect them with scanners such as git-leaks or git-secrets, and
  never print them or leave them in shell history files.

## Verify
Cloud audit logs show job-scoped federated tokens, no long-lived cloud keys exist in CI settings, a fork-triggered
workflow receives no secrets, and job logs contain none.

## Checked
Method: docs-checked 2026-11-09 against the GitHub "Using secrets in GitHub Actions" and OIDC overview pages, the
GitLab ID token authentication page (read to the claims table) and the OWASP CI/CD Security Cheat Sheet. Removed
unconfirmed claims: the AWS `configure-aws-credentials` and trust-policy specifics, Azure and GCP federation, GitLab
protected and masked variables, `pull_request_target` guidance, self-hosted runner and `set -x` advice, and
action pinning and `GITHUB_TOKEN` default-permission advice.
