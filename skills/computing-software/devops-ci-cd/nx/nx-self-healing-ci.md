---
id: computing-software.devops-ci-cd.nx.nx-self-healing-ci
name: nx-self-healing-ci
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, self-healing-ci, fix-ci, ai, ci-config, apply-locally]
level: practitioner
status: docs-checked
description: "Enable Nx Cloud Self-Healing CI: nx fix-ci with always-run conditions per CI provider, workspace settings, ai.fix-tasks-patterns, auto-apply, SELF_HEALING.md, nx apply-locally."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/self-healing-ci.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let Nx Cloud AI propose (and optionally auto-apply) fixes for failing CI tasks.

Prereqs: `npx nx@latest connect`; a VCS integration enabled in Nx Cloud (GitHub, GitLab, Azure DevOps, Bitbucket); "Self-Healing CI" on in workspace settings.

Add `nx fix-ci` as the last step of the main job (the one running `nx-cloud start-workers` and `nx affected`/`run-many`). It must run even when earlier steps failed; if all tasks passed it is a no-op.
- GitHub: `- run: npx nx fix-ci` with `if: always()`.
- Azure DevOps: `- script: npx nx fix-ci` with `condition: always()`.
- GitLab: put `- npx nx fix-ci` in `after_script`.
- Bitbucket: put it in the step's `after-script`.
Workers need `.nx/ci-config.yaml`:
```yaml
dte:
  distribute-on: 3 linux-large-js
lifecycle:
  stop-after: [lint, test, build]
```

Workspace settings (cloud.nx.app, Self-Healing CI): enable, GitHub PR comments, auto-retry flaky tasks (pushes an empty commit), public link access (avoid), draft PR handling, protected branch prefixes (default branch plus `main`, `master`, `trunk`, `dev`, `stable`, `canary` never get fixes). Eligible tasks: any failing task, or glob patterns, plus never-fix patterns such as `*e2e*`.

Auto-apply happens only when the task matches the patterns, the agent is highly confident, and the fix is verified. Preset "deterministic Nx checks" auto-fixes `nx format:check`, `nx sync:check`, `nx conformance:check` failures. Add include patterns (`*build*`, `lint`) and excludes.

Override per branch in `.nx/ci-config.yaml` (wins over workspace settings per key; use only for temporary changes):
```yaml
ai:
  fix-tasks-patterns: ['*lint*', '*test*', '!*e2e*']
  auto-apply-patterns: [lint]
```

Guide the agent with `.nx/SELF_HEALING.md` (freeform markdown: Confidence Rules, Off-Limits Areas, Fix Preferences, Predefined Fixes, Context). A root `CLAUDE.md` is also read; SELF_HEALING.md wins on conflict. The CI run's Configurations tab shows whether it was detected.

Apply a fix from the PR comment, editor (Nx Console) or Nx Cloud UI. To tweak locally: `nx apply-locally <fix-identifier>` (`--no-interactive` disables prompts). Revert via git or the diff viewer.

## Checked

2026-11-07. Confirmed against AI-Powered Self-Healing CI: prerequisites (connect, VCS integration for GitHub, GitLab, Azure DevOps and Bitbucket, workspace setting), nx fix-ci with if: always(), condition: always(), after_script and after-script, the no-op when all tasks pass, .nx/ci-config.yaml with dte and lifecycle, the general settings table including protected branch names, eligible-task modes and never-fix patterns, the auto-apply conditions, deterministic Nx checks, include and exclude patterns, ai.fix-tasks-patterns and ai.auto-apply-patterns with key-level precedence, .nx/SELF_HEALING.md sections, CLAUDE.md precedence, the Configurations tab, apply routes, and nx apply-locally with --no-interactive. Removed: the invented Verify step.

Method: documentation only; no commands were run.
