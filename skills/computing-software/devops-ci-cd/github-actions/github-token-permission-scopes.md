---
id: computing-software.devops-ci-cd.github-actions.github-token-permission-scopes
name: github-token-permission-scopes
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, permission-scopes, contents-write, permissions]
level: practitioner
status: docs-checked
description: "Map GITHUB_TOKEN permission scopes (contents, packages, pull-requests, checks, id-token, attestations, etc.) to the API calls and actions that need them."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions", "https://docs.github.com/en/actions/tutorials/authenticate-with-github_token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GITHUB_TOKEN permission scopes

Values: `read` (where applicable), `write` (includes `read`) and `none`. If you specify any scope, every
unspecified scope is set to `none`. `permissions: read-all`, `permissions: write-all` and `permissions: {}`
set all scopes at once.

| Scope | Documented example of what it allows |
|---|---|
| `contents` | `read` lists commits; `write` creates a release |
| `pull-requests` | `write` adds a label to a pull request |
| `issues` | `write` adds a comment to an issue |
| `packages` | `write` uploads and publishes packages on GitHub Packages |
| `checks` | `write` creates a check run |
| `statuses` | `read` lists commit statuses for a ref |
| `actions` | `write` cancels a workflow run |
| `deployments` | `write` creates a deployment |
| `id-token` | `write` is required to fetch an OIDC token (only `write` or `none`) |
| `attestations` | `write` generates an artifact attestation for a build |
| `security-events` | `read` lists code scanning alerts; `write` updates alert status |
| `pages` | `write` requests a GitHub Pages build |
| `discussions` | `write` closes or deletes a discussion |
| `vulnerability-alerts` | `read` lists Dependabot alerts (only `read` or `none`) |

Newer scopes (`artifact-metadata`, `code-quality`, `copilot-requests`) also exist on GitHub.com; see the
permissions reference for the current list. For the exact permission each REST endpoint needs, use the
REST API permissions pages.

## Common recipes
```yaml
# release job
permissions: { contents: write }
# image publish with provenance
permissions: { contents: read, packages: write, id-token: write, attestations: write }
# PR commenter
permissions: { contents: read, pull-requests: write }
```

## Gotchas
- Pull request events other than `pull_request_target` from forks: write permissions are changed to read-only unless an admin enabled "Send write tokens to workflows from pull requests".
- For access the token cannot have, use a GitHub App installation token or a personal access token.
- `permissions: {}` sets every scope to none.

## Verify
- [ ] Each job declares its own minimal block.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Scope names, value sets (id-token write/none, vulnerability-alerts read/none), read-all, write-all and {} syntax, and that unspecified scopes become none: confirmed in the github-token-available-permissions and github-token-scope-descriptions reusables used by workflow-syntax.
- Fork read-only rule and the GitHub App or PAT route for extra access: confirmed in workflow-syntax and the GITHUB_TOKEN tutorial.
- Removed the per-scope API mappings, `metadata: read`, `repository-projects` and the Set up job log claim, which the permissions docs do not state.

Method: documentation only; no commands were run.
