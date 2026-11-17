---
id: computing-software.systems-network-administration.linux.repair-broken-apt-dpkg-state
name: repair-broken-apt-dpkg-state
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, dpkg, apt-fix-broken, dpkg-configure-a, dpkg-lock, half-installed, unmet-dependencies]
level: practitioner
status: docs-checked
description: "Recover from interrupted or broken apt/dpkg runs: dpkg --configure -a, apt --fix-broken install, lock files, half-configured packages and failing maintainer scripts."
sources:
  - https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html
  - https://manpages.debian.org/bookworm/apt/apt-get.8.en.html
  - https://www.debian.org/doc/manuals/debian-faq/pkg-basics.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing broken apt/dpkg state

## Symptoms → first command
| Message | Do |
|---|---|
| interrupted dpkg run | `dpkg --configure -a` (`--pending` configures only pending packages) |
| unmet dependencies | `apt --fix-broken install` (`apt-get -f install`, `-f` is `--fix-broken`) |
| cannot get a lock | another apt or dpkg process is running: check with `ps aux` and wait |
| `dpkg returned an error code` | read the lines above it for the failing maintainer script |

## Locks
Do not delete lock files by hand while any apt or dpkg process exists; wait for it to finish, then run `dpkg --configure -a`.

## Failing maintainer scripts
```bash
dpkg --audit                                  # packages in bad states
dpkg -l | grep -vE '^(ii|rc)'                 # states other than installed/config-files-only (dpkg(1), Package states)
```
Read the error above the dpkg failure, fix the cause, then rerun `dpkg --configure -a`.

## Dependency tangles
```bash
apt -o Debug::pkgProblemResolver=yes install pkg      # enables resolver debug output (apt.conf(5))
apt-cache policy pkg dep                               # mixed repos / pinned versions
dpkg --remove --force-depends badpkg                   # ignore Depends problems for this removal (dpkg(1)); then fix-broken
```

## Gotchas
- `--force-*` options override dpkg safety checks; follow them with a fix.

## Verify
- [ ] `dpkg --audit` prints nothing; `apt-get check` (checks for broken dependencies) reports none.

## Checked

Checked against dpkg(1) (guillemj/dpkg, 2026-10), apt-get(8) and apt.conf(5) (Debian/apt doc/, last commit 2025-11-10).
Confirmed: `dpkg --configure -a|--pending`, `--audit`, `--remove` with `--force-depends`, `-f/--fix-broken`, `apt-get check`, `Debug::pkgProblemResolver`.
Removed as unconfirmed: exact error strings, lock-file paths and fuser command, maintainer script paths and the `exit 0` trick, mixed-release and full-disk remarks.

Method: documentation only; no commands were run.
