---
id: computing-software.systems-network-administration.mainframe-zos.irrdbu00-and-reports
name: irrdbu00-and-reports
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, irrdbu00, racf-database-unload, dbu-reports, racf-audit, racf-sef, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Reviewing access"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IRRDBU00 database unload and reports

Goal: audit the database.
- Run `IRRDBU00` to unload RACF to a flat file; load to Db2/analytics for queries.
- Look for UID 0, special/operations users, universal-access gaps, inactive IDs.
- SMF type 80 records show access events; `RACFRW` and `ICETOOL` build reports.
Verify: reports reconcile with `LISTUSER` samples.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
