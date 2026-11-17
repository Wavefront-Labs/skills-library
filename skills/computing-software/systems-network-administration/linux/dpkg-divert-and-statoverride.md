---
id: computing-software.systems-network-administration.linux.dpkg-divert-and-statoverride
name: dpkg-divert-and-statoverride
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dpkg, dpkg-divert, dpkg-statoverride, package-file-override, permissions-persistence, debian, ubuntu, lpic-2, sysadmin]
level: practitioner
status: verified
description: "Replace or re-permission files owned by Debian packages so upgrades don't undo it: dpkg-divert to move a packaged file aside, dpkg-statoverride to pin owner/mode."
sources:
  - https://manpages.debian.org/stable/dpkg/dpkg-divert.1.en.html
  - https://manpages.debian.org/stable/dpkg/dpkg-statoverride.1.en.html
  - https://www.debian.org/doc/debian-policy/ap-pkg-diversions.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dpkg-divert and dpkg-statoverride

**Goal:** override a file a package owns (binary, non-conffile config, script) or its
permissions, and have the change survive every future upgrade of that package.

## 1. Why plain edits fail
Files under `/usr`, `/lib`, `/bin` and non-conffiles in `/etc` are replaced on every package
upgrade. `chmod` on a packaged binary is reset too. (Real conffiles are handled by dpkg's conffile prompts; don't divert those.)

## 2. dpkg-divert: move the packaged version aside
```bash
dpkg-divert --list                                   # existing diversions
dpkg-divert --local --rename --divert /usr/bin/foo.distrib --add /usr/bin/foo
install -m 0755 my-foo-wrapper /usr/bin/foo          # your version takes the path
dpkg-divert --truename /usr/bin/foo                  # → /usr/bin/foo.distrib
```
Future upgrades of the package write their file to `/usr/bin/foo.distrib`; yours stays.
Common use: wrap a binary (the wrapper calls `foo.distrib "$@"`).
Undo:
```bash
rm /usr/bin/foo
dpkg-divert --local --rename --remove /usr/bin/foo   # moves foo.distrib back
```
`--local` diverts every package's version of the file (for an admin's locally modified copy); `--package <name>` diverts it for all packages except that one.
Use `--rename` to actually move the file; without it only the database changes (`--no-rename` is the current default; dpkg prints a warning asking for the flag to be given explicitly).

## 3. dpkg-statoverride: persistent owner/mode
```bash
dpkg-statoverride --list
dpkg-statoverride --update --add root ssl-cert 0640 /etc/ssl/private/site.key   # the group must exist (ssl-cert comes from the ssl-cert package)
dpkg-statoverride --update --add root adm 4750 /usr/bin/someprog   # restrict a setuid binary to group adm
dpkg-statoverride --remove /usr/bin/someprog       # then reinstall package or chmod back
```
`--update` applies the change now; without it only the database is changed and it takes
effect at the next package install. dpkg applies overrides whenever it unpacks the file.
Documented use: install normally-setuid programs without the setuid flag, or executable only by a group.

## Gotchas
- Diverting a file another package already diverts fails — check `dpkg-divert --list` first.
- Diversions are invisible in `ls`; document them (config management, `/etc/README.local`).
- Removing the package leaves your file; removing a diversion without `--rename` leaves the
  `.distrib` file orphaned.
- Statoverride on a path that doesn't exist yet needs no `--update` (with it dpkg only warns that the file does not exist); dpkg applies it on install.

## Verify
- [ ] `dpkg-divert --list | grep foo` / `dpkg-statoverride --list` shows the entry.
- [ ] `apt install --reinstall <pkg>` leaves your file/permissions intact (`sha256sum`, `stat -c '%U %G %a'`).

## Checked

Checked against dpkg-divert(1) and dpkg-statoverride(1) pod sources (guillemj/dpkg, last push 2026-10-19).
Confirmed: `--add`, `--remove`, `--list`, `--truename`, `--local` and `--package` semantics, `--rename` versus `--no-rename` default, `.distrib` default divert name, statoverride `--add user group mode path`, `--update` applies immediately only if the path exists, overrides apply when a package is installed.
Removed as unconfirmed: the dpkg -S diversion output, conffile list path, policy-rc.d and cron script uses, debsums check.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (dpkg 1.22, procps 4.0.4): dpkg-divert --list, --local --rename --divert --add moving the file, --truename, wrapper surviving apt-get install --reinstall while the package file lands in .distrib, re-adding the same diversion, --package clashing with an existing local diversion, --remove --rename restoring, --add without --rename leaving the file in place (with a warning to give the flag explicitly), --rename --add moving it; dpkg-statoverride --add with and without --update, override surviving a reinstall, --remove not changing the file until reinstall, error for a missing group, warning for a missing path. Not run: --package diversions for a real second package, setuid use.
