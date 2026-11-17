---
id: computing-software.digital-forensics-incident-response.incident-response-process.incident-case-platforms-thehive-and-iris
name: incident-case-platforms-thehive-and-iris
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [thehive, incident-ticketing, dfir-iris, case-management, case-tracking, dfir]
level: practitioner
status: draft
description: "Run incidents in a case platform (TheHive, DFIR-IRIS or a ticketing system): case templates, tasks, observables, evidence records, access control and exports."
sources: ["https://docs.strangebee.com/thehive/", "https://docs.dfir-iris.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident case platforms: TheHive and DFIR-IRIS

**Goal:** every incident lives in one system of record with tasks, observables, evidence,
timeline and notes, access-controlled and exportable for the report.

## What a case record needs
- Metadata: ID, title/codename, severity, classification, TLP/PAP, status, owner, dates.
- **Tasks** from a template per incident type (mirrors the playbook phases), assigned with due times.
- **Observables/IOCs**: IP, domain, hash, account, with tags (malicious/suspicious/benign),
  sighted flags and source.
- **Evidence register**: evidence ID, description, hash, custodian, storage location.
- **Timeline** of events, **notes**, attachments, and the decision log.

## TheHive (StrangeBee)
- Case templates define tasks and custom fields; alerts from SIEM/MISP are imported and
  merged into cases.
- Cortex analyzers enrich observables (VirusTotal, AbuseIPDB, MISP lookup) and responders
  can trigger actions; keep responders that change production behind human approval.
- MISP integration exports IOCs at closure for sharing.

## DFIR-IRIS
- Open source, built for DFIR: assets, IOCs, timeline (with graph), evidence register with
  hashes, notes, and module hooks (VT, MISP, webhooks).
- Timeline entries can be linked to assets and IOCs, which helps build the master timeline.

## Practice
- Restrict access per case; insider and HR cases need need-to-know.
- If the corporate IdP is compromised, the case platform must authenticate separately.
- Export the full case (JSON/PDF) at closure into the evidence store; platforms change, cases
  must stay readable for years.

## Verify
Close a test case and confirm the export alone lets someone reconstruct who did what and
when, without logging into the platform.
