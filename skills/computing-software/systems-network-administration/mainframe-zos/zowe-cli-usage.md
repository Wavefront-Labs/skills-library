---
id: computing-software.systems-network-administration.mainframe-zos.zowe-cli-usage
name: zowe-cli-usage
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, zowe-cli-profiles, zowe-jobs, zowe-files, zowe, zowe-cli, z-open-editor, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Scripting z/OS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zowe CLI

Goal: drive z/OS from a workstation.
- `zowe zosmf check status`, `zowe files list ds "HLQ.*"`, `zowe jobs submit lf job.jcl --wfo` (confirm flags).
- Profiles hold host and credentials (use secure credential store).
- Requires z/OSMF REST services.
Verify: submit a job and fetch spool output.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
