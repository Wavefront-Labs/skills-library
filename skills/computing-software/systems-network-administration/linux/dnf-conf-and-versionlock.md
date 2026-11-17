---
id: computing-software.systems-network-administration.linux.dnf-conf-and-versionlock
name: dnf-conf-and-versionlock
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dnf, yum, dnf-conf, dnf-config, versionlock, dnf-versionlock, exclude, package-pinning, installonly-limit, rhel, fedora, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Tune dnf behaviour in dnf.conf (gpgcheck, exclude, installonly_limit, cache, parallel downloads, best) and pin package versions with the versionlock plugin."
sources:
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/config_manager.html
  - https://dnf5.readthedocs.io/en/latest/commands/versionlock.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnf.conf and versionlock

**Goal:** make dnf behave predictably on servers and keep specific packages at a tested
version while everything else updates.

## 1. /etc/dnf/dnf.conf essentials
```ini
[main]
gpgcheck=1                  # verify package signatures (documented default is False; the RPM security policy can only be strengthened by it)
installonly_limit=3         # installonly packages (kernels) kept; default 3, minimum 2, 0 = unlimited
clean_requirements_on_remove=True
best=False                  # documented default False: go with a lower version if the latest cannot be installed; True fails instead
skip_if_unavailable=False   # True = continue and disable a repo that could not be synchronised
max_parallel_downloads=10   # documented default 3, maximum 20
fastestmirror=False         # True uses TCP socket latency to pick a mirror
keepcache=False
excludepkgs=kernel* firefox   # alias exclude=; excluded from all operations (--disableexcludes overrides)
defaultyes=False
proxy=http://proxy.example.com:3128
```
Per-repo options (`excludepkgs=`, `includepkgs=`, `priority=` with default 99 and lowest value wins, `module_hotfixes=`) go in the
`.repo` file section. One-off overrides: `dnf --setopt=install_weak_deps=False install x`,
`dnf --disableexcludes=all upgrade kernel`. Show effective config on dnf4: `dnf config-manager --dump` (dnf-plugins-core).
dnf5 has its own option reference (`man dnf5.conf`); check it for renamed options.

## 2. versionlock
```bash
dnf install python3-dnf-plugin-versionlock           # dnf4: versionlock plugin (dnf-plugins-core); dnf5 has `dnf5 versionlock`
dnf versionlock add postgresql16-server-16.4         # lock to the matching NEVRA(s)
dnf versionlock add --raw 'nginx-1:1.24.*'           # --raw uses the spec as written instead of resolving to NEVRAs
dnf versionlock list
dnf versionlock exclude kernel-core-5.14.0-503*      # exclude matching versions from transactions
dnf versionlock delete postgresql16-server
dnf versionlock clear
```
dnf4 keeps locks in the file named by `locklist` in `/etc/dnf/plugins/versionlock.conf` (the file must exist); dnf5 uses the TOML file `/etc/dnf/versionlock.toml`. Commit it to config management.
The plugin applies excludes only to transactions, not to `repoquery`, `list` or `info`, and not to local rpm files.

## 3. exclude vs versionlock
| | `exclude=` | versionlock |
|---|---|---|
| Effect | package excluded from all operations | other versions of the package are excluded |
Use versionlock for "stay on this version", exclude for "never touch this".

## Gotchas
- Locking a library can block updates of packages that need a newer version — review locks regularly.
- `excludepkgs=kernel*` stops all kernel updates; use `dnf versionlock exclude` for one known-bad build.

## Verify
- [ ] `dnf upgrade --assumeno` does not offer other versions of the locked package.
- [ ] `dnf versionlock list` matches the tracked list in config management.

## Checked

Checked against the dnf4 docs (rpm-software-management/dnf doc/conf_ref.rst, last push 2026-10-23), dnf-plugins-core docs versionlock.rst and config_manager.rst (last push 2026-10-22) and dnf5 docs (versionlock.8.rst, dnf5.conf.5.rst, last push 2026-10-23).
Confirmed: option names, defaults and ranges above (gpgcheck False, best False, installonly_limit 3 with minimum 2, max_parallel_downloads 3 and maximum 20, priority 99 lowest wins, excludepkgs/includepkgs, fastestmirror, keepcache, defaultyes, proxy); versionlock subcommands add/exclude/list/delete/clear and `--raw`; versionlock.conf `locklist`; dnf5 `/etc/dnf/versionlock.toml`; `dnf config-manager --dump`.
Fixed: wildcard version specs need `--raw`; the RHEL default claim for `best` was removed (check your distro's shipped dnf.conf). Removed as unconfirmed: the fixed lock-file path for dnf4, check-update behaviour, the Satellite remark and the comparison of dependency deadlock risk.

Method: documentation only; no commands were run.
