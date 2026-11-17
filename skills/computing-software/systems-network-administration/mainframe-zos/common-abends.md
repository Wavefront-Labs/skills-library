---
id: computing-software.systems-network-administration.mainframe-zos.common-abends
name: common-abends
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, sb37, s0c7, s806, abend, s0c4, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Decoding failures"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Common abend codes

Goal: resolve frequent abends.
- S0C7 data exception (bad packed decimal); S0C4 protection exception (bad address); SB37/SD37/SE37 out of space; S806 program not found; S222 cancelled; U4038 etc. Language Environment.
- Read the PSW and the offset from the listing; use compiler LIST/OFFSET options.
- For B37, increase SPACE or add volumes/extents.
Verify: rerun completes with RC=0.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
