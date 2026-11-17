---
id: computing-software.systems-network-administration.mainframe-zos.at-tls-policy
name: at-tls-policy
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, at-tls, policy-agent, pagent, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "TLS without code changes"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application Transparent TLS

Goal: encrypt traffic without app changes.
- Policy Agent rules (`TTLSRule`, `TTLSGroupAction`, `TTLSEnvironmentAction`) apply TLS to ports/jobs.
- Keyrings in RACF (`RACDCERT ADDRING`).
- Use sufficient cipher policy (modern TLS only).
Verify: handshake logged and clients confirm TLS.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
