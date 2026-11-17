---
id: computing-software.devops-ci-cd.github-actions.env-keyword-and-precedence
name: env-keyword-and-precedence
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, env-keyword, env-precedence, env-context, workflow-env, job-env, step-env, github-env, environment-variables, with-vs-env, action-inputs-env, input-prefix, env-in-if, workflow-syntax]
level: practitioner
status: verified
description: "Use env at workflow, job and step level with correct precedence, know when env values are visible to expressions vs only to the shell, and avoid the step-env-not-visible-in-if trap."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#env", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#env-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# env keyword and precedence

**Goal:** define variables once at the right scope and read them the right way.

## 1. Three scopes, narrowest wins
```yaml
env:                          # workflow: every job, every step
  NODE_OPTIONS: --max-old-space-size=4096
jobs:
  build:
    env:                      # job: overrides workflow
      CI_PROFILE: release
    steps:
      - run: echo "$CI_PROFILE"
        env:                  # step: overrides job and workflow
          CI_PROFILE: debug
```
Step > job > workflow: GitHub uses the most specific variable with that name.

## 2. Two ways to read it
- **Shell:** `$CI_PROFILE` (bash), `$env:CI_PROFILE` (pwsh), `%CI_PROFILE%` (cmd). Expanded at run
  time by the shell.
- **Expression:** `${{ env.CI_PROFILE }}`. Expanded by the runner *before* the step starts. Use
  this in `with:`, `name:`, `if:` and anywhere that is not a shell line.

Prefer `$VAR` inside `run:` — `${{ env.X }}` is substituted as literal text into the script, so a
value containing quotes or `$(...)` becomes a script-injection hole.

## 3. Visibility rules that bite
- `env` **cannot** be used in `jobs.<id>.if` or `on:` — only `github`, `inputs`, `vars` and
  `needs` contexts exist there. Use `vars` (configuration variables) for job-level gating.
- Which contexts a key can read is fixed by the context availability table in the contexts reference:
  a step's `if` may read `env`, but workflow-level `env` can only read `github`, `secrets`, `inputs` and
  `vars`.
- Variables in an `env` map cannot be defined in terms of other variables in the same map (GitHub docs).
  Chain via `GITHUB_ENV` instead.
- A value written with `echo "X=1" >> "$GITHUB_ENV"` is available to **subsequent** steps, not the step
  that wrote it. To pass values to another job use job outputs.

## 4. Actions read inputs as env too
`with:` inputs are set as environment variables prefixed `INPUT_` and converted to upper case, so
`with: { first_name: x }` reaches a container action as `INPUT_FIRST_NAME`. Do not log the environment.

## 5. Naming constraints
You cannot use a default environment variable name (`GITHUB_*`, `RUNNER_*`, `CI` ...): an attempt to
override one is ignored. `CI` is always `true`.

## Verify
- [ ] No `${{ env.* }}` interpolation inside `run:` lines that carry user-controlled content.
- [ ] `actionlint` reports no `context "env" is not allowed here` errors.
- [ ] Cross-job values flow through outputs, not env.
