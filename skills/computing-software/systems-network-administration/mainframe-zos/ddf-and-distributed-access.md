---
id: computing-software.systems-network-administration.mainframe-zos.ddf-and-distributed-access
name: ddf-and-distributed-access
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ddf, db2-connect, jdbc-db2, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Remote access"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DDF and distributed access

Goal: configure remote clients.
- DDF listens on SQL port (e.g., 446); location names, TCP/IP ports in BSDS (`DSNJU003`).
- JDBC/ODBC clients use data server drivers; use WLM sysplex routing.
- Secure with RACF and TLS.
Verify: a remote client query succeeds.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
