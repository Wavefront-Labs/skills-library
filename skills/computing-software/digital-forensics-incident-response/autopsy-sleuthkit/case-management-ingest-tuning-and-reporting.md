---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.case-management-ingest-tuning-and-reporting
name: case-management-ingest-tuning-and-reporting
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [autopsy, case-management, ingest-modules, keyword-search, regex-search, solr, tagging, multi-user-case, postgresql, report-generation, central-repository, hash-sets, nsrl, dfir-report, defensibility]
level: practitioner
status: draft
description: "Run an Autopsy case defensibly: tune ingest modules for the evidence type, build keyword/regex search lists, tag consistently, and generate a report a reviewer can retrace."
sources: ["https://sleuthkit.org/autopsy/docs/user-docs/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Autopsy case management, ingest tuning and reporting

**Goal:** run the case so the output holds up when someone else — opposing expert,
auditor, your own six-months-later self — retraces it, and so ingest doesn't either
silently skip something relevant or run for three days on modules you didn't need.

## 1. Case setup
- **Single-user vs multi-user case.** Multi-user requires PostgreSQL + Solr + ActiveMQ
  running and configured in Autopsy's multi-user settings; it buys concurrent
  examiner access to one case and is the only option once a case needs more than one
  investigator or exceeds what a laptop's local SQLite case file comfortably handles.
  Decide this before ingest starts — converting later means re-ingesting.
- Add the image/device as a **data source** with the correct host timezone; Autopsy
  derives displayed timestamps from this, and getting it wrong shifts every timeline
  entry in the UI by the offset, even though the underlying filesystem timestamps
  (always UTC/FILETIME on NTFS) are unaffected.

## 2. Ingest module tuning
Running every module on every case wastes hours and buries the signal:
- **Hash Lookup** against NSRL (known-good) and a known-bad/malware hash set first —
  this triages volume before anything else runs.
- **Keyword Search** is the one most worth tuning: default lists are generic. Build a
  case-specific list (names, domains, IOCs from the incident) and enable **regex**
  mode for patterns like credit card numbers, IPs, or custom malware strings — literal
  string search misses case variants and encoding differences (UTF-16LE text embedded
  in a binary needs a regex or a dedicated Unicode-aware search, not a plain ASCII hit).
- **Recent Activity**, **Embedded File Extraction**, **PhotoRec Carver** (runs the same
  carving as
  computing-software.digital-forensics-incident-response.autopsy-sleuthkit.file-carving-and-unallocated-space-recovery
  automatically on unallocated space — expensive, skip it on a quick triage pass and
  run it as a second, scoped ingest later if needed).
- Re-running ingest after adding a keyword list does **not** require re-ingesting
  modules that already ran; right-click the data source → "Run Ingest Modules" and
  select only Keyword Search to re-scan with the new list.

## 3. Tagging and review workflow
- Use **tags**, not bookmarks alone, for anything that will appear in the report —
  tags carry into the report generator with their comment field; bookmarks don't.
  Agree a tag taxonomy (`Relevant`, `Follow-up`, `Exculpatory`, `IOC`) before the team
  starts tagging so two examiners don't invent incompatible schemes mid-case.
- The **Central Repository** (if enabled) correlates a file/hash/account across every
  case in the repo — use it to catch "have we seen this exact malware sample before"
  across engagements, but be aware it persists across cases, so don't enable it on
  work bound by a case-specific NDA without checking that's allowed.

## 4. Reporting
- Autopsy's built-in report generator (HTML, Excel, "Autopsy Report", Body File,
  KML, etc.) works from tagged items, not everything ingest found — if something
  relevant wasn't tagged it won't appear, a common cause of a report missing a finding
  the examiner remembers seeing in the UI.
- The generated report lists the module versions and ingest settings used — keep this
  page; it's what lets another examiner (or a court) confirm what ran and how,
  satisfying the same reproducibility need as hashing the source evidence (see
  computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody).

## Verify
- Before closing a case, confirm every module you intended to run shows "Completed" in
  the ingest inbox (not "Completed with errors" silently ignored).
- Spot-check that every tagged item appears in the generated report before delivering it.
- Record the ingest module settings/version alongside the report output, not just the
  report itself.

Unconfirmed: multi-user case setup specifics (exact PostgreSQL/Solr version pinning)
vary by Autopsy release — check the release notes for the version in use before
standing up shared infrastructure.
