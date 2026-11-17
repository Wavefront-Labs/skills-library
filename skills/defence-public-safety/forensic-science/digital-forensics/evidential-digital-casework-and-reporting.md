---
id: defence-public-safety.forensic-science.digital-forensics.evidential-digital-casework-and-reporting
name: evidential-digital-casework-and-reporting
category: defence-public-safety
field: forensic-science
product: digital-forensics
tags: [digital-forensics, criminal-casework, digital-evidence, forensic-imaging, write-blocker, hash-verification, sha-256, chain-of-custody, continuity, acpo-principles, mobile-device-extraction, logical-extraction, full-file-system, cellebrite, xry, axiom, graykey, faraday-bag, airplane-mode, legal-authority, search-warrant, scope-of-examination, keyword-search, timeline, tool-validation, dual-tool-verification, evidential-report, streamlined-forensic-report, expert-witness, disclosure, iso-17025, fsr-codes, swgde]
level: practitioner
status: draft
description: "Digital evidence for a criminal case: work within legal authority, seize and isolate devices, image with verification, examine to the brief, validate tool output and write a court-ready report."
sources: ["ACPO Good Practice Guide for Digital Evidence (UK, v5) principles", "SWGDE best practices (computer forensics, mobile device acquisition)", "UK Forensic Science Regulator Codes — digital forensics appendices", "ISO/IEC 27037 identification, collection, acquisition and preservation of digital evidence"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Evidential digital casework and reporting

**Goal:** produce digital evidence a court will accept: lawfully obtained, unaltered
or with every alteration explained, examined against a clear brief, with findings
verified and reported so a non-specialist can follow them. For the technical acquisition
detail see `computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody`;
this skill covers what is different in criminal casework.

## 1. Authority and scope first
- Identify the **legal power** for seizure and examination (warrant, consent, statutory
  power) and what it covers — devices, data types, date range. Examining outside scope
  can make the evidence inadmissible. Cloud data reached from a device may need separate
  authority (jurisdiction-dependent — confirm with legal advisers).
- Get a written **examination brief** from the investigator: offences, relevant people,
  time window, specific questions. "Get everything" invites privacy challenges and
  unmanageable disclosure.
- Note legally privileged material risk (e.g. a lawyer's communications) and agree a
  filtering procedure before review.

## 2. Seizure and preservation
- The four ACPO principles still frame UK practice: don't change data; if you must
  access original data, be competent and explain; keep an audit trail; the person in
  charge is responsible for compliance.
- **Mobile devices:** isolate from networks (Faraday bag/box or airplane mode as policy
  directs) to stop remote wipe and new data arriving; keep powered if a powered-on state
  matters for extraction (full-disk encrypted phones are far harder after reboot — the
  "before first unlock" state). Record screen state with photographs.
- **Computers:** photograph, decide live capture (RAM, open sessions, encrypted volumes)
  vs power-off based on a documented triage, then image with a write-blocker.
- Exhibit every device with continuity labels like any physical exhibit.

## 3. Acquisition and verification
- Image to forensic formats (E01/AFF4/raw) and **hash** (SHA-256; MD5 also for legacy
  compatibility) at acquisition and verification.
- Mobile extraction levels: logical → file-system → full file system / physical. Record
  tool, version, method and any exploit/agent installed — these change the device, and
  that must be disclosed and justified.
- Work on verified copies only.

## 4. Examination
- Answer the brief: targeted keyword, date and artefact searches; build timelines of
  user activity; attribute activity to a **person**, not just an account or device
  (look for corroboration — logins, locations, content only that person would write).
- **Validate** significant findings: confirm with a second tool, or manually at the
  database/file level (e.g. parse the SQLite message table yourself). Parsers misreport
  timestamps (time zones, epoch formats) and deleted-record recovery.
- Record negative findings and limitations (encrypted containers not opened, apps not
  supported by the tool).

## 5. Reporting and disclosure
- Reports separate **facts** (artefact X found at path Y, timestamp Z UTC) from
  **opinion** (interpretation of what the user did). Expert opinion requires the expert
  declaration your jurisdiction mandates.
- Explain artefacts in plain language; include the extraction method, tools/versions,
  hash values and validation steps. Many jurisdictions accept staged reports (e.g. UK
  streamlined forensic reports) with full reports on request.
- Provide material for **disclosure**: the defence may get the image or an extraction
  report; unused material may contain exculpatory data — flag it.

## Gotchas
- Tool reports are not evidence of correctness. Accreditation (ISO/IEC 17025) requires
  validated methods; an unvalidated new parser output needs manual confirmation.
- Time zones: store and report in UTC with local time noted.
- "Deleted" chat recovered by a tool may be a fragment of a different thread — verify
  context before reporting.
- Volume: triage kiosks are for screening; findings from them need full lab verification.

## Verify
- [ ] Legal authority and brief recorded; examination stayed within scope.
- [ ] Acquisition and verification hashes match; tools and versions logged.
- [ ] Key findings validated by a second tool or manual parsing.
- [ ] Attribution to a person argued, not assumed.
- [ ] Report separates fact from opinion and lists limitations; disclosure considered.
