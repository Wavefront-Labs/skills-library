---
id: computing-software.systems-network-administration.linux.apparmor-local-overrides-and-tunables
name: apparmor-local-overrides-and-tunables
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apparmor, apparmor-local-overrides, apparmor-tunables, local-include, tunables-home, alias, apparmor-parser, ubuntu, debian, security, sysadmin]
level: practitioner
status: docs-checked
description: "Customise packaged AppArmor profiles without editing them: rules in /etc/apparmor.d/local/, tunables like @{HOME} and home.d, alias rules for moved directories, and reloading."
sources:
  - https://gitlab.com/apparmor/apparmor/-/blob/master/profiles/apparmor.d/local/README
  - https://gitlab.com/apparmor/apparmor/-/blob/master/parser/apparmor.d.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/parser/apparmor_parser.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/profiles/apparmor.d/tunables/global
  - https://gitlab.com/apparmor/apparmor/-/blob/master/profiles/apparmor.d/tunables/home
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppArmor local overrides and tunables

**Goal:** let a confined service read a non-default data path (or an extra home directory
location) in a way that survives package upgrades.

## 1. Why not edit the profile
Profiles in `/etc/apparmor.d/` belong to packages, and package updates can conflict with local
edits. Many shipped profiles end with a local include (upstream `local/README`):
```
  include if exists <local/usr.sbin.mysqld>
```
so, if your shipped profile has that line, `/etc/apparmor.d/local/usr.sbin.mysqld` is yours to edit
(create it if it is missing). Use it for small additions; make large policy changes in the profile itself.

## 2. Local rule example (MySQL datadir moved to /srv/mysql)
```
# /etc/apparmor.d/local/usr.sbin.mysqld
/srv/mysql/ r,
/srv/mysql/** rwk,
```
```bash
apparmor_parser -r /etc/apparmor.d/usr.sbin.mysqld     # reload the main profile (it includes local/)
systemctl restart mysql
journalctl -k -g 'apparmor="DENIED"' --since -5min     # confirm no new denials
```
Write only the minimum rules that the DENIED lines ask for (`requested_mask`, `name=`).

## 3. Tunables (variables)
- `/etc/apparmor.d/tunables/global` includes `home`, `multiarch`, `proc`, `alias`, `kernelvars`, `system`, `xdg-user-dirs`, `share`, `etc` and `run`.
- `@{HOME}` = `@{HOMEDIRS}/*/ /root/`; `@{HOMEDIRS}` = `/home/` by default.
- Homes elsewhere: add a file instead of editing `home`:
```
# /etc/apparmor.d/tunables/home.d/site.local
@{HOMEDIRS}+=/srv/home/ /data/users/
```
Then reload all profiles: `apparmor_parser -r /etc/apparmor.d/`.
- Custom variables in a local file: `@{APP_DATA}=/srv/app /opt/app/data` used as `@{APP_DATA}/** r,`.

## 4. alias for relocated trees
```
# /etc/apparmor.d/tunables/alias  (system-wide aliases)
alias /var/www/ -> /srv/www/,
```
Alias rules remap one path to another for site-specific layouts, after variable resolution, and must
appear in the preamble before the profile. Use alias for moved standard paths; use local rules for
genuinely extra paths.

## Gotchas
- Tunable changes need **every** profile reloaded, not just one; a reboot also works.
- A syntax error in a local file stops the profile from compiling; `apparmor_parser -Q -r <profile>` skips loading into the kernel, so you can test compilation without changing the running policy.

## Verify
- [ ] `apparmor_parser -r` succeeds with no errors; `aa-status` still shows the profile in enforce mode.
- [ ] The service works from the new path and the kernel log shows no new `DENIED` entries for it.

## Checked
Checked 2026-10-26 against the AppArmor sources on GitLab (master, latest commit 2026-10-23): profiles/apparmor.d/local/README, tunables/global and tunables/home, parser/apparmor.d.pod and apparmor_parser.pod, and the upstream usr.sbin.dnsmasq profile.
Confirmed: the `include if exists <local/NAME>` convention and the local directory purpose; `@{HOMEDIRS}=/home/` and `@{HOME}=@{HOMEDIRS}/*/ /root/`; `tunables/home.d` and the `+=` assignment; the real tunables/global include list; alias rule grammar (`alias PATH -> PATH,` in the preamble) and `/etc/apparmor.d/tunables/alias`; `apparmor_parser -r` and `-Q`.
Removed as unconfirmed: dpkg conffile behaviour, `alias.d`, `systemctl reload apparmor`, and the bind-mount remark. The MySQL profile name is an illustration; the upstream tree ships the same local-include pattern in profiles such as dnsmasq.
Method: documentation only; no commands were run.
