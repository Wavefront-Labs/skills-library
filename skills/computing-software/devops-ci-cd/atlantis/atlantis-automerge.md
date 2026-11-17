---
id: computing-software.devops-ci-cd.atlantis.atlantis-automerge
name: atlantis-automerge
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [automerge, merge-method, auto-merge-disabled, pull-request-merge]
level: practitioner
status: docs-checked
description: "Enable Atlantis automerge after all plans are applied and choose the merge method."
sources: ["https://www.runatlantis.io/docs/automerging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis automerge

Atlantis can merge a pull request automatically once all plans have been applied.

Enable either way:
1. Server flag `--automerge` (global; an explicit repo-config setting takes priority).
2. Repo `atlantis.yaml`:

```yaml
version: 3
automerge: true
projects:
- dir: .
```

If a repo has an `atlantis.yaml`, each project must be listed under `projects`.

To skip automerge for a single run, use `atlantis apply --auto-merge-disabled`.

Merge method: set a server default with `--automerge-method` or `ATLANTIS_AUTOMERGE_METHOD`, and override per command with `atlantis apply --auto-merge-method <method>`. Valid values are `merge`, `rebase` and `squash`. This is currently implemented only for GitHub.

Requirements:
- All plans must succeed before any plan can be applied. If `dir2/` fails to plan, `atlantis apply -d dir1` is blocked even though `dir1` planned fine; fix `dir2` and push so autoplan reruns.
- All autoplanned projects, directories or workspaces must be applied before Atlantis merges.
- The Atlantis VCS user must have permission to merge pull requests.

Related: `delete_source_branch_on_merge: true` in `atlantis.yaml` or repo config deletes the source branch after merge.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Automerging. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
