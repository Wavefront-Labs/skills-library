---
id: computing-software.systems-network-administration.mainframe-zos.sms-and-storage-classes
name: sms-and-storage-classes
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, sms, storage-class, management-class, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "System-managed storage"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMS classes and storage management

Goal: use SMS constructs.
- Data class (allocation defaults), storage class (performance/availability), management class (migration/backup/retention), storage group (volumes).
- ACS routines assign classes; users can request via `STORCLAS=` etc. subject to authorisation.
- Display with ISMF.
Verify: new datasets get expected classes (`LISTCAT ENTRIES(x) ALL`).

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
