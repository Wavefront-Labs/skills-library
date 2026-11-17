---
id: computing-software.systems-network-administration.linux.dnf-yum-dependency-resolution
name: dnf-yum-dependency-resolution
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dnf, yum, rpm, rhel, fedora, centos, rocky, almalinux, libsolv, sat-solver, repo-priority, module-streams, dnf-history, weak-dependencies, sysadmin, package-management, rpm-query]
level: advanced
status: docs-checked
description: "Debug dnf/yum dependency conflicts on RHEL-family systems: the libsolv SAT solver, repo priorities, module streams, and dnf history rollback."
sources:
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://dnf.readthedocs.io/en/latest/modularity.html
  - https://rpm.org/documentation.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dnf/yum dependency resolution — SAT solving and module streams

**Goal:** debug a dnf/yum conflict by reading what the solver actually tried,
use repo priorities to control which of several repos wins for a package,
and navigate module streams (the RHEL 8+ layer that trips up anyone coming
from plain rpm/apt mental models) — plus roll back a bad transaction.

## 1. rpm vs dnf — same split as dpkg vs apt
`rpm` installs and queries individual packages; `dnf` resolves the dependency graph and fetches
from configured repos, then drives rpm to do the install.
```bash
rpm -qa | grep <pkg>              # installed packages, low-level
rpm -qR <pkg>                      # dependencies as declared in the spec
rpm -q --whatprovides '/usr/bin/foo'   # which package owns this file
dnf repoquery --deplist <pkg>      # dnf's view of the same dependency tree
```

## 2. Reading a conflict
dnf reports a "Problem:" block listing the requests it could not satisfy. A typical report
contains lines such as "nothing provides X needed by Y" or a conflict between two packages.
"Nothing provides X" means the capability is not in any enabled repo at the needed version:
check which repos are enabled and whether a repo providing it (for example EPEL) is disabled.
```bash
dnf repoquery --provides <pkg>             # capabilities a package provides
dnf repoquery --unneeded                   # leaf packages installed as dependencies that are no longer needed
```
`--best` makes `dnf upgrade` fail with the reason instead of skipping packages that cannot be
installed because of dependencies; `--skip-broken` does the opposite.

## 3. Weak dependencies (dnf's Recommends equivalent)
```bash
dnf install --setopt=install_weak_deps=False <pkg>   # skip weak dependencies
dnf repoquery --recommends <pkg>
```
`install_weak_deps` (default True) pulls in packages linked by weak dependency relations
(`Recommends` or `Supplements`) when a new package is installed.

## 4. Repo priority — which repo wins when two provide the same package
```bash
dnf repolist                               # enabled repos and package counts
# /etc/yum.repos.d/myrepo.repo
[myrepo]
priority=1          # lowest value wins (default 99)
```
With `priority`, a candidate from the repo with the lowest priority value is picked, possibly despite being a lower version.
`excludepkgs=`/`includepkgs=` in a repo section restrict which packages a repo may supply.

## 5. Module streams (RHEL 8+/Fedora) — the layer that confuses apt/yum-7 veterans
```bash
dnf module list                            # available streams
dnf module install postgresql:15           # enable the stream and install a profile
dnf module switch-to postgresql:13          # switch streams, changing package versions and removing packages no longer available in the new stream
dnf module reset postgresql                 # back to unselected
```
A module stream is a version line of a package family that is active system-wide. If a module
conflict blocks an install, a different stream is probably already enabled; use `dnf module switch-to`
or `dnf module reset` first. Modular streams are a RHEL 8/9 and Fedora feature.

## 6. History and rollback — dnf's biggest advantage over apt here
```bash
dnf history list                            # every transaction, numbered
dnf history info 42                         # exactly what that transaction did
dnf history undo 42                         # reverse it
dnf history rollback 40                     # undo all transactions performed after transaction 40
```
If some transactions cannot be undone because of the current rpmdb state, dnf does not undo them.

## Gotchas
- `dnf upgrade` with no package name upgrades everything including the kernel; `-x/--exclude=<spec>` excludes packages for one run.
- When two repos supply the same package name, set `priority`, `excludepkgs` or `includepkgs` rather than relying on version order.
- Removing a package does not reset a module stream; use `dnf module reset` explicitly.

## Verify
- [ ] `dnf history info <latest>` describes exactly the change you meant to make, before trusting the system is in the intended state.
- [ ] `dnf module list --installed` shows only the streams intended to be active.
- [ ] A test `dnf upgrade --dry-run`/`--assumeno` after any repo priority change shows the expected package source winning.

## Checked

Checked against dnf4 command_ref.rst and conf_ref.rst (rpm-software-management/dnf, last push 2026-10-23).
Confirmed: `install_weak_deps` default True and its meaning, `priority` default 99 with lowest value winning, `excludepkgs`/`includepkgs`, `--best`, `--skip-broken`, `-x/--exclude`, repoquery `--unneeded`, `--recommends`, `--provides`, `--deplist`, module `install`, `switch-to` (changes versions and removes packages from the old stream), `reset`, `history undo` and `rollback`.
Removed as unconfirmed: libsolv/SAT description, the verbatim conflict message, the `%{reason}` query format, the claim that priority needs a plugin (it is a core repo option), lock-file path, apt-versus-dnf comparisons and the EPEL overlap advice.

Method: documentation only; no commands were run.
