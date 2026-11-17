---
id: computing-software.systems-network-administration.mainframe-zos.grants-and-privileges
name: grants-and-privileges
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, grant-execute, secadm, db2-privileges, db2-grant, db2-authid, db2-roles, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Privilege model"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GRANT, REVOKE and authorisation

Goal: control access.
- `GRANT SELECT ON T TO USR1`, `GRANT EXECUTE ON PACKAGE COLL.PGM1 TO PUBLIC`, roles and trusted contexts.
- Use separation of duties (SECADM, DBADM, install SYSADM changes in recent versions - confirm).
- Audit with the Db2 audit trace.
Verify: `SYSIBM.SYSTABAUTH` shows intended grants.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
