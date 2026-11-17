---
id: computing-software.systems-network-administration.linux.lynis-security-audit
name: lynis-security-audit
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lynis, security-audit, hardening-index, system-audit, custom-profile, cisofy, compliance, hardening, security, sysadmin]
level: practitioner
status: docs-checked
description: "Audit a Linux host with Lynis: running audit system, reading warnings and suggestions, the hardening index, skipping tests with a custom profile, and scheduling scans with report diffing."
sources:
  - https://github.com/CISOfy/lynis
  - https://github.com/CISOfy/lynis/blob/master/lynis.8
  - https://github.com/CISOfy/lynis/blob/master/default.prf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lynis security audit

**Goal:** a fast, agentless hardening review of any Linux/Unix host that produces a
prioritised to-do list and a score you can track over time.

## 1. Install and run
```bash
apt install lynis          # or dnf install lynis, or run it from a git checkout of CISOfy/lynis
lynis audit system                     # full audit, interactive pauses
lynis audit system --quick --quiet     # --quick: no pauses; --quiet: no screen output (also enables quick mode)
lynis show version; lynis update info
```
Root is not required, but the man page says it provides more details; a non-root run writes `lynis.log` and `lynis-report.dat` into the user's home directory instead of `/var/log`.

## 2. Read the output
- Console sections per area (boot, kernel, auth, file systems, networking, SSH, logging…) with `[OK]`, `[WARNING]`, `[SUGGESTION]`.
- End summary: **Hardening index** and number of tests performed.
- Files:
  - `/var/log/lynis.log` — the detailed log (`--logfile` changes the location).
  - `/var/log/lynis-report.dat` — machine-readable `key=value` (`warning[]=TEST|message|details|solution|`, `suggestion[]=`, `hardening_index=`).
```bash
grep -E '^(warning|suggestion)\[\]' /var/log/lynis-report.dat | cut -d'|' -f1,2
lynis show details SSH-7408           # explanation for one test ID
```
Treat warnings first; suggestions are often defence-in-depth, not vulnerabilities.

## 3. Custom profile (skip or tune tests)
```
# /etc/lynis/custom.prf
skip-test=FILE-6310          # "Checking /tmp, /home and /var directory" — handled by local policy
skip-test=SSH-7408:permitrootlogin   # skip one option within a test only (lowercase option name)
machine-role=server          # personal, workstation or server
```
Do not edit `default.prf`: its header says to put your changes in `custom.prf` in the same directory (`lynis show profiles` shows where profiles are). Record why each test is skipped.

## 4. Schedule and compare
```bash
# systemd timer or cron, weekly:
lynis audit system --cronjob > /dev/null      # --cronjob: cron-safe options (no colours, no questions, no breaks)
cp /var/log/lynis-report.dat /var/lib/lynis-reports/$(date +%F).dat
diff <(grep -E '^warning' last.dat) <(grep -E '^warning' new.dat)   # new warnings since last run
```
Ship `hardening_index` to monitoring to catch drift.

## Gotchas
- The hardening index is relative, not a compliance score — don't map it to CIS/STIG percentages.
- Lynis checks, it doesn't fix; pair findings with Ansible remediation.

## Verify
- [ ] `lynis-report.dat` exists with today's timestamp; all `warning[]` entries are fixed or have an owner and ticket.
- [ ] The hardening index after remediation is higher than the baseline and stays stable in scheduled runs.

## Checked

Checked 2026-10-26 against CISOfy/lynis master (last commit 2026-09-16): lynis.8, default.prf, the lynis script, include/report and db/tests.db. Confirmed: --quick, --quiet and --cronjob semantics, --logfile, log and report paths and the non-root home-directory fallback, report line format (warning[]=TEST|message|details|solution|), hardening_index key, show details TEST-ID, show version, update info, show profiles, skip-test syntax with lowercase option names, machine-role values, custom.prf guidance. Corrected: --cronjob is no colours, no questions and no breaks (not quiet); root is not required; FILE-6310 checks /tmp, /home and /var directories. Removed: the distro package lag claim, the 0-100 range and the package-vulnerability metadata claim.

Method: documentation only; no commands were run.
