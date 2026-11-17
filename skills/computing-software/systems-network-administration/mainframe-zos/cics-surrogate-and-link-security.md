---
id: computing-software.systems-network-administration.mainframe-zos.cics-surrogate-and-link-security
name: cics-surrogate-and-link-security
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, link-security, surrogate-user, cics-userid, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Cross-region identity"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Link security and surrogate users

Goal: control identities across regions.
- Link security with `SECURITYNAME` on CONNECTION and `SURROGAT` profiles to allow region userids to act as users.
- Default user for unauthenticated work must be least-privilege.
- Audit via SMF 80.
Verify: remote transactions run under the intended user.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
