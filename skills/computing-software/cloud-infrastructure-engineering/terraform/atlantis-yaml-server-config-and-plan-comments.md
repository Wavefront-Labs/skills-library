---
id: computing-software.cloud-infrastructure-engineering.terraform.atlantis-yaml-server-config-and-plan-comments
name: atlantis-yaml-server-config-and-plan-comments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, atlantis, atlantis-yaml, atlantis-server, atlantis-plan-comment, pull-request-automation, code-review, atlantis-workflows, apply-requirements]
level: advanced
status: docs-checked
description: "Configure Atlantis (repo atlantis.yaml projects, server-side repos.yaml workflows, apply requirements) and review changes through its PR plan comments."
sources: ["https://www.runatlantis.io/docs/repo-level-atlantis-yaml.html", "https://www.runatlantis.io/docs/server-side-repo-config.html", "https://www.runatlantis.io/docs/command-requirements.html", "https://www.runatlantis.io/docs/using-atlantis.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Atlantis: config and PR plan comments

## Repo-level atlantis.yaml
```yaml
version: 3
automerge: false              # default false: merge the PR when all plans are applied
parallel_plan: true
projects:
  - name: prod-network
    dir: live/prod/network    # relative to repo root; . for root
    workspace: default
    autoplan:
      when_modified: ["*.tf", "*.tfvars", "../../../modules/network/**/*.tf"]
      enabled: true
    apply_requirements: [approved, mergeable, undiverged]
    workflow: prod
```
- `when_modified` uses `.dockerignore` syntax, paths relative to the project `dir`, and
  applies to automatic and manual plans. A custom value **replaces the defaults
  entirely** (defaults: `**/*.tf*`, `**/*.tofu`, `**/*.tofu.json`, `**/terragrunt.hcl`,
  `**/.terraform.lock.hcl`), so list local module paths or module edits will not plan.
- `plan_requirements`, `apply_requirements` and `import_requirements` are restricted
  keys; the only supported values are `approved`, `mergeable` and `undiverged`.
- `terraform_version` must be semver-compatible; the project can also choose the
  `terraform` or `opentofu` distribution.

## Server-side repos.yaml
```yaml
repos:
  - id: /github.com/<ORG>/infra-.*/
    allowed_overrides: [workflow, apply_requirements]
    allow_custom_workflows: false          # default false: PRs cannot define their own workflows
    apply_requirements: [approved, mergeable]
    pre_workflow_hooks:
      - run: <COMMAND>
workflows:
  prod:
    plan:
      steps:
        - init
        - plan
    apply:
      steps: [apply]
```
A repo can only override the keys listed in `allowed_overrides`. `plan` steps accept
`extra_args`, and `run` steps run arbitrary commands, which is why custom workflows
from PRs should stay off.

## Working in the PR
- Re-plan one project with `atlantis plan -p <project>` (the name from atlantis.yaml;
  it cannot be combined with `-d` or `-w`). Without arguments it plans the projects it
  thinks were modified.
- `atlantis apply -p <project>` applies the plan for that project; `-d <dir>` selects
  by directory instead.
- `atlantis unlock` removes all Atlantis locks and discards all plans for the PR; a
  single plan can be unlocked in the Atlantis UI.
- `atlantis state rm` must satisfy both `apply_requirements` and `import_requirements`.

## Reviewing a plan comment
- Read the per-project plan summary; any destroy or replace needs a justification.
- Ensure every expected project planned (a missing project means a `when_modified` gap).

## Gotchas
- Atlantis holds credentials with apply power; use `apply_requirements` and restrict
  `allow_custom_workflows` and `allowed_overrides`.
- `undiverged` requires the PR's project files to be ahead of the base branch;
  `mergeable` requires the PR to be mergeable. On GitHub and Gitea, `approved` is met
  when at least one reviewer's latest review is a current approval.

## Verify
- [ ] Editing a module file triggers plans for every project using it.
- [ ] `atlantis apply` is rejected until the PR meets `apply_requirements`.

## Checked
2026-10-31. Confirmed against the four Atlantis pages cited: `automerge` default false,
`parallel_plan`, `when_modified` semantics and defaults, supported requirement values,
`allowed_overrides`, `allow_custom_workflows` default false, `pre_workflow_hooks`,
workflow `steps` and `extra_args`, `-p`/`-d` rules, `atlantis unlock` behaviour,
`state rm` requirements, `approved`/`mergeable`/`undiverged` meanings. Removed:
server flags (`--repo-allowlist`, `--require-approval`, `--enable-policy-checks`,
`--autoplan-modules`, `--checkout-strategy`), the `conftest` workflow step, the
`-lock-timeout` example, pinned `terraform_version` value, the project-lock-until-merge
claim, the comment-truncation and collapsible-plan claims, and sample plan-output text.
Method: documentation only; no commands were run.
