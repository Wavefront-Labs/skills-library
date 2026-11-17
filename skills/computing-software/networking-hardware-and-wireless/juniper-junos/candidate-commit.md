---
id: computing-software.networking-hardware-and-wireless.juniper-junos.candidate-commit
name: candidate-commit
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, candidate-config, commit, commit-check, commit-model, active-config]
level: practitioner
status: draft
description: "Understand Junos candidate vs active configuration, commit check, commit comment and how a failing commit behaves."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Candidate configuration and the commit model
Goal: use the candidate/commit model so a change is validated before it goes live.

Edits go to the candidate configuration. Nothing changes on the data plane until `commit`. The commit syntax-checks, validates cross-references, then activates.

```
user@host# commit check
configuration check succeeds
user@host# commit comment "add ospf to uplink, CHG-1234"
commit complete
user@host# show system commit
user@host> show system commit
```

- Each commit is stored; the last 50 are kept (`rollback 0..49`) with the comment and user.
- `commit and-quit` commits then leaves configuration mode.
- `commit synchronize` pushes to the other routing engine on dual-RE systems (or set `system commit synchronize` permanently).
- `commit at "2026-12-01 02:00:00"` schedules a commit.

Gotcha: a commit applies the entire candidate, including someone else's uncommitted edits on a shared candidate. Always run `show | compare` first.

## Verify
- `show system commit` lists your commit comment at index 0.
- `show configuration | compare rollback 1` is empty immediately after commit.
