---
id: computing-software.devops-ci-cd.gitlab-ci.hooks-pre-get-sources-script
name: hooks-pre-get-sources-script
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, pre-get-sources-script, hooks-keyword, git-clone-tuning, runner-pre-build-script]
level: practitioner
status: docs-checked
description: "Run commands before the runner clones the repository with hooks:pre_get_sources_script, for Git configuration tweaks, versus runner-level pre_get_sources and pre_build scripts."
sources: ["https://docs.gitlab.com/ci/yaml/", "https://docs.gitlab.com/runner/configuration/advanced-configuration/", "https://docs.gitlab.com/ci/runners/configure_runners/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hooks: pre_get_sources_script

Everything in `before_script` runs **after** the clone. When the clone itself needs tuning, use the hook.

## 1. Job keyword
```yaml
default:
  hooks:
    pre_get_sources_script:
      - git config --global http.postBuffer 524288000
      - git config --global url."https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.example.com/".insteadOf "git@gitlab.example.com:"
      - git config --global lfs.concurrenttransfers 16
```
The hook takes an array of single-line or multi-line commands (YAML anchors and CI/CD
variables are supported) that run on the runner before the Git repository and any
submodules are cloned. The documented uses are adjusting the Git configuration and exporting
tracing variables. `pre_get_sources_script` is currently the only available hook. It is a job
keyword, usable in a job or in `default`. The example values above are illustrative: check
each `git config` key against the Git documentation.

## 2. Runner-level equivalents (config.toml, admin-owned)
```toml
[[runners]]
  pre_get_sources_script = "git config --global fetch.parallel 8"
  post_get_sources_script = ""
  pre_build_script = "echo runner-wide setup"
  post_build_script = ""
```
Runner scripts apply to every job on that runner; the job hook applies per job. Runner
`pre_get_sources_script` runs before the repository and submodules are updated, and
`post_get_sources_script` after. `pre_build_script` runs before the job, in the same shell
context as `before_script` and `script`; if it fails, the remaining commands in that context
are skipped but `after_script` still runs.

## 3. Related clone knobs (often what you really want)
- `GIT_DEPTH: 20` (shallow), `GIT_STRATEGY: clone|fetch|none|empty` (with `empty`, the
  runner hook scripts still run), `GIT_CLEAN_FLAGS`, `GIT_SUBMODULE_STRATEGY`,
  `GIT_SUBMODULE_DEPTH`, `GIT_FETCH_EXTRA_FLAGS`, `GIT_LFS_SKIP_SMUDGE`.

## Gotchas
- `git config --global` on a shell executor changes the runner user's Git configuration for
  later jobs too; prefer per-repository configuration or undo it.
- Do not print the job token (for example by listing the Git configuration in a job log).

## Verify
- [ ] Log shows hook commands before the repository is fetched; previously failing clone succeeds.

## Checked

2026-10-28. Confirmed against the GitLab CI/CD YAML reference (`hooks`, `hooks:pre_get_sources_script`: array of commands, anchors and variables supported, runs before cloning the repository and submodules, Git configuration and tracing variables as uses), the GitLab Runner advanced configuration page (`pre_get_sources_script`, `post_get_sources_script`, `pre_build_script`, `post_build_script` behaviour) and the configure runners page (`GIT_STRATEGY` values clone, fetch, none, empty; `GIT_SUBMODULE_DEPTH`, `GIT_LFS_SKIP_SMUDGE` exist). Removed: the executor-environment claim, the failing-hook claim, the list of network and CA tweaks, and the masking claim for the job token (not in the fetched pages).

Method: documentation only; no commands were run.
