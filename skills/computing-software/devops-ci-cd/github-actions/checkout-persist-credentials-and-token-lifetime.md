---
id: computing-software.devops-ci-cd.github-actions.checkout-persist-credentials-and-token-lifetime
name: checkout-persist-credentials-and-token-lifetime
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, persist-credentials, token-expiry, github-token-lifetime, extraheader-authorization, git-config-leak, checkout-token, credential-in-git-config, 24-hour-token, token-revoked-after-job, push-after-checkout, zizmor-artipacked, actions-checkout, github-token]
level: practitioner
status: docs-checked
description: "GITHUB_TOKEN lifetime and actions/checkout persist-credentials: when the token sits in .git/config, how it leaks via artifacts, and how to push safely."
sources: ["https://github.com/actions/checkout#readme", "https://docs.github.com/en/actions/concepts/security/github_token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# checkout persist-credentials and token lifetime

**Goal:** know where the job token is kept by `actions/checkout` and avoid shipping it in an artifact.

## 1. Token lifetime
The `GITHUB_TOKEN` is an installation access token fetched before each job. It expires when the job finishes
or after its effective maximum lifetime:
- GitHub-hosted runners: the maximum job time is 6 hours, so the token lives at most 6 hours.
- Self-hosted runners: the maximum job time is 5 days, but the token can only be refreshed for up to
  24 hours; for jobs that run longer, use a personal access token or another authentication method.
The token is also available as the `github.token` context.

## 2. What checkout does with it
`actions/checkout` persists the auth token so your scripts can run authenticated git commands; the token is
removed during post-job cleanup. `persist-credentials` defaults to true; set `false` to opt out.
- Checkout v4 and v5: the token is persisted in the local git config (`.git/config`).
- Checkout v6 and later (current major v7): credentials are stored in a separate file under
  `$RUNNER_TEMP` instead of directly in `.git/config`; `git fetch` and `git push` still work. Running
  authenticated git commands from a Docker container action then needs Actions Runner v2.329.0 or later.
Consequences to keep in mind:
- On older checkout versions, any step that archives the workspace (for example `upload-artifact` with
  `path: .`) could include `.git/config` and the token. Upgrade to a current major and exclude `.git` anyway.
- Untrusted code that runs in the job while credentials are persisted may be able to use them.
- Checkout v7 refuses to check out fork pull request code by default under `pull_request_target` or
  `workflow_run`; the opt-in input is `allow-unsafe-pr-checkout: true` (read the securely-using-pull_request_target
  guidance first).

## 3. Safer default
```yaml
- uses: actions/checkout@v7
  with:
    persist-credentials: false
```
Then pass the token explicitly to the one step that needs it, for example through `env` with
`GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` for the `gh` CLI, and grant only the permissions that step needs.

## 4. When to keep persist-credentials true
Short jobs on trusted code whose later steps run `git push` or `git fetch`. Exclude `.git` from any artifact
path anyway.

## 5. Gotchas
- The checkout `fetch-depth` input defaults to 1 (a single commit); `0` fetches all history and tags. Set it at
  checkout time if later steps need history, especially with `persist-credentials: false`.
- Pin the checkout major you have reviewed (the README lists v7 as current); behaviour above differs by major.

## Verify
- [ ] The artifact upload step excludes `.git`.
- [ ] Push steps still succeed using the explicit token.

## Checked

Date: 2026-10-25. Documentation release: actions/checkout README (v7) and github/docs, commit of 2026-10-23.
- GITHUB_TOKEN lifetime (6 hours hosted, 5 days self-hosted job limit, 24-hour refresh limit, github.token context): confirmed in the github_token concept page.
- persist-credentials default and storage location by major (v4 local git config, v6 separate file under RUNNER_TEMP), v7 allow-unsafe-pr-checkout, fetch-depth default 1: confirmed in the actions/checkout README (v7 section, latest release v7.0.2).
- Removed the extraheader and base64 details, the manual push recipes, the zizmor artipacked claim, the re-run and 24-hour-only lifetime claims, and post-step cleanup remarks, none of which the fetched documentation states or which were stale for v6 and later.

Method: documentation only; no commands were run.
