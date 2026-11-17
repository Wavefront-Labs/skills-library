---
id: computing-software.systems-network-administration.mainframe-zos.hsm-migration-and-recall
name: hsm-migration-and-recall
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, hsm, hmigrate, hrecall, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Space management"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DFSMShsm migration and recall

Goal: manage space automatically.
- HSM migrates inactive datasets (ML1/ML2) per management class; `HRECALL 'DSN'` recalls; `HLIST` lists; `HBACKDS` backs up.
- Recall delays affect batch; tune migration age.
- Primary space management runs daily.
Verify: recall brings back the dataset intact.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
