---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.linux-account-sudoers-and-shadow-analysis
name: linux-account-sudoers-and-shadow-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [sudoers, linux-forensics, linux-persistence, account-management-events, dfir]
level: practitioner
status: docs-checked
description: "Review Linux account integrity: passwd/shadow/group anomalies, UID 0 duplicates, password change dates, shadow field meanings, sudoers and sudoers.d drop-ins."
sources: ["https://man7.org/linux/man-pages/man5/shadow.5.html", "https://www.sudo.ws/docs/man/sudoers.man/", "https://attack.mitre.org/techniques/T1136/001/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux account, sudoers and shadow analysis

**Goal:** attackers create local accounts (MITRE T1136.001: on Linux typically with `useradd`, or by editing passwd/shadow
directly), give themselves root through sudo or UID 0, or change authentication. Account files are small and quick to review on
every compromised host.

## /etc/passwd and /etc/group
- More than one account with UID 0; service accounts with interactive shells; new accounts with UIDs out of sequence; home
  directories in unusual places; names that look like existing ones.
- Membership of privileged groups (for example the groups your sudoers rules grant rights to).

## /etc/shadow (shadow(5))
Nine colon-separated fields per line, in this order: login name, encrypted password, date of last password change, minimum age,
maximum age, warning period, inactivity period, account expiration date, reserved.
- Last password change is the number of days since 1970-01-01 00:00:00 UTC; convert it and compare with the incident window.
  Value 0 means the user must change the password at next login; an empty field means aging is disabled.
- An empty password field means the user can log in without a password (some applications may refuse it). A field starting with
  `!` means the password is locked; a value such as `!` or `*` that is not valid crypt(3) output means no UNIX password login,
  though other login methods may still work.
- Account expiration (field 8) is different from password expiration: it blocks the login itself.
- `/etc/shadow-` is the backup file written by the shadow toolsuite (not by every tool): compare it with the live file.

## sudo (sudoers)
- Read `/etc/sudoers` and every file included from it. `@includedir /etc/sudoers.d` (or the older `#includedir`) reads each file
  in the directory in sorted lexical order, skipping names that end in `~` or contain a `.`; so a drop-in with a dot in its name
  is not loaded, and an attacker file in that directory is. Package managers use the same directory.
- Rules with the `NOPASSWD:` tag remove the password prompt for the listed commands; review who they apply to.
- Logging is configurable: sudoers logs allowed and denied attempts by default, to syslog unless changed with the `syslog` and
  `logfile` settings (`log_allowed` and `log_denied` control what is logged). A change to these settings, or a changed
  `env_keep` list, is worth explaining.
- Check syntax of an extracted file with visudo's `-f` option (see the visudo manual); it does not catch alias redefinitions
  that span files.

## Timeline
- Filesystem times of passwd, shadow, group and their backups, and authentication-log entries for account creation or change.
- Authentication module (PAM) configuration and module files are outside the cited pages: treat them with a package-verification
  skill.

## Verify
All UID 0, sudo-capable and recently changed accounts are attributed to a person or a change record.

## Checked
Date: 2026-11-08.
Confirmed in shadow(5): nine fields and their order, days-since-epoch date, empty and `!` password meanings, account expiration
versus password expiration, `/etc/shadow-` backup note. Confirmed in the sudoers manual: `@includedir` and `#includedir`, sorted
order and the skip rule for `~` and `.` names, `NOPASSWD:` tag, default logging to syslog with `syslog`/`logfile`, `env_keep`,
visudo `-f` behaviour. Confirmed in T1136.001: `useradd` and editing passwd/shadow.
Removed (not in the cited pages): the awk and date one-liners, hash prefixes ($6$, $y$, $1$), `Defaults !logfile`/`!syslog` and
`env_keep += LD_PRELOAD` examples, `visudo -c`, `sudo -l -U`, the PAM module names and paths, and the auth-log message text.
Method: docs-only read of cited pages, 2026-11-08
