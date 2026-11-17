---
id: computing-software.systems-network-administration.mainframe-zos.ftp-to-zos
name: ftp-to-zos
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ftp-site-commands, jes-ftp, quote-site, zos-ftp, sftp-zos, scp-zos, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Transfers"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FTP to z/OS

Goal: transfer datasets reliably.
- `site lrecl=80 recfm=fb`, `type a|e|i`, `quote site filetype=jes` to submit jobs.
- Prefer SFTP/SSH or Zowe; enable TLS on FTP.
- Never transfer binary data in text mode.
Verify: dataset attributes preserved.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
