---
id: computing-software.systems-network-administration.linux.permission-denied-triage
name: permission-denied-triage
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, permission-denied, eacces, eperm, selinux, acls, systemd-sandboxing, troubleshooting]
level: practitioner
status: docs-checked
description: "Systematically resolve 'Permission denied' (EACCES/EPERM): identity, path traversal, ACL mask, SELinux/AppArmor, mounts, capabilities, chattr, sandboxing."
sources:
  - https://man7.org/linux/man-pages/man2/open.2.html
  - https://man7.org/linux/man-pages/man7/capabilities.7.html
  - https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/using_selinux/troubleshooting-problems-related-to-selinux_using-selinux
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Permission denied" triage

Work outward from the process to the object. Reproduce as the real identity first.

## 1. Who is really doing it?
Confirm the effective user and groups of the process (`id <user>`, `ps` for the pid). open(2) lists EACCES for "the
requested access to the file is not allowed, or search permission is denied for one of the directories in the path
prefix". Group changes need a new login or a service restart to apply.

## 2. Classic DAC
Check every directory in the path for search (`x`) permission, then the file mode and owner. Fix the narrowest
layer that fails.

## 3. SELinux (RHEL family)
```bash
getenforce
ausearch -m AVC,USER_AVC,SELINUX_ERR,USER_SELINUX_ERR -ts recent
```
`/var/log/audit/audit.log` is the first place to look for an SELinux denial (auditd must be running). To test
whether SELinux is the cause, `setenforce 0` switches to permissive mode; switch back with `setenforce 1` and fix
the cause instead: relabel with `restorecon -R -v <path>` after fixing file contexts, or enable the right SELinux
boolean. The Red Hat "Troubleshooting problems related to SELinux" chapter walks through each step.

## 4. Capabilities
Actions such as binding low ports, raw sockets, `chown` by non-root or ptrace fail with EPERM unless the process has
the matching capability (`CAP_NET_BIND_SERVICE`, `CAP_NET_RAW`, `CAP_CHOWN`, `CAP_SYS_PTRACE`). capabilities(7)
describes file capabilities (`setcap`) and the ambient set for non-root helpers.

## 5. Other layers to check
Mount options, file attributes, POSIX ACL masks, AppArmor, systemd sandboxing and network-filesystem identity mapping
can each return "Permission denied": look up the relevant manual for your distribution before changing them.

## Verify
- [ ] The fix is the narrowest one found by the first failing layer; the operation succeeds as the real user/service
  without `setenforce 0` or `chmod 777`.

## Checked
2026-10-28. Confirmed in open(2), capabilities(7) and the Red Hat SELinux troubleshooting chapter: EACCES wording,
capability names, `setcap`, ambient capabilities, `getenforce`, the `ausearch` invocation, audit.log, `setenforce`,
`restorecon`, SELinux booleans. Removed as unconfirmed: `ps -o label`, `systemctl show` properties, `namei`, `lsattr`
immutable/append-only EPERM claim, `findmnt`, `ls -Z`, AppArmor log filter, Yama ptrace_scope, systemd sandbox
directives and `systemd-run` test, NFS and CIFS specifics.
Method: documentation only; no commands were run.
