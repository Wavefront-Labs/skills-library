---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-candidate-vs-running-config-commit
name: pan-os-candidate-vs-running-config-commit
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [candidate-config, pan-os, commit, rollback, running-config, config-lock, commit-lock, load-config]
level: practitioner
status: draft
description: "Work with the PAN-OS candidate versus running config, partial commits, locks, diffs and rollback to a saved version."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/firewall-administration/manage-configuration-backups"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: change config safely, preview what a commit will do, and recover fast if it breaks traffic.

PAN-OS keeps a candidate config (edited, not live) and a running config (active). Nothing takes effect until `commit`.

```
configure
validate full
commit description "add web rule"
commit partial admin alice
exit
request config-lock add comment "maintenance window"
request commit-lock add comment "freeze"
save config to pre-change-2026-11-03.xml
load config from pre-change-2026-11-03.xml
load config version 41
commit
```

Rollback options
- `revert config` discards uncommitted candidate edits.
- `load config version N` then `commit` restores an earlier committed version (versions are listed in Device > Setup > Operations > Config Audit).
- Config Audit compares any two versions side by side; use the GUI Preview Changes before committing.

Gotchas
- A commit lock stops other admins committing, not editing; forgetting to remove it blocks the team (`request commit-lock remove`).
- `commit force` can publish a colleague's half-finished edits sitting in the shared candidate. Prefer `commit partial admin <name>` or admin-scoped commits.
- Commit validation errors for a missing profile reference are common after deleting objects.

## Verify
```
show jobs all
show config running | match hostname
```
The commit job must end `FIN` with result `OK`.
