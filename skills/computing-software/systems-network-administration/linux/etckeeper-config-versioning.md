---
id: computing-software.systems-network-administration.linux.etckeeper-config-versioning
name: etckeeper-config-versioning
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, etckeeper, config-backup, etc-git, configuration-history, package-hooks, change-tracking, git, sysadmin]
level: practitioner
status: docs-checked
description: "Version /etc with etckeeper: init, commits around package transactions, reviewing and reverting changes with git, metadata, secrets handling and pushing off-host."
sources:
  - https://etckeeper.branchable.com/
  - https://manpages.debian.org/stable/etckeeper/etckeeper.8.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# etckeeper: /etc under git

**Goal:** every change to `/etc` (by you, a colleague or a package upgrade) is recorded,
and any file can be compared or restored in seconds.

## 1. Install and initialise
```bash
etckeeper init                    # sets up the repository (VCS from etckeeper.conf)
etckeeper commit "initial import"
```
Config: `/etc/etckeeper/etckeeper.conf`; its `VCS` setting selects git, mercurial, bazaar or darcs.

## 2. What happens automatically
- `etckeeper pre-install` runs from apt's `DPkg::Pre-Install-Pkgs` hook (or an equivalent hook of other
  package managers) and commits uncommitted changes before packages are installed or upgraded.
- `etckeeper post-install` runs from apt's `DPkg::Post-Invoke` hook and commits changes made by packages.
- Metadata that git does not normally track, such as the permissions of `/etc/shadow`, is stored.
- `etckeeper commit` notices when a user became root with sudo or su and records the original username.

## 3. Day to day
```bash
etckeeper vcs status               # runs "git status" in /etc
etckeeper vcs diff                 # what changed since the last commit
etckeeper commit "sshd: disable password auth (CHG-1234)"
git -C /etc log -p --since=yesterday
```
Commit your own changes with a ticket reference immediately; otherwise they are bundled into the next
package commit with a misleading message.

## 4. Off-host copy
```bash
git -C /etc remote add backup ssh://git@git.example.com/infra/etc-host.git
git -C /etc push backup HEAD
```
The remote must be private and access-controlled: `/etc` contains `shadow`, private keys and credentials.
Keep files you cannot store off-host out of the repository (see `etckeeper update-ignore`), knowing that
excluded files are then not versioned.

## Gotchas
- `etckeeper uninit` DESTROYS DATA (removes the VCS information); use it with care.
- It is not a substitute for config management: it records drift, it does not prevent it.

## Verify
- [ ] `git -C /etc log -3` shows commits from a recent package install.
- [ ] Changing a file and running `etckeeper commit` records it; `etckeeper vcs status` is clean afterwards.

## Checked
2026-10-28. Confirmed in the etckeeper project page and etckeeper(8): VCS options, `init`, `commit`, `vcs`,
`pre-install` and `post-install` hooks, sudo username recording, `update-ignore`, `uninit` warning, metadata
such as `/etc/shadow` permissions, pushing the repository elsewhere. Removed (not confirmed): daily
autocommit, `AVOID_*` and `PUSH_REMOTE` settings, `.etckeeper` file details, repository mode 0700, default
ignore entries, per-distro install behaviour.
Method: documentation only; no commands were run.
