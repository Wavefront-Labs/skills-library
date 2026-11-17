---
id: computing-software.digital-forensics-incident-response.log-analysis.linux-syslog-auditd-and-ssh-log-forensics
name: linux-syslog-auditd-and-ssh-log-forensics
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [linux-forensics, auditd, ausearch, auditctl, syslog, journald, ssh-forensics, authentication-log, bash-history, cron-persistence, systemd-persistence, utmp, wtmp, btmp, lastlog, dfir, incident-response]
level: advanced
status: draft
description: "Investigate a compromised Linux host: auditd rules and ausearch/aureport, SSH/auth log analysis, bash-history reconstruction and its gaps, cron/systemd persistence hunting."
sources: ["https://man7.org/linux/man-pages/man8/auditd.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux syslog, auditd and SSH log forensics

**Goal:** the Windows-centric log-analysis skill
(computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting)
doesn't transfer directly — Linux has no built-in Sysmon-equivalent process-creation
log unless auditd (or eBPF-based tooling) was configured *before* the incident. Know
what's on by default, what needs pre-configuration, and where the gaps are.

## 1. What's on by default vs what needs auditd
- `/var/log/auth.log` (Debian/Ubuntu) or `/var/log/secure` (RHEL/CentOS) — SSH
  authentication attempts (success/failure, source IP, key vs password), `sudo`
  invocations, PAM events. This is on by default and is the first place to check for
  brute force (`Failed password` repetition), successful logins from unexpected
  source IPs, and sudo privilege escalation.
- **Process execution is NOT logged by default.** Without auditd execve rules
  configured in advance (or an EDR agent), there is no built-in record of what
  commands ran, when, by whom — the single biggest gap vs Windows Sysmon/4688
  coverage. If auditd wasn't configured before the incident, process-execution
  history has to be reconstructed indirectly (bash history, below) with all its
  limitations, not retrieved directly.
- `journald` (systemd-based distros) centralizes syslog plus service start/stop/crash
  events; `journalctl -u sshd`, `journalctl --since`/`--until` for a time-bounded
  pull. Binary journal format persists across reboots if `Storage=persistent` was set
  — check this wasn't left at the volatile default before assuming history survived.

## 2. auditd, when it was running
```
ausearch -k <rule_key> -ts today            # search by configured rule key
ausearch -ui <uid> -ts recent               # search by actor
aureport --summary                           # quick overview across all audit records
```
`auditd` only logs what explicit rules (`auditctl -a always,exit -F arch=b64 -S execve
...`) tell it to — a default/minimal auditd config logs very little beyond what the
distro's baseline (often tied to a compliance profile like CIS/STIG) enables. Check
`auditctl -l` (or the rule files under `/etc/audit/rules.d/`) for what was actually
being captured before assuming execve/file-access coverage exists for the incident
window.

## 3. Bash history — useful but adversary-controlled and incomplete
`~/.bash_history` is the closest thing to a command-execution record absent auditd,
but:
- It's **written on shell exit** (or periodically), so a live/still-open shell's
  recent commands aren't flushed yet — don't assume the file is current.
- **Trivially evaded**: `unset HISTFILE`, `export HISTSIZE=0`, `history -c`, piping
  through tools that don't go through an interactive shell at all (a single `curl |
  bash` one-liner from automation leaves no bash-history trace). An attacker with any
  competence disables or clears it — its *absence* for a session that clearly did
  something is itself a finding, not a dead end.
- Lacks timestamps unless `HISTTIMEFORMAT` was set before the session (retroactively
  invisible) — correlate command order against auth.log login/logout timestamps for
  that session instead of trusting history's own ordering alone.
- `.bash_history` for root and every user account that was accessed matters — check
  all of them, not just the initially compromised account.

## 4. Persistence hunting
- **Cron**: `/etc/crontab`, `/etc/cron.d/*`, per-user `crontab -l` for every user
  (including service accounts), and `/etc/cron.{hourly,daily,weekly,monthly}/` —
  check file modification times against the incident window, not just content.
- **systemd**: a malicious unit file or timer dropped in `/etc/systemd/system/` or
  `/lib/systemd/system/` and enabled; `systemctl list-unit-files --state=enabled` for
  an inventory, cross-referenced against a known-good baseline for the distro/image
  if one exists.
- `/etc/rc.local`, shell profile files (`/etc/profile.d/`, `~/.bashrc`, `~/.bash_profile`)
  and SSH `authorized_keys` additions (check every user's, including ones not
  normally logged into) round out the common persistence locations.

## 5. Login session accounting
`utmp`/`wtmp`/`btmp` (`last`, `lastb`, `lastlog` commands) give login session history
(wtmp), failed logins (btmp) and last-login-per-user (lastlog) — binary files that,
like Windows logon events, can be tampered with by a root-level attacker; cross-check
against auth.log's own record of the same sessions rather than trusting one source.

## Verify
- Confirm whether auditd execve rules were actually active before the incident
  before treating process-history gaps as "nothing happened" rather than "not logged."
- Check bash history across every user account touched, and treat an unexpectedly
  empty/missing history file as a finding worth flagging, not a dead end.
- Cross-check wtmp/btmp/lastlog against auth.log for the same sessions.

Unconfirmed: default log paths/retention and auditd baseline rules vary meaningfully
across distros and hardening profiles — verify the specific distro/config in the
engagement rather than assuming RHEL or Debian defaults apply universally.
