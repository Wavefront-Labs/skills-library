---
id: computing-software.systems-network-administration.mainframe-zos.copy-recover-quiesce
name: copy-recover-quiesce
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, image-copy, recover-utility, point-in-time-recovery, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Backup and recovery"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# COPY, RECOVER, QUIESCE

Goal: protect data.
- `COPY TABLESPACE ... FULL YES`, `QUIESCE`, `RECOVER TABLESPACE ... TOLOGPOINT x`.
- Take copies after LOAD and REORG; use MODIFY RECOVERY to prune.
- Test recovery routinely.
Verify: recovered object matches a pre-test checksum.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
