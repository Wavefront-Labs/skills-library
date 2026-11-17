---
id: computing-software.devops-ci-cd.ci-pipeline-design.pre-commit-hooks-and-pre-tested-commits
name: pre-commit-hooks-and-pre-tested-commits
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, pre-commit-hooks, pre-commit, pre-tested-commit, gated-commit, merge-queue, keep-main-green, continuous-integration]
level: practitioner
status: docs-checked
description: "Keep main green: fast local checks with the pre-commit framework (and CI enforcing the same hooks), plus pre-tested/gated commits via a merge queue."
sources: ["https://pre-commit.com/", "https://martinfowler.com/articles/continuousIntegration.html", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-commit hooks and pre-tested commits

Two layers with different jobs: **local hooks** give quick feedback before a commit exists;
**pre-tested commits** keep broken changes off the mainline until a build passes.

## 1. Local hooks with the pre-commit framework
pre-commit is a multi-language package manager for git hook scripts: you list the hooks you
want and it installs and runs them, whatever language they are written in.
```yaml
# .pre-commit-config.yaml (project root)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: <tag>
    hooks:
      - id: trailing-whitespace
```
```bash
pip install pre-commit
pre-commit install            # writes .git/hooks/pre-commit
pre-commit run --all-files    # run every hook on every file
```
- By default hooks run only on the changed (staged) files during git hooks; run
  `--all-files` when adding new hooks.
- `rev` pins the hook repository version; `pre-commit autoupdate` updates to the latest tags
  (by default), `--freeze` pins to commit SHAs.
- `--show-diff-on-failure` runs `git diff` after hooks fail, which helps in CI logs.
- To skip a hook without `--no-verify`, set the `SKIP` environment variable to a
  comma-separated list of hook ids, for example `SKIP=flake8 git commit -m "foo"`.
- The `manual` stage holds hooks that run only on request via
  `pre-commit run --hook-stage manual <hook-id>`.
- Local hooks only help if installed, so run the same configuration in CI, for example
  `pre-commit run --all-files` as an early job (judgement; not stated in this form on the page).

## 2. Pre-tested commits (Fowler: Pending Head)
Fowler: some teams remove the risk of breaking the mainline with a **pending head**
(also called pre-tested, delayed or gated commit): commits pushed for integration go onto
another branch until the build completes, and migrate to the mainline only after a green
build. It avoids any danger to the mainline, though an effective team should rarely see a red
mainline, and its visibility encourages people to learn how to avoid it. If the build does
break, the usual best fix is to revert the faulty commit.

## 3. GitHub merge queue
Once a pull request has passed required branch protection checks, a user with write access
can add it to the queue. The queue ensures the changes pass all required status checks when
applied to the latest version of the target branch and any pull requests already in the
queue. It merges in first-in-first-out order using temporary branches and a `merge_group`.
- With GitHub Actions, workflows used for required checks must add the `merge_group` event as
  a trigger, otherwise the checks are not reported and the merge fails. It is separate from
  the `pull_request` and `push` events.
- A pull request is removed from the queue if required checks fail or conflicts appear
  after grouping.
- A setting lets pull requests that failed checks be grouped as long as the last pull
  request in the group passed, which can help with intermittent failures.

## Verify
- [ ] Hooks are installed (`pre-commit install`) and CI runs the same configuration.
- [ ] Required checks run on the merge queue trigger as well as on pull requests.
- [ ] A broken mainline is reverted first, debugged second.

## Checked
Confirmed 2026-11-09 against the pre-commit.com page (install, config, autoupdate, `--all-files`, `--show-diff-on-failure`, SKIP, manual stage; searched by keyword and read sections), Fowler's Continuous Integration article (fix broken builds, pending head; lines 509-538), and GitHub's merge queue page (read in full).
Removed as unconfirmed: hook versions and the ruff, gitleaks, detect-private-key and check-added-large-files hooks, the 5-second hook budget, pre-commit.ci, husky, lefthook, Zuul, Bors, Mergify, TeamCity and Azure DevOps gated check-in, GitLab merged-results pipelines and merge trains, the "require branches up to date" setting, and the 10-minute gate guidance. The continuousdelivery.com page was read but supported none of the specific claims, so it was dropped from `sources`.
Method: docs-checked 2026-11-09 against pre-commit.com, martinfowler.com continuousIntegration, docs.github.com managing a merge queue
