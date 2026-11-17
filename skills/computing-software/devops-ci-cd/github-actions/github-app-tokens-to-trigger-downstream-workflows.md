---
id: computing-software.devops-ci-cd.github-actions.github-app-tokens-to-trigger-downstream-workflows
name: github-app-tokens-to-trigger-downstream-workflows
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, token-no-trigger, github-app-token, create-github-app-token, github-token-no-recursion, bot-pr-no-checks, app-installation-token, private-key-secret, app-id-variable, cross-repo-token, pat-alternative, tibdex-github-app-token, github-token, permissions]
level: practitioner
status: docs-checked
description: "Why GITHUB_TOKEN pushes and PRs never start workflows, and how to mint a scoped GitHub App installation token with actions/create-github-app-token that does."
sources: ["https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflow-runs", "https://github.com/actions/create-github-app-token#readme"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub App tokens when GITHUB_TOKEN cannot trigger workflows

**Goal:** a release-bot PR that gets CI checks, a tag push that starts the release
workflow — without a long-lived personal access token.

## 1. The rule
Events triggered by the repository's `GITHUB_TOKEN` do not create new workflow runs, to prevent accidental
recursive runs; for example a push made with `GITHUB_TOKEN` does not start a workflow configured on `push`.
Exceptions: `workflow_dispatch` and `repository_dispatch` always create runs, and `pull_request` events
(`opened`, `synchronize`, `reopened`) from a pull request that a workflow created or updated with
`GITHUB_TOKEN` create runs in an **approval-required** state that a user with write access starts with
"Approve workflows to run" (other activity types create no runs). Symptoms: a bot's PR whose checks wait for approval,
or a pushed tag that did not start `release.yml`.

## 2. Mint an App installation token
Create a GitHub App with the permissions you need (for example Contents: write, Pull requests: write) and install it
on the repositories. Store the app's client ID as a variable and its private key as a secret.
```yaml
permissions: { contents: read }
steps:
  - id: app
    uses: actions/create-github-app-token@v3
    with:
      client-id: ${{ vars.RELEASE_APP_CLIENT_ID }}   # legacy app-id input is also accepted
      private-key: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}
      owner: ${{ github.repository_owner }}      # optional; with no repositories = whole installation
      repositories: app,infra                     # optional: comma or newline separated
      permission-contents: write                  # optional: narrow the token's permissions
  - uses: actions/checkout@v7
    with: { token: "${{ steps.app.outputs.token }}" }
  - run: |
      git config user.name "release-bot[bot]"
      git config user.email "${{ steps.app.outputs.app-slug }}[bot]@users.noreply.github.com"
      git commit -am "chore: release" && git tag v1.2.3 && git push --follow-tags
```
An installation access token expires after 1 hour, and unless `skip-token-revoke` is set it is revoked in the action's
post step (so it cannot be passed to another job). By default the token inherits all of the installation's permissions
and is scoped to the current repository when `owner` and `repositories` are empty. The token is output as `token`;
`installation-id` and `app-slug` are also output.

## 3. Why an App rather than a PAT
- Scoped to listed repositories and permissions rather than a person's full access.
- Commits and PRs are attributed to the app's bot account, which you can exclude with `github.actor` conditions.

## 4. Loop guard
A workflow triggered by the App's push can push again and loop. Guard the job (for example with a `github.actor`
condition) or use the skip-run commit message convention when no downstream run is wanted.

## 5. Gotchas
- `repositories` entries may include an owner, which must match the `owner` input (or the current repository owner).
- The private key input accepts escaped newlines (`\n`), which are replaced with real newlines.
- The `enterprise` input is mutually exclusive with `owner` and `repositories`.

## Verify
- [ ] A tag pushed with the app token starts the release workflow.
- [ ] The bot PR's checks run without waiting for approval.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and actions/create-github-app-token README (v3).
- Events caused by GITHUB_TOKEN not creating runs, the workflow_dispatch and repository_dispatch exceptions, and the approval-required pull_request behaviour: confirmed in the actions-do-not-trigger-workflows reusable and the GITHUB_TOKEN concept page.
- actions/create-github-app-token (latest release v3.3.0) inputs client-id and legacy app-id, private-key, owner, repositories, enterprise, permission-<name>, skip-token-revoke; outputs token, installation-id, app-slug; 1-hour expiry and post-step revoke: confirmed in the action README.
- Removed unconfirmed claims: rate-limit figures, tibdex history, deletion and 401 behaviour, cross-owner remark and the skip-ci advice stated as fact.

Method: documentation only; no commands were run.
