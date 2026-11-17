---
id: computing-software.systems-network-administration.linux.systemctl-list-dependencies
name: systemctl-list-dependencies
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, list-dependencies, systemd-target, unit-tree, reverse-dependencies, wants]
level: intro
status: docs-checked
description: "Read unit and target dependency trees with systemctl list-dependencies (--reverse, --all, --before/--after) to see why a unit starts or what a target pulls in."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.special.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemctl list-dependencies

## Questions it answers
```bash
systemctl list-dependencies multi-user.target          # what this target pulls in (Wants/Requires...), recursive for targets
systemctl list-dependencies --all sshd.service         # full recursion through non-target units too
systemctl list-dependencies --reverse nfs-client.target  # who wants/requires this — "why is it running?"
systemctl list-dependencies --after network-online.target   # ordering: what must start before it
systemctl list-dependencies --before sshd.service
systemctl list-dependencies --plain default.target   # flat list, no tree
```


## Related views
- `systemctl show -p Wants -p Requires -p After -p WantedBy foo.service` — raw properties.
- `systemd-analyze critical-chain foo.service` — the time-critical ordering chain at boot.
- `systemd-analyze dot 'sshd.service'` - dependency graph in Graphviz dot format.
- `ls /etc/systemd/system/*.wants/` — what `enable` created.

## Typical uses
- A service starts that you disabled → `--reverse` shows another unit or a socket/timer pulls it in;
  `mask` it if it must never start.
- Comparing a broken host with a good one: `--plain` output of `default.target`, diff.
- Before switching default target, see what goes missing.

## Gotchas
- Default output recurses only into targets; use `--all` for full trees (long).
- Ordering (`--after/--before`) is not dependency — a unit listed there won't be started by it.

## Verify
- [ ] You can explain each enabled unit's presence by a path in `list-dependencies --reverse`.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: list-dependencies follows `Requires=`, `Requisite=`, `Wants=`, `ConsistsOf=`, `BindsTo=`, `Upholds=`; only targets are expanded unless `--all`; `--reverse`, `--after`, `--before`, `--plain`; `systemd-analyze critical-chain` and `dot`; `systemctl show -p`. Removed the status-dot colour legend and the shell pipelines.

Method: documentation only; no commands were run.
