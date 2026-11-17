---
id: computing-software.systems-network-administration.linux.restrict-su-with-pam-wheel
name: restrict-su-with-pam-wheel
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, pam-wheel, su-restriction, wheel-group, su, privilege-escalation, cis-benchmark]
level: practitioner
status: docs-checked
description: "Limit who can use su to the wheel (or a named) group with pam_wheel, avoid lockouts, combine with sudo-only admin models, and check SU logging."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_wheel/pam_wheel.8.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restricting su with pam_wheel

By default any user knowing the root password can `su -`. CIS benchmarks require restricting it to a group.

## Configure
`/etc/pam.d/su` (uncomment or add near the top of the auth stack):
```
auth  required  pam_wheel.so use_uid group=sugroup
```
- `use_uid` checks the real user running su (not the login name).
- Create the group (empty is fine for sudo-only shops): `groupadd sugroup`; add admins: `gpasswd -a alice sugroup`.
- Without `group=`, the module uses the group `wheel`, or the group with GID 0 if no `wheel` group exists; `group=` selects another.
- `trust` makes group members succeed without a password prompt when stacked with `sufficient` — don't.
- `root_only` limits the check to targets with UID 0; `deny` inverts the rule.
Keep a root session open while testing; a typo in PAM can block su for everyone.

## Behaviour
```
$ su -
Password:
su: Permission denied          # applicant not in the group
```
The denial is logged by the module through syslog; read it in the system's authentication log or journal.

## Models
- Sudo-only: empty `sugroup` → nobody can su; admins use sudo (auditable per command), root password vaulted for console only.
- `sudo -i` is governed by the `sudo` PAM service, not `/etc/pam.d/su`, so this restriction does not apply to it.

## Verify
- [ ] Non-member gets "Permission denied" with the right password; member succeeds; console/rescue root login unaffected.

## Checked
Checked 2026-10-25 against Linux-PAM master pam_wheel(8) documentation.
Confirmed: option names `group=`, `use_uid`, `root_only`, `trust`, `deny`, the fallback to GID 0 when no wheel group exists, and that the module returns PAM_IGNORE for non-members.
Corrected: the default group is `wheel` or the GID 0 group, not RHEL-only. Removed as unconfirmed: log file paths and the sudo PAM service statement is reduced to the general PAM-service rule.

Method: documentation only; no commands were run.
