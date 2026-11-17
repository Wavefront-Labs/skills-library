---
id: computing-software.cybersecurity-defensive.system-hardening.aide-file-integrity
name: aide-file-integrity
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [file-integrity-monitoring, aide, fim, integrity-database, baseline, intrusion-detection, cis-control]
level: practitioner
status: docs-checked
description: "Deploy AIDE file integrity monitoring on Linux: tune aide.conf rules, initialise and protect the baseline, schedule checks, and update the database after approved changes."
sources: ["https://github.com/aide/aide/blob/master/doc/aide.conf.5", "https://github.com/aide/aide/blob/master/doc/aide.1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AIDE file integrity monitoring

**Goal:** detect unauthorised changes to system binaries and configuration on Linux hosts, with a trustworthy baseline.

## Install and initialise
```
# install the aide package from your distribution
aide --init             # writes the new database (database_out)
# move it to the path named by database_in (aide --version shows the defaults)
aide --check
```

## Tune `/etc/aide.conf`
```
# rule groups (NORMAL and LOG are names defined here; built-in groups are R, L, >, H, X and E)
NORMAL = p+i+n+u+g+s+m+c+acl+selinux+xattrs+sha512
LOG = p+u+g+n+acl+selinux+ftype      # growing logs: watch perms, not content
/boot   NORMAL
/bin    NORMAL
/sbin   NORMAL
/usr    NORMAL
/etc    NORMAL
/var/log LOG
!/var/log/journal
!/etc/mtab
!/var/lib/docker
```
Rules are regular expressions that must start with `/` and are matched from the start of the full path (implicit `^`); a leading `!` excludes matches and recurses into children, which are excluded only if they also match. Exclude volatile paths to avoid alert fatigue; include `/etc/ssh`, `/etc/sudoers.d`, `/etc/cron*`, `/etc/systemd`, and application binaries.

## Schedule
Run `aide --check` from a systemd timer or cron and send the output to the SIEM rather than local mail.

## Protect the baseline
An attacker with root can update the database. Copy the database and the binary/config to read-only media or a central server after each approved update, and verify its hash before checks (or run checks from a trusted boot environment for high assurance).

## After approved changes (patching)
`aide --update` checks and writes a new database non-interactively (input and output databases must differ). Review the change report, then move the new database to the `database_in` location; tie this to the change record.

## Gotchas
- Huge first reports after OS upgrades: update the baseline as part of the patch process.
- `aide --dry-init` (AIDE 0.17+) walks the file system and reports what the rules match without writing a database or report, which helps when testing new rules.

## Verify
- [ ] Modifying a test file in `/etc` shows up in the next `aide --check`.
- [ ] Off-host copy of the database exists with a recorded hash.

## Checked
Checked 2026-10-25 against the AIDE manual pages aide.conf(5) and aide(1) in the aide/aide repository (last commit 2026-10-18). Confirmed: rule syntax (regular expression anchored at the path start, `!` recursive negative rule), attribute names (p, i, n, u, g, s, m, c, acl, selinux, xattrs, sha512, ftype), built-in group names, `--init`, `--check`, `--update` (input and output databases must differ), `--dry-init`, and the `database_in` and `database_out` options. Removed unconfirmed distribution package, path, prelink and package-manager details.

Method: documentation only; no commands were run.
