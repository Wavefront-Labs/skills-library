---
id: computing-software.devops-ci-cd.github-actions.default-environment-variables-vs-contexts
name: default-environment-variables-vs-contexts
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, default-environment-variables, env-vs-context, github-workspace, github-ref-name, github-sha, github-run-id, runner-temp, runner-tool-cache, github-head-ref, github-base-ref, github-server-url, github-api-url, runner-os, runner-arch, ci-variable, expressions, contexts]
level: practitioner
status: verified
description: "Pick between GITHUB_* default environment variables and the github/runner contexts: what each exposes, which are unset on which events, and the ref-name vs head-ref traps."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#github-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default environment variables vs contexts

**Goal:** read run metadata the right way in the right place, and stop being surprised by
empty values.

## 1. Two views of the same data
| Shell (`$GITHUB_*`, `$RUNNER_*`) | Expression (`${{ github.* }}`, `${{ runner.* }}`) |
|---|---|
| Set on the runner process; only inside `run:` and actions | Resolved by the server/runner before the step; usable in `if`, `with`, `name`, `env` |
| Strings only | Typed (`github.event` is an object) |
| Not available in `jobs.<id>.if`, `runs-on`, `concurrency` | Available almost everywhere |

Rule: use `${{ }}` outside shell lines; use `$VAR` inside them.

## 2. The ones that matter
| env var | context | note |
|---|---|---|
| `GITHUB_WORKSPACE` | `github.workspace` | default working directory for steps and default location of the repo after `actions/checkout` |
| `GITHUB_SHA` | `github.sha` | depends on the event; on `pull_request` it is the last merge commit on the PR merge branch, not the PR head; use `github.event.pull_request.head.sha` |
| `GITHUB_REF` | `github.ref` | full ref (`refs/heads/main`, `refs/pull/12/merge`, `refs/tags/v1`) |
| `GITHUB_REF_NAME` | `github.ref_name` | short name; on PRs it is `12/merge`, not the branch |
| `GITHUB_HEAD_REF` / `GITHUB_BASE_REF` | `github.head_ref` / `github.base_ref` | **only set on pull_request(_target)**; empty on push |
| `GITHUB_REF_TYPE` | `github.ref_type` | `branch` or `tag` |
| `GITHUB_RUN_ID` / `RUN_NUMBER` / `RUN_ATTEMPT` | `github.run_id` … | run_number increments per workflow, never resets |
| `GITHUB_JOB` | `github.job` | job key (not display name) |
| `GITHUB_ACTOR` | `github.actor` | who triggered; `github.triggering_actor` differs on re-runs |
| `GITHUB_REPOSITORY_OWNER` | `github.repository_owner` | handy for GHCR paths (lowercase it yourself) |
| `GITHUB_SERVER_URL` / `API_URL` | `github.server_url` / `api_url` | the server and REST API URLs |
| `RUNNER_OS` / `RUNNER_ARCH` | `runner.os` / `runner.arch` | `Linux`/`Windows`/`macOS`, `X64`/`ARM64` |
| `RUNNER_TEMP` | `runner.temp` | emptied at the beginning and end of each job; put downloads here |
| `RUNNER_TOOL_CACHE` | `runner.tool_cache` | directory containing the preinstalled tools on GitHub-hosted runners |
| (none) | `secrets.GITHUB_TOKEN` / `github.token` | not in the default variable list; map it with `env:` if a script needs it |
| `CI` | — | always `true` |

Branch name that works on both push and PR:
```yaml
env:
  BRANCH: ${{ github.head_ref || github.ref_name }}
```

## 3. Event-shape differences
`github.event` is the raw webhook payload: `head_commit` exists only for push;
`pull_request` only for PR events; `inputs` only for dispatch. Reference a missing path and
you get an empty string, not an error — guard with `github.event_name` checks.

## 4. Gotchas
- `GITHUB_REPOSITORY` keeps the owner/repo casing; lowercase it for image names with bash:
  `echo "IMAGE=${GITHUB_REPOSITORY,,}" >> "$GITHUB_ENV"` (`Octo-Org/My-Repo` → `octo-org/my-repo`, run locally).
- Trying to override a default variable (such as `GITHUB_*`) in `env:` is ignored.

## Verify
- [ ] PR workflows use `head.sha`/`head_ref` where the real branch matters.
- [ ] No `${{ github.* }}` inside `run:` lines with user-controlled content (titles, bodies).
- [ ] Dumping `${{ toJSON(github) }}` once confirmed the fields you rely on exist for each event.
