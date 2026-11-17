---
id: computing-software.systems-network-administration.mainframe-zos.uss-shell-and-zfs
name: uss-shell-and-zfs
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, oshell, zfs-filesystem, omvs, uss, zfs, bpxbatch, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Using USS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# z/OS UNIX shell and zFS file systems

Goal: work in the USS environment.
- Enter via `OMVS` or ssh; `ls -T` shows file tags; `chtag -tc ISO8859-1 file` sets encoding.
- zFS aggregates are mounted with `MOUNT FILESYSTEM('HLQ.ZFS') MOUNTPOINT('/u/x') TYPE(ZFS)`.
- Run from JCL with `BPXBATCH`.
Verify: file tags and text encoding match (ASCII vs EBCDIC).

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
