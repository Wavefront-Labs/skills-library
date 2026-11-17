---
id: computing-software.devops-ci-cd.nomad.job-revert
name: job-revert
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, job-revert, revert, rollback, job-history, job-version, tag, cli]
level: practitioner
status: docs-checked
description: "Roll back a Nomad job to an earlier version or tag with nomad job revert, find versions through nomad job history -p, and know the ACL capabilities needed."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/job/revert.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad job revert

Reverts a job to a prior version. List candidates first.

```
nomad job history -p example
nomad job revert example 0
```
Syntax: `nomad job revert [options] <job> <version|tag>`. A number reverts to that exact version; a string reverts to the version carrying that **tag**.

## Behaviour
Revert is a new submission of the old definition: in the example, reverting to version 0 produced a new version 2 (marked `Stable = true`) whose diff changed `image` from `redis:4.0` back to `redis:7`, and the monitor reported the evaluation and deployment like a normal update.

## Options
- `-detach` - return the evaluation ID without monitoring (check with `nomad eval status`).
- `-verbose`.

## ACLs
`submit-job` in the namespace; `list-jobs` if you use a job ID prefix; `read-job` to monitor when not detached.

## Related
`update { auto_revert = true }` automates this on deployment failure (`computing-software.devops-ci-cd.nomad.update-block`). Use `-p` on `job history` to see diffs between versions before picking one.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 job revert command page: syntax with version or tag, -detach, -verbose, ACLs, the worked example. Removed: the history-is-never-deleted claim.

Method: documentation only; no commands were run.
