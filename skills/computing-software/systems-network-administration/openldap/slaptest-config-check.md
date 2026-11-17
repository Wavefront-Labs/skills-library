---
id: computing-software.systems-network-administration.openldap.slaptest-config-check
name: slaptest-config-check
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slaptest, config-check, validate-config, cn-config, slapd-conf]
level: practitioner
status: docs-checked
description: "Validate an OpenLDAP configuration before restart with slaptest: -f, -F, -n, -Q, -u, -v options, exit codes, and conversion behaviour."
sources:
  - https://www.openldap.org/software/man.cgi?query=slaptest&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slaptest config check
```
slaptest -f /usr/local/etc/openldap/slapd.conf -v
slaptest -F /usr/local/etc/openldap/slapd.d
slaptest -F /usr/local/etc/openldap/slapd.d -Q; echo $?
```
Options:
- `-f slapd.conf`, `-F confdir`: with both, converts the file to directory format.
- `-n dbnum`: test only the nth database; `-n 0` is the config database (always first).
- `-Q`: quiet; only the exit code reports (0 success, anything else failure).
- `-u`: dry run; do not fail if databases cannot be opened, as long as the config is valid. Without it, an unopenable database causes failure even if the config is fine.
- `-v` verbose; `-d level` debug; `-o syslog=...`.

Gotchas:
- With no `-f`/`-F`, the default config directory is tried first, and a valid one makes the default slapd.conf ignored. Name the path explicitly.
- Conversion can fail on a fresh config when backends have not been created yet; use slapcat to convert instead.
- Dry-run mode blocks conversion.

Use it as a gate in change scripts: validate, then restart slapd only when the exit code is 0.

## Checked
2026-11-08: confirmed against the slaptest(8) man page: every option, the -F default-directory and conversion behaviour, the fresh-config conversion caveat, and the -Q exit code meaning.
Method: documentation only; no commands were run.
