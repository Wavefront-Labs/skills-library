---
id: computing-software.systems-network-administration.mainframe-zos.setropts-and-password-rules
name: setropts-and-password-rules
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, setropts-list, password-rules, revoke-interval, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "System-wide options"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SETROPTS and password policy

Goal: enforce policy.
- `SETROPTS PASSWORD(INTERVAL(90) HISTORY(10) RULE1(LENGTH(8:8) LEGAL(ALPHANUM)))`, `REVOKE(5)`, `INACTIVE(90)`.
- `SETROPTS LIST` shows current options.
- Consider MFA (IBM MFA) and passphrases (confirm product availability).
Verify: `SETROPTS LIST` matches policy.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
