---
id: computing-software.systems-network-administration.mainframe-zos.ipcs-dump-reading
name: ipcs-dump-reading
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ipcs, dump-dataset, stack-trace, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Dump analysis"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading dumps with IPCS

Goal: analyse a dump.
- Allocate the dump DSN in IPCS (option 0 defaults), then `STATUS FAILDATA`, `SUMMARY FORMAT`, `LIST` storage, `VERBX LEDATA`.
- Language Environment dumps (`CEEDUMP`) show traceback with offsets.
- Match offsets to the compile listing.
Verify: identified failing statement.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
