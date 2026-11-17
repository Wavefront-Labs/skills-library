---
id: computing-software.cybersecurity-defensive.system-hardening.auditd-rules
name: auditd-rules
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [audit-log-management, auditd-rules, linux-auditing, augenrules, ausearch, execve-logging, immutable-audit]
level: advanced
status: docs-checked
description: "Write and deploy Linux auditd rules for identity, privilege, persistence and execution events, keep them performant, make them immutable and query with ausearch and aureport."
sources: ["https://github.com/linux-audit/audit-userspace/blob/master/docs/auditctl.8", "https://github.com/linux-audit/audit-userspace/blob/master/docs/audit.rules.7", "https://github.com/linux-audit/audit-userspace/blob/master/docs/augenrules.8", "https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_loginuid/pam_loginuid.8.xml", "https://github.com/Neo23x0/auditd"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux auditd rules

**Goal:** kernel-level audit records for security-relevant activity, with manageable volume and tamper protection.

## Layout
Rules in `/etc/audit/rules.d/*.rules` (files must end in `.rules`, merged in natural sort order) are compiled by `augenrules --load` into `/etc/audit/audit.rules`. augenrules emits the last `-D` first, then `-b`, `-f`, and the last `-e` as the final line, wherever they appear in the files. Check loaded rules: `auditctl -l`; status `auditctl -s`.

## Core rules
```
-D
-b 8192
-f 1
--backlog_wait_time 60000
# identity and auth
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/sudoers -p wa -k priv_esc
-w /etc/sudoers.d/ -p wa -k priv_esc
-w /etc/ssh/sshd_config -p wa -k sshd
# persistence
-w /etc/cron.d/ -p wa -k cron
-w /var/spool/cron/ -p wa -k cron
-w /etc/systemd/system/ -p wa -k systemd
-w /root/.ssh/ -p wa -k rootkey
# kernel modules
-a always,exit -F arch=b64 -S init_module,finit_module,delete_module -k modules
# privileged command execution by real users
-a always,exit -F arch=b64 -S execve -F euid=0 -F auid>=1000 -F auid!=unset -k root_cmd
-a always,exit -F arch=b32 -S execve -F euid=0 -F auid>=1000 -F auid!=unset -k root_cmd
# time changes
-a always,exit -F arch=b64 -S adjtimex,settimeofday,clock_settime -k time_change
# make immutable (last line; changes need reboot)
-e 2
```
Include `arch=b32` variants for syscall rules on 64-bit systems or 32-bit calls evade them.

## Performance
- Syscall rules are evaluated on every syscall; filter with `-F` (auid, euid, path) and avoid logging all execve on busy servers unless shipping volume is planned.
- Exclude noise with `never` rules placed at the top of the list, because an event triggers on the first matching rule (for example `-a never,exit -F arch=b64 -S all -F exe=/path/to/agent`; `-F exe=` is documented in auditctl(8) with `-S all`).
- Watch the lost-record and backlog counters in `auditctl -s`; `auditctl --reset-lost` resets the lost counter.

## Query
`ausearch -k priv_esc -ts this-week -i` (ausearch(8) defines the keyword `today` as "now", so use `this-week`, `yesterday` or an explicit date and time), `aureport --auth --failed`, `aureport -x --summary`. Forward the audit log to the SIEM with your log shipper.

## Gotchas
- `-e 2` blocks rule changes until reboot - plan changes accordingly.
- `auid` (login UID) survives `sudo`/`su`, which is what makes attribution work; the `pam_loginuid` session module sets it and belongs only in entry-point services such as login, sshd and crond, not in sudo or su.
- An unset login UID is written as `unset` (or -1, 4294967295) in rules, which is why `auid>=1000` is paired with `auid!=unset`.
- osquery's audit-based tables cannot share the audit netlink socket with auditd.

## Verify
- [ ] `auditctl -s` shows the configuration locked (enabled flag 2) and a lost-record counter of 0.
- [ ] Editing `/etc/sudoers.d/test` produces a `priv_esc` event in the SIEM.

## Checked
Checked 2026-10-25 against the audit-userspace manual pages auditctl(8), audit.rules(7), augenrules(8), ausearch(8) and aureport(8) (linux-audit/audit-userspace), and the Linux-PAM pam_loginuid page. Confirmed: `-D`, `-b`, `-f 1`, `--backlog_wait_time`, `-e 2` locking (last command), comma-separated `-S` lists, `arch=` for performance, `auid>=1000 -F auid!=unset`, never rules at the top (first match wins), augenrules ordering and the `.rules` suffix, ausearch `-k`/`-ts`/`-i`, aureport `--auth`, `--failed`, `-x`, `--summary`. Corrected the ausearch `-ts today` example. The Neo23x0 rule set is cited as a source repository only; its individual rules were not re-read.

Method: documentation only; no commands were run.
