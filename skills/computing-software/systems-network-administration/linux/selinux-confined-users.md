---
id: computing-software.systems-network-administration.linux.selinux-confined-users
name: selinux-confined-users
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, selinux, selinux-users, semanage-login, semanage-user, confined-users, staff-u, user-u, sysadm-u, unconfined-u, sudo-role-transition, security, hardening, sysadmin]
level: advanced
status: docs-checked
description: "Map Linux logins to confined SELinux users: user_u/staff_u/sysadm_u roles, semanage login, sudo role transitions for admins, and testing confinement."
sources:
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-login.8
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-user.8
  - https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/newrole/newrole.1
  - https://github.com/SELinuxProject/selinux-notebook/blob/main/src/hardening.md
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/SELinuxProject/refpolicy/blob/main/policy/modules/services/ssh.te
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux confined users

**Goal:** limit what an account can do even if it gets a root shell — by mapping logins
to confined SELinux users instead of the default `unconfined_u`.

## 1. The SELinux users
| SELinux user | Role | Notes |
|---|---|---|
| `unconfined_u` | unconfined_r | mostly unconfined; in the targeted policy unprivileged users and root are unconfined |
| `user_u` | user_r | the confined user for unprivileged accounts |
| `staff_u` | staff_r | unprivileged login that can escalate to `sysadm_r` or another admin role |
| `sysadm_u` | sysadm_r | a more confined administrator than the `root` SELinux user |

Other SELinux users (for example `guest_u`, `xguest_u`) depend on the distribution's policy; list
users and their roles with `semanage user -l`.

## 2. Map logins
```bash
semanage login -l                                  # Login → SELinux user, MLS range
semanage login -a -s user_u alice                  # one user
semanage login -a -s staff_u %wheel                # a Linux group (% prefix)
semanage login -m -s user_u -r s0 __default__      # all users not listed → confined
semanage user -l                                   # roles allowed per SELinux user
```
The user must log in again; check with `id -Z` (e.g. `staff_u:staff_r:staff_t:s0-s0:c0.c1023`).

## 3. Admins: staff_u + sudo role transition
```
# /etc/sudoers.d/admins
%wheel ALL=(ALL) TYPE=sysadm_t ROLE=sysadm_r ALL
```
The sudoers `ROLE=` and `TYPE=` tags (sudoers `SELinux_Spec`) set the SELinux role and type the command runs in.
`newrole -r sysadm_r` is the manual alternative. Direct SSH login as `sysadm_u` is governed by the
`ssh_sysadm_login` boolean (default false in refpolicy): `setsebool -P ssh_sysadm_login on`.

## 4. Booleans
```bash
getsebool -a        # booleans your policy offers; names vary by distribution
```

## 5. Test
As the confined user: `id -Z`; try the privileged actions you expect to be blocked;
`ausearch -m AVC -ts recent -su user_t` shows what was blocked (`-su` matches the subject context).

## Gotchas
- Before changing `__default__` to a confined user, map your admin group to `staff_u` and keep a root console open.
- A group mapping needs the `%` prefix (`%wheel`).

## Verify
- [ ] `semanage login -l` shows the intended mapping; `id -Z` after login matches.
- [ ] A `user_u` account is blocked from the administrative actions you expect; an admin using the sudoers `ROLE=`/`TYPE=` entry runs as `sysadm_r`/`sysadm_t` (`id -Z`).

## Checked
Checked 2026-10-26 against the SELinux Notebook (main), the SELinuxProject/selinux man pages (semanage-login, semanage-user, newrole), the sudo sudoers manual source and refpolicy ssh.te.
Confirmed: `semanage login -a/-m -s SEUSER`, `%group` mapping and `__default__` (man page examples); user_u/staff_u/sysadm_u roles and escalation of staff_u with newrole (Notebook hardening chapter); sudoers `ROLE=`/`TYPE=` SELinux_Spec; the `ssh_sysadm_login` boolean (default false); ausearch `-su`.
Removed as unconfirmed: per-user can/cannot claims for guest_u and xguest_u, the user_exec/execmod booleans, home-label and rootless tool notes.
Method: documentation only; no commands were run.
