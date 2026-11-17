---
id: media-communication.library-and-archive-science.records-management.retention-schedules-and-legal-holds
name: retention-schedules-and-legal-holds
category: media-communication
field: library-and-archive-science
product: records-management
tags: [records-management, rim, retention-schedule, records-retention, disposition, destruction, certificate-of-destruction, legal-hold, litigation-hold, e-discovery, records-policy, file-plan, big-bucket, records-inventory, vital-records, iso-15489, gdpr, storage-limitation, microsoft-purview, retention-labels, sharepoint, information-governance, archives-transfer]
level: practitioner
status: draft
description: "Govern an organisation's records: inventory, a big-bucket retention schedule with legal citations, defensible disposition, legal holds that suspend it, and policy plus system enforcement."
sources: ["https://www.iso.org/standard/62542.html", "https://www.archives.gov/records-mgmt", "https://learn.microsoft.com/en-us/purview/retention"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Retention schedules and legal holds

**Goal:** keep records exactly as long as law, regulation and business need require —
then dispose of them defensibly — while being able to freeze anything relevant the
moment litigation or an investigation is anticipated.

**Not legal advice:** retention periods are set by law and regulation that vary by
country, sector and record type. Always have legal/compliance sign off the schedule.

## 1. Inventory what you have
Survey each business unit: record series (e.g. "Supplier contracts", "Payroll",
"Customer complaints"), format and location (systems, shared drives, paper, email),
owner, volume, how long it's used actively, and who else relies on it. A **record
series** is a group of records with the same function and retention — the unit you
schedule, not individual documents.

## 2. Build the retention schedule
Each row:
`series | description | owner | trigger event | retention period | legal/regulatory citation | disposition (destroy / transfer to archives / review) | vital record? | system of record`
- **Trigger events** make periods meaningful: "contract end + 6 years", "employee
  termination + 7 years", "end of financial year + 7 years". Fixed periods from creation
  are rarely right.
- Cite the source (statute, regulation, limitation period, contract term) for each
  period; where none applies, record the business rationale.
- **Big buckets:** group series into fewer, broader categories with one period (e.g.
  ~20–60 buckets rather than 1,000 rows). Far easier for staff and systems to apply;
  take the longest requirement within the bucket.
- Privacy law (e.g. GDPR's storage-limitation principle) pushes the other way: personal
  data must *not* be kept longer than necessary. The schedule is your evidence of that.
- Approve formally (legal, compliance, records owner, executive) and version it.

## 3. Disposition that stands up
- Run disposition regularly (e.g. annually) — a schedule never executed is worse than
  none, because it shows awareness without compliance.
- Steps: system report of records past retention › **check legal holds** › owner review
  and sign-off › destroy securely (shredding to an appropriate standard, cryptographic
  erasure or verified deletion; destroy backups per their own cycle) › **certificate/log
  of destruction** (what series, date range, volume, method, approver). Never log
  destroyed content itself in a way that defeats the purpose.
- Records with archival value transfer to the archives instead (with metadata).

## 4. Legal holds (litigation holds)
When litigation, an investigation or an audit is **reasonably anticipated** (not only
when served), legal issues a hold:
1. Define scope: matters, custodians, date range, record types, systems.
2. Send hold notices to custodians and IT; require written acknowledgement.
3. **Suspend disposition** for in-scope records — including auto-delete rules, mailbox
   cleanups and backup rotation where relevant.
4. Re-remind custodians periodically; add new custodians as the matter evolves.
5. **Release** the hold formally when legal says so, then resume normal retention.
Destroying records under hold (spoliation) can bring court sanctions; the hold must
override everything.

## 5. Enforce in systems
- Map buckets to **retention labels/policies** in the systems where records live (e.g.
  Microsoft Purview retention labels for SharePoint/OneDrive/Exchange/Teams; Google
  Vault for Workspace; ECM/EDRMS rules). Use eDiscovery holds in the same tools.
- Prefer auto-applied labels by location or content type; manual labelling is
  inconsistent.
- Test: a dummy record with a short-retention test label disposes as expected; one
  under hold doesn't.

## 6. Policy and people
A short records policy: scope, roles, the schedule's authority, holds, disposal, and
penalties. Train staff on the few rules they must apply (where to save, what not to
keep in personal drives/chat).

## Gotchas
- Keeping "everything forever" — raises discovery cost, breach exposure and privacy risk.
- Email and chat are records too; unmanaged mailboxes defeat the schedule.
- Holds that never get released freeze disposition indefinitely; track them.

## Verify
- [ ] Every series is in the schedule with trigger, period, citation/rationale and owner.
- [ ] Legal/compliance sign-off and version date recorded.
- [ ] Last disposition run has certificates and owner approvals on file.
- [ ] Hold register lists active holds, custodians, acknowledgements; tested that holds block deletion.
- [ ] Retention labels/policies in systems match the schedule buckets.
