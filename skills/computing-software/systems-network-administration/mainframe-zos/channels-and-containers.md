---
id: computing-software.systems-network-administration.mainframe-zos.channels-and-containers
name: channels-and-containers
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, channel-container, put-container, get-container, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Passing large data"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Channels and containers

Goal: pass data without the 32K COMMAREA limit.
- `EXEC CICS PUT CONTAINER('X') CHANNEL('CH') FROM(...)`, `GET CONTAINER`, `LINK PROGRAM('P') CHANNEL('CH')`.
- Containers can be CHAR or BIT; code pages convert as CHAR.
- Prefer channels for new designs; JSON/XML payloads fit naturally.
Verify: called program receives the container intact.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
