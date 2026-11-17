---
id: computing-software.systems-network-administration.mainframe-zos.liberty-jvm-server
name: liberty-jvm-server
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, jvmserver, liberty-profile, java-in-cics, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Java workloads"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Liberty JVM server in CICS

Goal: run Java in CICS.
- JVM server resources (`JVMSERVER`) host OSGi or Liberty; use `JCICS` API.
- Memory (heap) set in the JVM profile.
- zIIP-eligible work offloads CP use.
Verify: JVM server ENABLED.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
