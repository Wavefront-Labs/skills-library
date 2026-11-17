---
id: computing-software.systems-network-administration.linux.zypper-package-management
name: zypper-package-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, zypper, suse, opensuse, sles, rpm, zypper-patch, zypper-dup, lpic-1]
level: practitioner
status: docs-checked
description: "Manage packages on SUSE/openSUSE with zypper: repos, install/remove, patches vs updates, locks, dup for Tumbleweed and SP upgrades, search and rollback with snapper."
sources:
  - https://github.com/openSUSE/zypper/blob/master/doc/zypper.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zypper (SUSE/openSUSE)

## Everyday
```bash
zypper refresh                         # zypper ref
zypper search nginx                    # se
zypper info nginx
zypper install nginx                   # in; --no-recommends skips recommended packages
zypper remove --clean-deps nginx       # rm; -u, --clean-deps removes dependencies that become unneeded
zypper what-provides /usr/bin/dig      # wp; internally becomes `search --provides --match-exact`
zypper search --provides 'libssl.so.3()(64bit)'
```
## Repositories
```bash
zypper repos -d                        # lr -d: more information such as URI, priority, type
zypper addrepo --refresh <URI> devtools   # ar; --refresh turns on autorefresh
zypper modifyrepo -p 90 devtools       # mr; priority 1 is highest, 99 is the default, -p 0 resets to the default
zypper removerepo devtools
```
## Updating
| Command | Use |
|---|---|
| `zypper patch` | install all available needed patches (similar to `zypper update -t patch`) |
| `zypper list-patches --category security` | list pending patches of a category (`-g`, `--category`) |
| `zypper update` (`up`) | update installed packages with newer versions where possible; does not change package vendor unless allowed in `/etc/zypp/vendors.d` |
| `zypper dist-upgrade` (`dup`) | apply the state of the repositories to the system: upgrades or downgrades packages, removes packages that are gone from the repos, handles splits and renames |
| `zypper ps -s` | processes using deleted files (typically deleted shared libraries) in a short table, to decide which services to restart |
| `zypper needs-rebooting` | exit code 102 (`ZYPPER_EXIT_INF_REBOOT_NEEDED`) = reboot suggested, otherwise 0 |

## Locks and rollback
`zypper addlock kernel-default` (`al`), `zypper locks` (`ll`), `zypper removelock` (`rl`); locks are stored in `/etc/zypp/locks`.

## Gotchas
- `--non-interactive` (`-n`) answers prompts with defaults; scripts should handle the exit codes (0 OK, 100 patches available, 101 security patches available, 102 reboot suggested, 103 package manager restart needed).
- `zypper patch` installs patches affecting the package management first and asks you to run it again.

## Verify
- [ ] `zypper list-patches` empty after patching; `zypper ps -s` shows no stale processes; `zypper verify` (dependencies of installed packages satisfied) is clean.

## Checked

Checked against doc/zypper.8.txt and doc/zypper.8.d in openSUSE/zypper (last push 2026-10-23).
Confirmed: `what-provides` (`wp`) behaviour, `remove --clean-deps` (`-u`), `--no-recommends`, `repos -d`, repository priority semantics (1 highest, default 99, `-p 0` resets), `patch`, `list-patches --category`, `update` vendor behaviour, `dist-upgrade` semantics, `ps -s`, `needs-rebooting` and exit code 102, `addlock/locks/removelock` and `/etc/zypp/locks`, `--non-interactive`, exit codes 100 to 103, `verify`.
Removed as unconfirmed: SUSEConnect, snapper rollback, the Tumbleweed `up` versus `dup` rule, the `search -s` meaning, and the openSUSE example repository URL.

Method: documentation only; no commands were run.
