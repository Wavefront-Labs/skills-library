---
id: computing-software.systems-network-administration.mainframe-zos.ebcdic-ascii-conversion
name: ebcdic-ascii-conversion
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ebcdic, iconv, code-page, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Data encoding"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EBCDIC and ASCII data conversion

Goal: avoid mojibake.
- `iconv -f IBM-1047 -t ISO8859-1`; FTP/SFTP text mode conversion; Zowe CLI uploads with encoding option.
- Binary fields (packed decimal COMP-3) must not be transferred in text mode.
- Know your code page (IBM-037 vs IBM-1047 differ in brackets).
Verify: round-trip a file with special characters.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
