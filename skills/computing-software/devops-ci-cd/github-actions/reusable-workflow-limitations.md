---
id: computing-software.devops-ci-cd.github-actions.reusable-workflow-limitations
name: reusable-workflow-limitations
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, reusable-workflow-limitations, env-not-inherited, reusable-workflows]
level: practitioner
status: docs-checked
description: "Know reusable workflow limits before designing around them: env not inherited, 10 nesting levels, 50 called workflows, no step-level calls, and secrets/permissions rules."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#limitations-of-reusable-workflows", "https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reusable workflow limitations

| Limit | Detail | Workaround |
|---|---|---|
| `env` not passed | Caller's workflow-level `env` is not visible in the callee; callee `env` not visible to caller (use workflow outputs); `GITHUB_ENV` cannot pass values to caller steps | pass as `inputs`, or use `vars` (repo, org or environment level) |
| Call site | Only at **job** level (`jobs.x.uses:`), never as a step | composite action for step-level reuse |
| Nesting | Up to 10 levels of workflows total (top-level caller + up to 9 levels of reusable workflows); loops are not permitted | flatten |
| Count | Max 50 unique reusable workflows from a single workflow file, including nested trees (GitHub.com; 20 on GitHub Enterprise Server) | consolidate |
| Permissions | The `GITHUB_TOKEN` permissions passed from the caller can only be downgraded, not elevated, by the called workflow; if the calling job sets no `permissions`, the callee gets the default token permissions | grant max in caller job |
| Secrets | Not passed unless `secrets: inherit` or mapped explicitly; nested callees need inherit at every level | inherit, or explicit per level |
| Job with `uses` | Cannot have `steps`, `runs-on`, `env`, `container`, `services`, `timeout-minutes` | put them in the callee |
| Outputs | Callee must map job outputs to `on.workflow_call.outputs` | - |
| Private repo callee | The callee repository's settings must allow access (see the sharing docs) | settings |

## Allowed on the calling job
`name`, `uses`, `with`, `secrets` (including `secrets: inherit`), `strategy`, `needs`, `if`, `concurrency`, `permissions`, and (where the feature is enabled) `cache-mode`. No other job keyword is allowed.

## Verify
- [ ] Callee prints the inputs it relies on; no reliance on caller env.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Nesting depth (10 levels, top-level caller plus 9) and no loops: confirmed in reuse-workflows (Nesting reusable workflows).
- 50 unique reusable workflows per workflow file on GitHub.com (20 on GHES) and the env, vars and GITHUB_ENV limitations: confirmed in the reusable workflow reference, Limitations.
- The closed list of keywords allowed on a calling job, and that permissions can only be maintained or reduced down the chain: confirmed in the same reference.
- Removed unconfirmed error-message texts and the specific private-repository setting name.

Method: documentation only; no commands were run.
