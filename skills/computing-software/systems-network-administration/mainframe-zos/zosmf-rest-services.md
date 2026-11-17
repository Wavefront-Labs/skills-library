---
id: computing-software.systems-network-administration.mainframe-zos.zosmf-rest-services
name: zosmf-rest-services
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, zosmf, rest-jobs-api, workflows, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Web interface and REST"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# z/OSMF REST

Goal: use z/OSMF.
- REST: `/zosmf/restjobs/jobs`, `/zosmf/restfiles/ds`; requires `X-CSRF-ZOSMF-HEADER`.
- Workflows automate repeated admin tasks.
- Secure with RACF groups and TLS (AT-TLS).
Verify: a REST call lists your jobs.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
