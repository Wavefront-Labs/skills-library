---
id: computing-software.systems-network-administration.mainframe-zos.locking-and-isolation
name: locking-and-isolation
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, lock-escalation, isolation-levels, deadlock-timeout, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Concurrency"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locking and isolation

Goal: avoid contention.
- Isolation: RR, RS, CS, UR; lock sizes row/page/table; escalation via LOCKMAX.
- -911 (rollback, deadlock/timeout) and -913 require retry logic.
- `-DIS DB(...) LOCKS` and IFCID traces diagnose.
Verify: lock waits low in accounting reports.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
