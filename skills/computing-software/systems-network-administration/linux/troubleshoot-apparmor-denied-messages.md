---
id: computing-software.systems-network-administration.linux.troubleshoot-apparmor-denied-messages
name: troubleshoot-apparmor-denied-messages
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apparmor-denied, apparmor, aa-logprof, aa-complain, aa-status, audit-log]
level: practitioner
status: docs-checked
description: "Diagnose AppArmor DENIED audit messages: find the profile and operation, switch to complain mode, update profiles with aa-logprof or local overrides, and reload safely."
sources:
  - https://gitlab.com/apparmor/apparmor/-/wikis/AppArmor_Failures
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-logprof.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-genprof.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-complain.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/profiles/apparmor.d/local/README
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshoot AppArmor DENIED messages

## Find them
```bash
journalctl -k -g 'apparmor="DENIED"' --since -1h
grep 'apparmor="DENIED"' /var/log/audit/audit.log    # if auditd runs, messages go here instead of kern.log
dmesg | grep -i apparmor
```
Example:
```
audit: type=1400 apparmor="DENIED" operation="open" profile="/usr/sbin/mysqld" name="/data/mysql/ibdata1" pid=2211 comm="mysqld" requested_mask="r" denied_mask="r" fsuid=110
```
Read it as: profile `/usr/sbin/mysqld` blocked `open` with read on `/data/mysql/ibdata1`. `operation` names the attempted action (the AppArmor wiki shows `inode_unlink` in its sample message); `requested_mask` and `denied_mask` give the permissions.

## Confirm AppArmor is the cause
```bash
aa-status                          # loaded profiles and mode (enforce/complain)
aa-complain /usr/sbin/mysqld       # log instead of block (apparmor-utils)
# retry the action; if it now works, AppArmor was the cause
aa-enforce /usr/sbin/mysqld        # back to enforce after fixing
```

## Fix: local overrides (survive package updates)
Many distribution profiles include `local/<name>` files:
```
# /etc/apparmor.d/local/usr.sbin.mysqld
/data/mysql/ r,
/data/mysql/** rwk,
```
```bash
apparmor_parser -r /etc/apparmor.d/usr.sbin.mysqld     # reload that profile
```
Use local files for small additions and edit the profile itself for large policy changes (upstream `local/README`).

## Fix: interactively
```bash
aa-logprof        # reads logs, proposes rules, writes the profile
aa-genprof /opt/app/bin/server   # build a new profile by exercising the program
```
Prefer narrow globs (`/data/mysql/**`) over `/**`.

## Gotchas
- Docker containers run under `docker-default`; see the containers skill.
- Disabling a profile: `ln -s /etc/apparmor.d/usr.sbin.cupsd /etc/apparmor.d/disable/ && apparmor_parser -R /etc/apparmor.d/usr.sbin.cupsd`. Avoid `apparmor=0` on the kernel command line.

## Verify
- [ ] No new DENIED lines for the profile after the fix; profile back in enforce mode.

## Checked
Checked 2026-10-26 against the AppArmor sources on GitLab (master, latest commit 2026-10-23): the AppArmor_Failures wiki page, utils/aa-logprof.pod, aa-genprof.pod, aa-complain.pod and profiles/apparmor.d/local/README.
Confirmed: log locations (kern.log, messages, audit.log with auditd), the `denied_mask`/`requested_mask` fields and auditd's DENIED wording, aa-status first, aa-complain to test whether AppArmor is the cause, aa-logprof and aa-genprof workflows, the local include directory.
Removed as unconfirmed: the list of operation names, the capable/ownership advice and the symlink remark.
Method: documentation only; no commands were run.
