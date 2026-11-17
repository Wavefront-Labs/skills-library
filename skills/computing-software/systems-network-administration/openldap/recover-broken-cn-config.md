---
id: computing-software.systems-network-administration.openldap.recover-broken-cn-config
name: recover-broken-cn-config
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, recovery, broken-config, slapmodify, slapcat, slapadd, cn-config]
level: advanced
status: docs-checked
description: "Repair an OpenLDAP cn=config that stops slapd starting: export with slapcat, edit the LDIF, reimport with slapadd, or patch in place with slapmodify."
sources:
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# recover a broken cn=config
Options in order of preference (slapd stopped):

1. Export, edit, reimport:
```
slapcat -F /usr/local/etc/openldap/slapd.d -n0 -l extracted_config.ldif
slapadd -F /usr/local/etc/openldap/slapd.d -l updated_config.ldif
slaptest -F /usr/local/etc/openldap/slapd.d
```
Edit `extracted_config.ldif` between the first two commands, and load the result into an emptied slapd.d directory. `-n0` selects the config database.

2. Modify in place with `slapmodify -F /usr/local/etc/openldap/slapd.d`, feeding LDIF change records (`dn: ..., cn=config` plus `changetype:`).

3. Last resort: treat the config as a plain `back-ldif` database with schema checking disabled. The guide warns this may stop working in future releases.

Verify with `slaptest -F <dir>` (exit 0 means success) before starting slapd; `-Q` prints nothing and reports only through the exit code.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide 5.5 (slapcat -n0 export, slapadd reload after backing up and removing the old contents, slaptest check, slapmodify in place, plain back-ldif last resort with its future-release warning) and slaptest(8) (-Q and exit code). Removed the unsupported claim about checksums in slapd.d files.

Method: documentation only; no commands were run.

