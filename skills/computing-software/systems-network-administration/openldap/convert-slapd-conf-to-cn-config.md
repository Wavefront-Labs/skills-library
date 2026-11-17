---
id: computing-software.systems-network-administration.openldap.convert-slapd-conf-to-cn-config
name: convert-slapd-conf-to-cn-config
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, conversion, slapd-d, migrate-config, slaptest, cn-config]
level: practitioner
status: docs-checked
description: "Convert an OpenLDAP slapd.conf to a slapd.d cn=config directory with slaptest, add a config-database rootpw, and verify access."
sources:
  - https://www.openldap.org/doc/admin26/slapdconf2.html
  - https://www.openldap.org/software/man.cgi?query=slaptest&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# convert slapd.conf to cn=config
slapd.conf is deprecated.

1. Add a config database to the existing slapd.conf:
```
database config
rootpw VerySecret
```
2. Convert:
`slaptest -f /usr/local/etc/openldap/slapd.conf -F /usr/local/etc/openldap/slapd.d`
3. Verify:
`ldapsearch -x -D cn=config -w VerySecret -b cn=config`
4. Start slapd with `-F /usr/local/etc/openldap/slapd.d` if that is not the default directory.

Notes:
- Included files are merged into the converted configuration.
- With both `-f` and `-F`, slaptest converts and writes the directory. Dry-run (`-u`) prevents conversion.
- Conversion can fail on a fresh config if the configured backends have not been created yet; use slapcat to convert instead.
- With neither `-f` nor `-F`, the default config directory is tried first, and a valid one makes the default slapd.conf ignored.
- Replace plain `rootpw` with SASL where possible, since the config backend can load arbitrary code.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide 5.4 (database config and rootpw, the slaptest command, the ldapsearch check, -F on launch, included files merged, arbitrary code warning) and slaptest(8) (-f with -F converts, -u dry run, conversion may fail on a fresh config and slapcat is the fallback, default directory tried first). Reduced the deprecation line to what slapdconf2 states.

Method: documentation only; no commands were run.

