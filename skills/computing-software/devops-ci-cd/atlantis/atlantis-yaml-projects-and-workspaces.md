---
id: computing-software.devops-ci-cd.atlantis.atlantis-yaml-projects-and-workspaces
name: atlantis-yaml-projects-and-workspaces
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [atlantis-yaml, projects, workspaces, repo-config, yaml-anchors, symlinks]
level: practitioner
status: docs-checked
description: "Configure repo-level atlantis.yaml projects, workspaces, branches, symlinked dirs and YAML anchors."
sources: ["https://www.runatlantis.io/docs/repo-level-atlantis-yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis yaml projects and workspaces

The repo-root `atlantis.yaml` is optional and must start with `version: 3`. Atlantis reads it from the pull request branch, so keys that could run code (`workflows`, `workflow`, `plan_requirements`, `apply_requirements`, `import_requirements`) are restricted and need `allowed_overrides` in the server-side config.

Once `projects` is set, Atlantis stops auto-discovering and follows only the listed projects, unless `autodiscover.mode` is `enabled`.

Project keys:
- `dir` (required, relative to repo root, `.` for root).
- `name`: required when several projects share the same `dir` and `workspace`; used with `-p`.
- `workspace` (default `default`): cannot contain `/`, `\`, `..`, `$`, whitespace or control characters, or start with `-` or `~`.
- `branch`: regex matched against the PR base branch.
- `terraform_version`, `terraform_distribution`, `workflow`, `autoplan`, `repo_locks`, `silence_pr_comments` (`plan`/`apply`), `custom_policy_check`, `execution_order_group`, `depends_on`.

Multiple workspaces: repeat the same `dir` with different `workspace` values and target one with `atlantis plan -w staging -d project1`. A project represents one Terraform state; several states in one directory (via `-backend-config`) need a `name`.

DRY with YAML anchors: define `&template` on the first project and reuse with `<<: *template`, overriding `name`, `dir` and `workspace`.

Symlinks: Atlantis resolves symlinks in `dir`. A target outside the cloned repo is rejected with `project path traversal detected: path escapes base directory`. A symlinked plan file is deleted before a new plan is written.

Top-level extras: `automerge`, `delete_source_branch_on_merge`, `parallel_plan`, `parallel_apply`, `allowed_regexp_prefixes`.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Repo Level atlantis.yaml. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
