---
id: computing-software.systems-network-administration.linux.rpm-scriptlets-and-triggers
name: rpm-scriptlets-and-triggers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rpm, rpm-scriptlets, pre-post-scripts, rpm-triggers, filetriggers, spec-file, failed-scriptlet, rhel, fedora, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Read, write and debug RPM scriptlets: %pre/%post/%preun/%postun ordering and the $1 install/upgrade argument, triggers and file triggers, and recovering from a failing scriptlet."
sources:
  - https://rpm-software-management.github.io/rpm/manual/triggers.html
  - https://rpm-software-management.github.io/rpm/manual/file_triggers.html
  - https://github.com/rpm-software-management/rpm/blob/master/docs/man/rpm-scriptlets.7.scd
  - https://github.com/rpm-software-management/rpm/blob/master/docs/man/rpm-sysusers.7.scd
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RPM scriptlets and triggers

**Goal:** know what code a package runs as root during install/upgrade/removal, write
scriptlets that behave on upgrade, and fix a transaction broken by one.

## 1. Inspect before you install
```bash
rpm -qp --scripts package.rpm         # all scriptlets in a file
rpm -q --scripts nginx                # installed package
rpm -q --triggers nginx; rpm -q --filetriggers <pkg>
```

## 2. Order during an upgrade (old -> new)
The order for a single package upgrade (rpm-scriptlets(7)) is: `%pretrans` (new), `%preuntrans` (old),
`%pre` (new), unpack new files, `%post` (new), `%triggerin`, `%preun` (old), erase old files,
`%postun` (old), `%posttrans` (new), `%postuntrans` (old); file triggers and `%triggerprein`/`%triggerun`
slots sit in between (see the man page for the full list).
`$1` is the number of installed instances of the package once the operation completes. It is `1` on
initial install and `0` on final removal; otherwise it is an upgrade, downgrade or parallel install:
| Scriptlet | `$1` on install | on upgrade | on erase |
|---|---|---|---|
| `%pre`/`%post` | 1 | 2 | — |
| `%preun`/`%postun` | — | 1 | 0 |
So "only on full removal": `if [ $1 -eq 0 ]; then ... fi` in `%preun`.

## 3. Writing them (spec file)
```spec
%post
%systemd_post myapp.service

%preun
%systemd_preun myapp.service

%postun
%systemd_postun_with_restart myapp.service
```
User and group creation should use rpm's native sysusers support instead of scripting: ship a
`%{_sysusersdir}/myapp.conf` with lines such as `g myapp -` and `u! myapp - "My app" /var/lib/myapp -`
(rpm-sysusers(7)). Use the distro `%systemd_*` macros instead of hand-rolled systemctl calls.
Scriptlets cannot be interactive and must not rely on their output being seen. A non-zero exit from
`%pre` or `%preun` stops the install or removal of that package; rpm cannot roll back a transaction,
so scriptlets should always exit zero.

## 4. File triggers
`%filetriggerin -- /usr/lib/myapp/plugins` runs after the installation of each triggering package that
installs files under that path prefix and receives the matching paths on stdin, one per line.
`%transfiletriggerin` runs once at the end of the transaction instead. File triggers are meant to centralise
cache and registry updates.

## 5. Recover from a broken scriptlet
```bash
rpm -e --noscripts brokenpkg               # skip all scriptlets (then clean up manually)
rpm -e --nopreun brokenpkg                 # skip only the %preun scriptlet
dnf install --setopt=tsflags=noscripts x   # tsflags noscripts: install without scriptlets (diagnosis only)
```
`--noscripts` leaves users, services and state the package would have cleaned; check
`rpm -q --scripts` for what to undo by hand.

## Gotchas
- Scriptlets cannot be interactive; do not rely on prompts or visible output.
- A non-zero exit from any scriptlet is reflected as a transaction error, but rpm cannot roll back.

## Verify
- [ ] `rpm -qp --scripts` reviewed for third-party packages before deployment.
- [ ] Test install, upgrade (old → new) and erase in a VM; service state is correct after each.

## Checked

Checked against rpm-scriptlets(7), rpm-sysusers(7) and rpm(8) in rpm-software-management/rpm docs/man (last push 2026-10-22), and dnf4 conf_ref.rst for `tsflags`.
Confirmed: scriptlet slots and the upgrade execution order, `$1` semantics, exit-status rules for `%pre`/`%preun`, `rpm -q --scripts/--triggers/--filetriggers`, `--noscripts` and `--nopreun`, file trigger behaviour and stdin paths, `tsflags=noscripts`, native sysusers support, `%systemd_post/preun/postun_with_restart` macros (systemd repository macros.systemd.in).
Fixed: file triggers run once per triggering package (`%filetriggerin`) while only `%transfiletriggerin` runs once per transaction; the `%sysusers_create_compat` macro was replaced by rpm's native sysusers files (the macro is not in systemd's macros.systemd.in). Removed as unconfirmed: the minimal-environment/no-TTY remark, container tsflags remark and the exact dnf error text.

Method: documentation only; no commands were run.
