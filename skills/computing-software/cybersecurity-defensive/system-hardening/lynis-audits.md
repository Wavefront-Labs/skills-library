---
id: computing-software.cybersecurity-defensive.system-hardening.lynis-audits
name: lynis-audits
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [lynis, security-audit, linux-hardening, hardening-index, cisofy, compliance-scanning]
level: practitioner
status: docs-checked
description: "Audit Linux and macOS hosts with Lynis: running system audits, reading warnings, suggestions and hardening index, custom profiles, skipping tests and tracking over time."
sources: ["https://github.com/CISOfy/lynis", "https://github.com/CISOfy/lynis/blob/master/default.prf", "https://github.com/CISOfy/lynis/blob/master/include/helper_show", "https://github.com/CISOfy/lynis/blob/master/include/tests_ssh", "https://github.com/CISOfy/lynis/blob/master/include/tests_kernel_hardening"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lynis audits

Lynis (CISOfy, GPLv3) is an agentless shell-script auditor for Linux, macOS and BSD. It runs hundreds of tests
(boot, kernel, authentication, file systems, SSH, firewall, logging, malware tools, PHP/web servers) and
outputs warnings, suggestions and a **hardening index**.

## Run
```bash
git clone https://github.com/CISOfy/lynis && cd lynis
sudo ./lynis audit system
sudo ./lynis audit system --quick                        # do not pause between sections (-Q)
sudo ./lynis show details SSH-7408                       # print that test's section from the log of the last scan
```
Outputs: `/var/log/lynis.log` (detailed) and `/var/log/lynis-report.dat` (machine-readable key=value) when run as root; non-root runs write them under the user's home directory. `--quiet` (`-q`) suppresses screen output.

## Reading results
- **Warnings**: likely security problems, fix first (e.g. `FIRE-4512` checks iptables for an empty ruleset, `AUTH-9216` checks the group and shadow group files).
- **Suggestions**: hardening opportunities with test IDs (e.g. `SSH-7408` checks SSH-specific options, `KRNL-6000` checks sysctl key pairs in the scan profile, `BOOT-5122` checks for a GRUB boot password, `ACCT-9628` checks for auditd).
- **Hardening index**: rough progress indicator; do not treat as compliance score.
- Report data keys like `warning[]=`, `suggestion[]=`, `hardening_index=` can be parsed for fleet reporting.

## Profiles and tuning
Custom profile (`custom.prf` next to `default.prf`, or `--profile`):
```
skip-test=PKGS-7392       # skip a test; record the reason in a comment
skip-test=SSH-7408:loglevel   # a test can also be skipped for a single sub-check
machine-role=server
```
Skip tests that do not apply to the role rather than ignoring them in reports.

## Fleet use
- Run via configuration management or cron, ship `lynis-report.dat` to a central place, track hardening index
  and warning count over time per host group.

## Lynis vs benchmark scanners
Lynis runs its own hygiene checks (see the test registrations in `include/tests_*`). For formal benchmark compliance use a
benchmark-specific scanner such as OpenSCAP (see scap-security-guide-tailoring); use Lynis for quick audits.

## Gotchas
- Run as root for complete results; tests registered as root-only (for example FIRE-4512) are skipped when not privileged.
- Use a current upstream release so the test set is up to date (check `lynis show version` against the repository).

## Verify
Report shows zero warnings on a hardened golden image, and fleet hardening index trend is reported monthly.

## Checked
Checked 2026-10-25 against the Lynis source repository (CISOfy/lynis, last commit 2026-09-16): `lynis` main script (default log and report locations, `--quiet`), `include/helper_show` (`show details TEST-ID`, `--quick (-Q)`), `default.prf` (`skip-test=`, `machine-role=`, custom.prf next to default.prf), `include/report` (`hardening_index=`), `include/functions` (`warning[]=` and `suggestion[]=` keys), and the test registrations for FIRE-4512, AUTH-9216, SSH-7408, KRNL-6000, BOOT-5122, ACCT-9628 and PKGS-7392. GPL v3 licence confirmed in the README. Removed the unconfirmed `config:test_skip_always` profile line (and the AUTH-9328 skip example), the Lynis Enterprise remark and the distribution-package age claim. The CISOfy control-description site was not read.

Method: documentation only; no commands were run.
