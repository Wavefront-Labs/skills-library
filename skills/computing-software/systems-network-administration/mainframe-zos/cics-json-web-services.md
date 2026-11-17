---
id: computing-software.systems-network-administration.mainframe-zos.cics-json-web-services
name: cics-json-web-services
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cics-pipeline, zosconnect, json-assistant, cics-web-services, cics-json, liberty-jvm-server, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Exposing CICS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JSON and web services in CICS

Goal: expose programs as APIs.
- Use CICS pipelines/URIMAP resources, JSON assistants, or z/OS Connect (confirm current product naming).
- Map COMMAREA/channels to JSON.
- Secure with TLS and RACF identity propagation.
Verify: curl call returns program output.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
