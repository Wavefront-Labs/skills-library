---
id: law-government.politics-and-campaigns.voter-file-and-campaign-tech.building-universes-and-cutting-turf-in-a-voter-file
name: building-universes-and-cutting-turf-in-a-voter-file
category: law-government
field: politics-and-campaigns
product: voter-file-and-campaign-tech
tags: [voter-file-and-campaign-tech, politics-and-campaigns, voter-file, voterfile, ngp-van, votebuilder, minivan, nationbuilder, pdi, campaign-tech, crm, targeting-universe, list-building, saved-search, saved-list, turf-cutting, cut-turf, walk-list, call-list, virtual-phone-bank, survey-questions, activist-codes, contact-history, vote-history, support-score, turnout-score, modelled-scores, data-entry, list-hygiene, data-protection, electoral-register, uk-gdpr]
level: practitioner
status: draft
description: "Work an NGP VAN/NationBuilder-class voter file: universes from vote history and scores, saved lists, walkable turf, phone banks, consistent contact logging and clean, lawful data."
sources: ["NGP VAN / VoteBuilder and NationBuilder public help documentation", "UK ICO guidance on political campaigning and use of the electoral register"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building universes and cutting turf in a voter file

**Goal:** turn the campaign's target universes into accurate lists, walkable turf and
call lists, and get every contact result back into the file the same day. Written for
NGP VAN/VoteBuilder-class systems (US) and NationBuilder-class organising CRMs; UK
parties use their own systems on the electoral register. Menu names differ between tools
and versions — the concepts below transfer. Access to voter files and permitted uses are
set by law and by the data provider's terms (US state voter-file rules; UK electoral
register rules and data-protection law) — check before exporting anything.

## 1. Understand what's in the file
| Field type | Examples | Use |
|---|---|---|
| Registration | name, address, precinct/ward, party (where recorded) | universe and turf |
| Vote history | elections voted in, method (early/postal/in person) | turnout likelihood |
| Modelled scores | support, turnout, issue scores (0-100) | targeting |
| Contact history | survey responses, canvass results, activist codes | IDs, volunteers |
| Commercial / appended | phones, emails, age | contactability |
Know when the file was last refreshed against the official register — stale files mean
wasted doors.

## 2. Build a universe as a saved search
1. Start from the geographic scope (district, precincts).
2. Add criteria step by step and record counts at each step, e.g. persuasion: turnout
   score 50-100 AND support score 40-60 AND not already ID'd as a strong supporter or opponent.
   GOTV: support score above 70 OR ID'd as supporter, AND turnout score below 60, AND has
   not yet voted (from returned-ballot data).
3. Exclude: deceased, moved, do-not-contact, already voted.
4. Save the **search criteria** (so it can re-run with fresh data), not just a static list.
5. Sanity-check the count against the campaign plan's universe size; investigate big gaps.

## 3. Cut turf
- Load the universe into the turf-cutting map (VAN: "Cut Turf"; similar map tools elsewhere).
- Size each packet for one shift: commonly 40-80 doors for a 2-3 hour urban shift; fewer
  where houses are spread out.
- Draw along walkable boundaries (don't cross major roads or rivers); keep apartment
  buildings whole; check for access-controlled buildings.
- Name turf consistently (e.g. ward-number-letter) and print/assign to the mobile canvass app.
- Track which turfs are completed and how many passes each has had.

## 4. Phone and text lists
Create call lists with valid phones only; use the system's virtual phone bank or
predictive dialer according to the law (automated calling and texting to mobiles is
heavily restricted in some jurisdictions, e.g. US TCPA consent rules). Respect opt-outs
immediately.

## 5. Log contacts consistently
- Use one set of **survey questions** (e.g. support 1-5) and **result codes** (not home,
  refused, moved, wrong number) across all programmes.
- Use activist codes or tags for volunteer interest, yard signs, postal-vote request
  help, etc.
- Mobile apps sync in real time; paper results need data entry within 24 hours, with a
  second person spot-checking.
- Never create a new survey question when one already exists — duplicates fragment data.

## 6. Keep the data clean and lawful
- Permissions: give volunteers the narrowest access level that lets them do the job;
  remove access at the end of the campaign.
- Exports: only what is needed, stored securely, deleted when done; never on personal
  devices without approval.
- Merge duplicate records carefully, keeping contact history.
- Honour data-subject rights where data-protection law applies (UK/EU: access requests,
  objection to direct marketing).

## Gotchas
- Static lists that ignore new ballot-return data, sending volunteers to people who already voted.
- Turf packets too big to finish, leaving half-walked areas.
- Over-filtering until the universe is tiny but "pure".
- Volunteers creating ad hoc codes ("maybe2"), making the data unusable.

## Verify
- [ ] File refresh date known; universes saved as re-runnable searches with counts logged.
- [ ] Exclusions (deceased, moved, voted, do-not-contact) applied.
- [ ] Turf packets sized for a shift and drawn on walkable boundaries.
- [ ] One standard survey/result code set used everywhere; data entered within 24 hours.
- [ ] Access levels, exports and calling/texting comply with law and data-provider terms.
