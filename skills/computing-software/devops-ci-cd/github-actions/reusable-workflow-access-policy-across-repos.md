---
id: computing-software.devops-ci-cd.github-actions.reusable-workflow-access-policy-across-repos
name: reusable-workflow-access-policy-across-repos
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, reusable-workflow-access, cross-repo-reusable, private-reusable-workflows, actions-access-policy, accessible-from-repositories, internal-repositories, enterprise-access, workflow-not-found, allowed-actions-reusable, org-actions-policy, platform-ci-repo, reusable-workflows, workflow-call]
level: practitioner
status: docs-checked
description: "Share reusable workflows and actions from a private or internal repo across the org/enterprise: the Actions access setting, the allowed-actions policy, and diagnosing 'workflow was not found'."
sources: ["https://docs.github.com/en/actions/how-tos/reuse-automations/share-with-your-organization", "https://docs.github.com/en/actions/how-tos/reuse-automations/share-across-private-repositories", "https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#access-to-reusable-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reusable workflow access across repositories

**Goal:** a `platform-ci` repo whose workflows every team repo can `uses:` — without making
it public and without each caller needing a token.

## 1. Who can call what
| callee repo visibility | callable from |
|---|---|
| public | any caller, subject to the caller's Actions permissions |
| internal (enterprise) | callers in the enterprise, **if** the Access setting allows |
| private | other private repositories, **if** the Access setting allows |

The setting lives on the **callee** repository: *Settings, Actions, General, Access*, with options such as
"Accessible from repositories in the 'ORGANIZATION-NAME' organization" (or, for a personal account, "Accessible
from repositories owned by 'USERNAME' user"). For internal or private callee repositories the Access policy must be
explicitly configured. The caller's repository must also allow actions and reusable workflows in its own Actions
permissions.

## 2. Caller
```yaml
jobs:
  ci:
    uses: octo-org/platform-ci/.github/workflows/node-ci.yml@v3
    with: { node-version: '22' }
    secrets: inherit
```
Reference the callee by tag, branch or SHA. The callee file must be directly under `.github/workflows/`;
subdirectories of `workflows` are not supported.

## 3. Policies that apply
The caller repository's Actions permissions must allow the use of actions and reusable workflows; if your
organisation limits actions to a selected set, make sure the callee is permitted (see the policy documentation for the
exact allow-list pattern syntax).

## 4. Diagnosis
- A caller that cannot resolve the callee usually has the Access setting off on the callee, a wrong path, or a
  missing ref.
- A callee that works for one team but not another is often in a different organisation (the organisation Access
  option is organisation-scoped); consider an internal repository with enterprise access on GHEC or GHES.

## 5. Gotchas
- Access applies to the repository's components (actions and reusable workflows), not to selected files.
- Everyone who calls `@v3` runs whatever that tag points to, so protect the callee repository's workflow files
  with review rules.

## Verify
- [ ] A new consumer repo in the org runs the shared workflow with no PAT.
- [ ] A repository outside the organisation cannot call the workflow (access is scoped as intended).

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Caller/callee visibility table, the Access policy requirement for internal or private callee repositories, and the caller's Actions permissions requirement: confirmed in the reusable workflows reference (access section).
- Access setting wording for organisation and user scope: confirmed in the share-with-your-organization and share-across-private-repositories pages. `.github/workflows` only, no subdirectories, and uses syntax with tag, branch or ref: confirmed in reuse-workflows.
- Removed unconfirmed claims: error message texts, allow-list pattern strings, local composite action resolution, ls-remote advice, floating-tag commands, fork and Dependabot remarks.

Method: documentation only; no commands were run.
