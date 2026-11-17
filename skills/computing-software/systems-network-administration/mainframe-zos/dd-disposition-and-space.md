---
id: computing-software.systems-network-administration.mainframe-zos.dd-disposition-and-space
name: dd-disposition-and-space
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, disp, space-allocation, dcb, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Dataset allocation in JCL"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DISP, SPACE and DCB parameters

Goal: allocate and manage datasets in JCL.
- `DISP=(NEW,CATLG,DELETE)` new/normal/abnormal; `SHR`, `OLD`, `MOD`.
- `SPACE=(CYL,(10,5),RLSE)` primary/secondary; `RECFM=FB,LRECL=80`; `UNIT=SYSDA`.
- Referback: `DCB=*.step.dd`, `DSN=*.step.dd`.
Verify: the dataset is cataloged with intended attributes after the job.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
