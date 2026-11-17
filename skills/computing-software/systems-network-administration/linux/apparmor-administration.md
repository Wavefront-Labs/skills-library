---
id: computing-software.systems-network-administration.linux.apparmor-administration
name: apparmor-administration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apparmor, mandatory-access-control, mac, ubuntu, debian, suse, profile, enforce-mode, complain-mode, aa-genprof, aa-logprof, aa-status, aa-complain, aa-enforce, security, hardening, path-based, apparmor-profile-syntax, apparmor-abstractions]
level: advanced
status: docs-checked
description: "Write and debug AppArmor profiles — enforce vs complain mode, aa-genprof/aa-logprof, and reading denials from the kernel log."
sources:
  - https://gitlab.com/apparmor/apparmor/-/blob/master/parser/apparmor.d.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/parser/apparmor_parser.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-genprof.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-logprof.pod
  - https://gitlab.com/apparmor/apparmor/-/wikis/AppArmor_Failures
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AppArmor administration — path-based confinement without a labeling system

**Goal:** confine a process to the files, capabilities and network access it
actually needs using AppArmor's profile files, move it from learning mode to
enforcement safely, and read a denial back to the exact line to fix.

## 1. Mental model (vs SELinux)
AppArmor is **path-based**, not label-based: a profile names a binary
(`/usr/sbin/nginx`) and lists file *paths* with permissions
(`/var/www/html/** r`), rather than tagging files with a type that moves
with them. That makes profiles human-readable and quick to hand-write, but
means a symlink or bind-mount to an un-listed path falls outside the profile
unless you account for it explicitly — SELinux's label travels with the
inode, AppArmor's rule doesn't. Check `aa-status` to see whether it is active on your system.

```bash
aa-status                      # which profiles are loaded, enforce vs complain, unconfined processes
systemctl status apparmor      # service state
cat /sys/module/apparmor/parameters/enabled   # Y = kernel support present
```

## 2. Profile anatomy
Profiles live in `/etc/apparmor.d/`, named after the binary path with slashes
turned to dots (`/usr/sbin/nginx` → `usr.sbin.nginx`):
```
#include <tunables/global>

/usr/sbin/nginx {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  capability net_bind_service,
  network inet stream,

  /etc/nginx/**       r,
  /var/log/nginx/*.log w,
  /var/www/html/**     r,
  /run/nginx.pid       rw,

  deny /home/**        rwx,     # explicit deny rule
}
```
Permission letters: `r` read, `w` write, `a` append-only, `x` execute (needs
a qualifier: `ix` inherit profile, `px` switch to the target's own profile,
`ux` unconfined; a bare `x` is only allowed in rules with the `deny` qualifier, per apparmor.d(5)).

## 3. Load, test, enforce
```bash
apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx   # parse + reload one profile
aa-complain /usr/sbin/nginx     # switch to complain: log would-be denials, don't block
# exercise the app through its real workload here
aa-logprof                      # interactively reviews the log, offers to add rules to the profile
aa-enforce /usr/sbin/nginx      # flip to enforcing once the profile looks complete
```
`aa-genprof /path/to/binary` does the complain → exercise → `aa-logprof`
cycle from scratch for a binary with no profile yet — the standard way to
build a new one rather than hand-writing every rule blind.

## 4. Reading denials
Denials are logged to `/var/log/kern.log`, `/var/log/messages` or (with auditd)
`/var/log/audit/audit.log`, depending on how auditing is set up:
```
audit: type=1400 apparmor="DENIED" operation="open"
  profile="/usr/sbin/nginx" name="/etc/ssl/private/key.pem"
  pid=1234 comm="nginx" requested_mask="r" denied_mask="r"
```
`profile=` is the confined program, `name=` the path it tried to touch,
`requested_mask`/`denied_mask` the permission. Fix is almost always: add that
exact path (or a glob covering its sibling files) with the needed
permission to the profile, then `apparmor_parser -r`.

```bash
journalctl -k | grep -i apparmor | grep -i denied
```

## 5. Gotchas
- **Complain mode still logs but never blocks** — don't mistake a quiet
  complain-mode run for "the profile is complete"; it means the workload
  path you exercised didn't hit anything missing, not that nothing is
  missing. Exercise every code path (including error/cron/backup paths)
  before flipping to enforce.
- Editing a profile file does nothing until `apparmor_parser -r` (or a
  service restart that reloads it) — unlike SELinux booleans there's no
  separate "persist" step, the file *is* the source of truth, but it must be
  reparsed.
- `unconfined` processes (shown by `aa-status`) have no profile at all and
  are not protected — a newly installed daemon is unconfined by default
  until a profile exists and is loaded for it.
- Abstractions (`#include <abstractions/base>`) pull in common rule bundles
  (DNS, shared libs) — skip them and a profile fails in surprising ways
  (can't resolve hostnames, can't load `.so` files) that look unrelated to
  your own rules.
- Explicit `deny` rules are still enforced in complain mode: complain mode only converts
  implicit denials into logged ALLOWED events (apparmor.d(5)). A `deny` rule's rejections
  are quieted in the log unless the rule has the `audit` prefix (AppArmor wiki).

## Verify
- [ ] `aa-status` shows the target binary's profile loaded and in `enforce` mode.
- [ ] `journalctl -k | grep DENIED` is empty after the full workload (including error paths) runs under enforce.
- [ ] `apparmor_parser -r <profile>` returns no syntax errors after any edit.
- [ ] The profile denies access it shouldn't need (spot-check: `ls /home` from inside the confined process fails if the profile has no rule granting it).

## Checked
Checked 2026-10-26 against the AppArmor sources on GitLab (master, latest commit 2026-10-23): parser/apparmor.d.pod, apparmor_parser.pod, utils/aa-genprof.pod, aa-logprof.pod, and the AppArmor_Failures wiki page.
Confirmed: profile syntax (`include`, `capability`, `network`, file rules), ix/px/ux transitions and the bare-`x`-only-with-deny rule, complain-mode semantics (explicit denials are not converted), `apparmor_parser -r`, the aa-genprof complain/exercise/aa-logprof cycle, log locations and the `denied_mask` field, `/sys/module/apparmor/parameters/enabled`.
Removed as unconfirmed: the distribution-default sentence, and the wrong claim that `audit` controls whether deny rules are enforced in complain mode (it controls logging quieting).
Method: documentation only; no commands were run.
