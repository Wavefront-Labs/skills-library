---
id: computing-software.systems-network-administration.openldap.overlay-auditlog
name: overlay-auditlog
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, auditlog, olcauditlogfile, change-log, overlay, ldif-audit]
level: practitioner
status: docs-checked
description: "Write an LDIF audit trail of OpenLDAP changes with the auditlog overlay: auditlog and olcAuditlogFile, record header fields and caveats."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-auditlog&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# auditlog overlay
slapd.conf:
```
overlay auditlog
auditlog /var/log/ldap/auditlog.ldif
```
cn=config:
```
dn: olcOverlay=auditlog,olcDatabase={1}mdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcAuditLogConfig
olcOverlay: auditlog
olcAuditlogFile: /var/log/ldap/auditlog.ldif
```
Adjust `{1}mdb` to suit your database; the file name must be a fully qualified path.

Output is LDIF per operation. Header: `# modify <timestamp> <suffix> <modifiersName> IP=<ip:port> conn=<number>`, then the change (including `modifiersName` and `entryCSN`), then `# end modify <timestamp>`. Fields: operation, epoch seconds, suffix, modifiersName, client address, connection number (-1 means an internal operation).

Gotchas:
- `auditlog` goes after the `overlay` line in slapd.conf; use `olcAuditlogFile` in cn=config.
- For Add and Modify the identity comes from `modifiersName`, which other overlays may alter, so it is not always the requester.
- It records changes on the one backend database it is attached to.
- The man page and guide examples log to a `/tmp` file "for testing"; choose a real path and make sure slapd can write it.

## Checked
2026-11-08: confirmed against the slapo-auditlog(5) man page (directives, six comment fields, conn -1, modifiersName note, cn=config example, example changelog) and the Admin Guide overlays chapter section 12.2 (read that section only, not the whole chapter). Removed the unconfirmed ldapmodify command line.
Method: documentation only; no commands were run.
