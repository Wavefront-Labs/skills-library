---
id: computing-software.devops-ci-cd.atlantis.atlantis-server-side-repo-config
name: atlantis-server-side-repo-config
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [repos-yaml, allowed-overrides, allow-custom-workflows, repo-config-file, allowed-workflows]
level: advanced
status: docs-checked
description: "Write the server-side repos.yaml with repo matching, allowed_overrides, allowed_workflows and per-repo defaults."
sources: ["https://www.runatlantis.io/docs/server-side-repo-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis server side repo config

Enable the server-side config with `atlantis server --repo-config=path/to/repos.yaml`, or pass JSON via `--repo-config-json` or `ATLANTIS_REPO_CONFIG_JSON`. Top-level keys: `repos`, `workflows`, `policies`, `metrics`, `team_authz`.

A built-in first entry always exists: `id: /.*/`, `branch: /.*/`, empty requirements, `workflow: default`, `allowed_overrides: []`, `allow_custom_workflows: false`.

Repo keys: `id` (exact `{VCS hostname}/{org}/{name}` or a regex in slashes), `branch` regex, `repo_config_file` (default `atlantis.yaml`), `workflow`, `plan_requirements`, `apply_requirements`, `import_requirements`, `allowed_overrides`, `allowed_workflows`, `allow_custom_workflows`, `delete_source_branch_on_merge`, `repo_locks`, `policy_check`, `custom_policy_check`, `autodiscover`, `silence_pr_comments`, `pre_workflow_hooks`, `post_workflow_hooks`.

Matching: if several entries match, the last match wins, and undefined keys do not override earlier matches. With `/.*/` setting `allow_custom_workflows: true` and `apply_requirements: [approved]`, a later entry setting only `apply_requirements: []` ends with empty requirements and custom workflows still allowed.

`allowed_overrides` lists keys a repo `atlantis.yaml` may set: `apply_requirements`, `workflow`, `delete_source_branch_on_merge`, `repo_locking`, `repo_locks`, `custom_policy_check`. `allowed_workflows` limits which server-side workflows projects may select; every project is checked, with the error `workflow '<name>' is not allowed for this repo`. `allow_custom_workflows: true` lets anyone who can open a PR run arbitrary code on the server.

Several Atlantis servers on one repo: give each a different `repo_config_file` such as `atlantis-production.yaml`.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Server Side Repo Config. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
