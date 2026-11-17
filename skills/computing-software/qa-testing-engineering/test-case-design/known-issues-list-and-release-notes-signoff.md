---
id: computing-software.qa-testing-engineering.test-case-design.known-issues-list-and-release-notes-signoff
name: known-issues-list-and-release-notes-signoff
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [known-issues-list, release-notes, release-signoff, exit-criteria, defect-management]
level: practitioner
status: draft
description: "Prepare the known issues list and release notes for sign-off: which open defects to disclose, workarounds, customer impact wording and approval records."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Known issues list and release notes sign-off

**Goal:** open defects shipping with the release are visible, explained and accepted by the right people, and customers or support get workable guidance.

## Build the known issues list
1. Query open defects affecting the release version (Jira: `project = APP AND type = Bug AND status not in (Done, Closed) AND affectedVersion = "2.4"`).
2. Exclude those not reachable in this release (feature-flagged off) with a note.
3. Per item record: ID, title in user language, affected feature/platforms, severity, customer impact, workaround, target fix version, decision owner.
4. Separate internal-only issues from those disclosed externally.

## Wording for release notes
- Describe the symptom, not the code cause: "Exporting more than 10,000 rows to Excel can time out. Workaround: filter by date range and export in parts."
- Give scope (which browsers or plans) and the workaround; avoid promising dates unless committed.
- Security issues: coordinate disclosure with the security team; never describe exploit details before a fix.

## Sign-off
- Review with product owner, support lead and QA lead; product owner accepts each disclosed issue (risk acceptance).
- Record approval (ticket comment, release record or approval in the change management tool) with date and names.
- Support gets the list before release so they can recognise tickets.

## Verify
Every open defect affecting the release version appears on the list or has a documented exclusion reason, and approval is recorded before deployment.
