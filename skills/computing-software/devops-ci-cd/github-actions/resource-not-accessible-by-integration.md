---
id: computing-software.devops-ci-cd.github-actions.resource-not-accessible-by-integration
name: resource-not-accessible-by-integration
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, resource-not-accessible-by-integration, github-token, permissions]
level: practitioner
status: docs-checked
description: "Debug the 403 \"Resource not accessible by integration\" in Actions: missing permission scope, fork PR read-only token, org default policy, or a resource GITHUB_TOKEN cannot reach."
sources: ["https://docs.github.com/en/actions/tutorials/authenticate-with-github_token", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging "Resource not accessible by integration" (HTTP 403)

The token authenticated but lacks access. Work through these in order.

1. **Check effective permissions**: read the `permissions` blocks in the workflow and the repository, organisation and enterprise defaults (permissions are calculated from the default, then the workflow level, then the job level, then the fork rule).
   Compare with the scope the API needs (see the scope table: comments need `pull-requests: write` or
   `issues: write`, releases need `contents: write`, check runs need `checks: write`).
2. **Was a `permissions:` block added somewhere?** If you specify any permission, all unspecified ones are set to `none`.
3. **Fork PR?** For pull request events other than `pull_request_target` from a fork, write permissions are changed to read-only unless an admin enabled "Send write tokens to workflows from pull requests". A `workflow_run` workflow runs with write tokens and secrets, so it can post results, but never execute untrusted PR code there; `pull_request_target` also gets read/write, so do not check out the PR head in it.
4. **Dependabot PR?** Workflow runs triggered by Dependabot pull requests run as if from a fork: read-only `GITHUB_TOKEN` and no access to secrets. See the secure-use reference for safe patterns.
5. **Org/enterprise default** restricted permissions apply as the starting point, and the repository setting that allows or prevents Actions workflows from creating or approving pull requests can block PR creation; check the repository, organisation and enterprise Actions settings.
6. **Resource outside the repo**: other repos, org projects v2, org members, another repo's packages.
   GITHUB_TOKEN is scoped to the current repository. For permissions the token cannot have, create a GitHub App and use an installation access token (or a personal access token stored as a secret).

## Reproduce quickly
Retry the failing API call from a minimal workflow whose job declares only the one scope you expect it to need.

## Verify
- [ ] The failing call succeeds with the minimal added scope; no blanket `write-all`.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- How token permissions are calculated (default, workflow level, job level, fork adjustment) and the fork read-only rule with the 'Send write tokens' exception: confirmed in workflow-syntax, permissions.
- Unspecified permissions become none when any is specified: confirmed in the permissions reusable text.
- Dependabot runs behave as from a fork with read-only token and no secrets; GITHUB_TOKEN is repository-scoped and a GitHub App token is the documented route for more: confirmed in the permissions text and the GITHUB_TOKEN tutorial.
- Removed the Set up job log hint, the Packages access step and the gh api command, which no fetched page documents.

Method: documentation only; no commands were run.
