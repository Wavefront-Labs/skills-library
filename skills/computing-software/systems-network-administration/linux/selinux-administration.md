---
id: computing-software.systems-network-administration.linux.selinux-administration
name: selinux-administration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, selinux, mandatory-access-control, mac, rhel, fedora, centos, audit2allow, semanage, restorecon, chcon, sestatus, booleans, context, type-enforcement, avc-denial, ausearch, setroubleshoot, security, hardening, semanage-fcontext, setenforce, semodule]
level: advanced
status: docs-checked
description: "Diagnose and fix SELinux AVC denials with contexts, booleans, and audit2allow — the targeted-policy workflow, not disabling it."
sources:
  - https://github.com/SELinuxProject/selinux-notebook/blob/main/src/global_config_files.md
  - https://github.com/SELinuxProject/selinux-notebook/blob/main/src/hardening.md
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-fcontext.8
  - https://github.com/SELinuxProject/selinux/blob/main/python/audit2allow/audit2allow.1
  - https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-boolean.8
  - https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/scripts/fixfiles.8
  - https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SELinux administration — fix the denial, don't disable the control

**Goal:** read an SELinux AVC denial, decide whether it's a mislabeled file or
a genuinely missing policy rule, and fix it with the narrowest change —
without ever reaching for `setenforce 0` as a permanent answer.

## 1. Mental model
SELinux is **type enforcement**: every process and file has a *context*
(`user:role:type:level`), and policy rules allow a *source type* to perform
an *action* on a *target type*. Discretionary permissions (owner/group/mode)
still apply underneath — SELinux can only say *no* on top, never *yes* when
DAC already says no. On RHEL/Fedora/CentOS it ships as `targeted` policy
(confines daemons, leaves normal user processes unconfined) — almost always
the right mode; `mls` is the policy for multi-level-security systems.

```bash
sestatus                       # mode (enforcing/permissive/disabled), policy name
getenforce                     # quick current mode
setenforce 0                   # TEMPORARY permissive, for testing only — resets on reboot
```
Permanent mode lives in `/etc/selinux/config` (`SELINUX=enforcing|permissive|disabled`);
`SELINUX=disabled` is slated for deprecation in favour of the `selinux=0` kernel command-line switch.

## 2. Reading a denial
```bash
ausearch -m avc -ts recent               # recent AVC denials from the audit log
ausearch -m avc -ts recent | audit2allow -w   # explain why access was denied
```
A denial line has the shape:
```
avc: denied { read write } for pid=1234 comm="httpd"
  scontext=system_u:system_r:httpd_t:s0
  tcontext=unconfined_u:object_r:user_home_t:s0
  tclass=file
```
Read it as: **source type** `httpd_t` tried `read write` on a **target type**
`user_home_t` file, and policy has no rule allowing it. The target context is
the first thing to check — a *mislabeled file* (the right type would have worked)
is a common cause, ahead of a missing rule.

## 3. Fix order (cheapest first)
1. **Relabel.** If the file context doesn't match what the service expects:
   ```bash
   matchpathcon /var/www/html/upload     # what the policy THINKS this path should be
   restorecon -Rv /var/www/html           # fix labels back to policy default
   chcon -t httpd_sys_content_t /path     # one-off override; LOST on next restorecon/relabel
   ```
   `chcon` is temporary (not in the policy database); for a persistent custom
   path, add it to the file-context database instead:
   ```bash
   semanage fcontext -a -t httpd_sys_content_t "/srv/myapp/uploads(/.*)?"
   restorecon -Rv /srv/myapp/uploads
   ```
   Writable content needs a writable-content type from your distribution's policy;
   find it with `semanage fcontext -l | grep httpd`.
2. **Booleans** — toggles for known, common policy variations, no compile step:
   ```bash
   getsebool -a | grep httpd              # list relevant booleans
   setsebool -P httpd_can_network_connect on   # -P persists across reboot
   ```
   Check booleans before writing a custom policy module — booleans such as
   `httpd_can_network_connect` and `httpd_can_sendmail` exist for common cases
   (list them with `getsebool -a`).
3. **Custom policy module** — only when neither of the above applies and the
   access is genuinely something the stock policy didn't anticipate:
   ```bash
   ausearch -m avc -ts recent | audit2allow -M mypolicy
   semodule -i mypolicy.pp
   ```
   `audit2allow` output is a *starting point, not a final answer* — it
   grants exactly what's in the log, including denials that were themselves
   a symptom of misconfiguration. Read the generated `.te` file before
   installing; don't pipe straight to `| audit2allow -M x && semodule -i x.pp`
   blind in production.

## 4. Gotchas
- **Never leave `setenforce 0` as the fix.** It's a diagnostic step; permanent
  permissive mode silently stops protecting anything while `sestatus` still
  looks "configured." If permissive is genuinely the operational decision,
  set it in `/etc/selinux/config`, document why, and revisit.
- A file's context is stored on the filesystem, so a file moved or copied into
  a new location can carry a label that does not match the policy for that path.
  Compare `ls -Z` with `matchpathcon <path>` and fix with `restorecon -Rv`.
- A full relabel after a policy/package upgrade: `touch /.autorelabel; reboot`
  (or `fixfiles onboot`) — faster than hunting denials one by one.
- `semanage` may be absent on a minimal image; install the distribution package that provides it.
- AppArmor and SELinux are mutually exclusive on one system in practice —
  see `computing-software.systems-network-administration.linux.apparmor-administration`
  for the path-based alternative used by Ubuntu/Debian/SUSE.

## Verify
- [ ] `sestatus` shows `Current mode: enforcing` in production (permissive only intentionally, documented).
- [ ] `ausearch -m avc -ts recent` is empty (or only expected/known entries) after a fix.
- [ ] `restorecon -Rv <path>` reports no changes needed — labels match policy expectation.
- [ ] Any custom `.pp` module's source `.te` was read before `semodule -i`, and grants only the specific access needed.
- [ ] The fixed service still works end to end (denial gone AND functionality confirmed, not just one or the other).

## Checked
Checked 2026-10-26 against the SELinux Notebook (main), the SELinuxProject/selinux man pages (semanage-fcontext, setsebool, audit2allow, fixfiles), the audit-userspace ausearch man page and the refpolicy apache.te boolean definitions.
Confirmed: `SELINUX=enforcing|permissive|disabled` and the planned deprecation of `disabled` in favour of `selinux=0`; targeted leaves unprivileged users unconfined; `ausearch -m avc -ts recent`; `audit2allow -M` and `-w`; `setsebool -P`; `semanage fcontext -a -t ... "/web(/.*)?"` then restorecon; `fixfiles onboot` and `/.autorelabel`; `httpd_can_network_connect` and `httpd_can_sendmail` booleans.
Removed as unconfirmed: the 80 percent statistic, the sealert command, the cp/mv labelling rule, and package names for semanage.
Method: documentation only; no commands were run.
