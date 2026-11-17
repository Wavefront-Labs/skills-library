---
id: computing-software.digital-forensics-incident-response.incident-response-process.ir-retainers-and-third-party-coordination
name: ir-retainers-and-third-party-coordination
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ir-retainer, third-party-ir, mssp, outside-counsel, dfir]
level: practitioner
status: draft
description: "Set up and run IR retainers and third-party responders (DFIR firm, MSSP, insurer panel, cloud support) so they start work within hours, under privilege."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/resources-tools/resources/incident-response-plan-irp-basics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IR retainers and third-party coordination

**Goal:** when you need outside responders, the contract, access and legal structure already
exist, so day one is spent investigating rather than negotiating.

## Before the incident
1. **Read the cyber insurance policy first.** Most require panel vendors (breach coach
   counsel, DFIR firm, negotiator) and pre-approval of costs. An off-panel firm can void
   reimbursement.
2. **Retainer contract** with a DFIR firm: pre-signed MSA and SOW, response SLA (remote
   within 2 h, onsite within 24 h), named contacts, an hours bank convertible to proactive
   work (tabletops, compromise assessments) if unused.
3. **Engage under counsel.** Outside counsel engages the DFIR firm (three-way agreement).
   Privilege over the forensic report is fragile: in Capital One (2020) and Clark Hill (2021)
   reports prepared for business purposes and widely shared were ordered produced. Keep a
   separate, non-privileged remediation summary for wide circulation.
4. **Pre-provision access**: EDR console accounts, a deployable collector (Velociraptor or
   KAPE package), VPN accounts kept disabled until needed, an approved data transfer method.
5. **MSSP/MDR contract**: what they may do without asking (isolate host, disable account),
   escalation path, log retention they hold, how you get raw telemetry out.

## During the incident
- One point of contact on each side; daily written status.
- Scope in writing: questions to answer (initial access, dwell time, data accessed), systems
  in scope, deliverables (privileged report, IOCs, remediation plan).
- Record evidence handed over in your chain-of-custody log and obtain the firm's records.
- Cloud providers: open a high-severity support case early; AWS, Microsoft and Google act
  only on the account owner's request.

## Gotchas
- Two firms (insurer's and yours) collecting from the same hosts: coordinate or you corrupt
  evidence and pay twice.
- Retainer hours expire; schedule proactive use mid-term.
- Do not hand third parties domain admin; give scoped accounts and log their use.

## Verify
Once a year call the retainer hotline as a drill and time how long until a qualified
responder is on the phone.
