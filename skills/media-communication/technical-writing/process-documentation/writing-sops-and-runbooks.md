---
id: media-communication.technical-writing.process-documentation.writing-sops-and-runbooks
name: writing-sops-and-runbooks
category: media-communication
field: technical-writing
product: process-documentation
tags: [process-documentation, sop, standard-operating-procedure, runbook, playbook, work-instruction, procedure-writing, decision-points, document-control, revision-history, review-cycle, iso-9001, gmp, compliance, controlled-documents, checklists, swimlane, raci, approval, step-accuracy, walkthrough-testing, operations]
level: practitioner
status: draft
description: "Write SOPs, runbooks and work instructions that work under pressure: purpose/scope/roles header, testable numbered steps, explicit decision points, document control and scheduled reviews."
sources: ["https://www.iso.org/iso-9001-quality-management.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing SOPs and runbooks

**Goal:** procedures someone can follow correctly on a bad day — tired, new, mid-
incident — that hold up in an audit and stay current. SOP = how an organisation does
a recurring process; runbook = how to operate or recover a system; work instruction =
the detailed how for one task inside an SOP.

## 1. Before writing: capture the real process
- **Watch it being done** (or do it) and write down what actually happens, not what the
  old document or the manager says happens. Note workarounds — they're often the truth.
- Interview the person who does it most, and the newest person (they know where it's
  confusing).
- Confirm scope: where it starts (trigger), where it ends (output), and what's
  deliberately out of scope.

## 2. Standard header (every procedure)
```
Title:            <verb + object>  e.g. "Restore the orders database from backup"
ID / version:     SOP-OPS-014 v3        Effective: <date>     Next review: <date>
Owner:            <role, not a person's name>
Purpose:          one sentence — why this exists
Scope:            applies to / does not apply to
Roles:            who does which steps (RACI if several roles)
Prerequisites:    access, tools, training, materials
Safety/risk notes: what can go wrong, irreversible steps
Related:          linked SOPs, forms, systems
```

## 3. Writing the steps
- Numbered, **one action per step**, imperative ("Stop the service"), in the order done.
- Each step specific enough to be **checkable**: exact command, field name, value,
  tolerance, form number. "Check the logs" fails; "Run `<cmd>`; confirm no lines contain
  `ERROR` in the last 10 minutes" passes.
- State the **expected result** after significant steps, and what to do if it differs.
- **Decision points** explicitly: "If the queue depth is over 10,000, go to step 12;
  otherwise continue." For complex branching, add a flowchart or decision table and keep
  steps and diagram in sync.
- Flag irreversible or high-risk steps *before* the step ("CAUTION: the next step deletes …").
- Include timings where they matter (hold 30 s; wait until status shows *Ready*, up to 5 min).
- Runbooks: start with **"How to know you need this runbook"** (symptoms/alerts) and end with
  **verification and escalation** (who to call, with what information).

## 4. Format choices
- Linear simple tasks → numbered list or checklist.
- Multi-role → swimlane diagram plus steps grouped by role.
- Repeated checks → checklist with initials/timestamps (regulated environments often need
  signed records).
Keep reference info (contact lists, config values) in linked tables, not inside steps.

## 5. Test before publishing
**Walkthrough test:** someone who didn't write it, ideally the least experienced intended
user, performs the procedure (or a dry run) using only the document while the writer
watches silently and notes every hesitation. Fix and repeat. For runbooks, rehearse in a
test environment or game day.

## 6. Document control and keeping it current
- Version, approval and effective date on each revision; a revision history table
  (what changed, why, who approved).
- One controlled master; printed copies marked "uncontrolled when printed".
- **Review triggers:** scheduled (e.g. annually), plus any system change, incident,
  audit finding or near-miss involving the process.
- Regulated settings (ISO 9001, GMP, ISO 27001) need evidence of control and training on
  new versions — *requirements vary by standard; check yours.*

## Gotchas
- Writing from memory → missed steps experts do unconsciously.
- Personal names as owners: people leave; use roles.
- Screenshots of systems that change monthly; prefer field names.
- Burying the "why": people skip steps they don't understand.

## Verify
- [ ] Header complete: owner role, scope, prerequisites, next review date.
- [ ] Every step is a single checkable action; decision points are explicit.
- [ ] A walkthrough by a non-author succeeded with no verbal help.
- [ ] Irreversible steps are flagged before they occur.
- [ ] Revision history and review triggers are recorded.
