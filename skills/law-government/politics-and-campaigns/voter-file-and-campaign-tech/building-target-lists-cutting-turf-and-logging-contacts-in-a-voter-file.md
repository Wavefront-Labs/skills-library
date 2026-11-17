---
id: law-government.politics-and-campaigns.voter-file-and-campaign-tech.building-target-lists-cutting-turf-and-logging-contacts-in-a-voter-file
name: building-target-lists-cutting-turf-and-logging-contacts-in-a-voter-file
category: law-government
field: politics-and-campaigns
product: voter-file-and-campaign-tech
tags: [politics-and-campaigns, voter-file-and-campaign-tech, voter-file, voter-database, ngp-van, votebuilder, van, minivan, nationbuilder, pdi, i360, gop-data-center, campaign-crm, electoral-register, marked-register, list-building, targeting-universe, support-score, turnout-score, modelled-scores, turf-cutting, walk-lists, call-lists, survey-questions, activist-codes, canvass-results, contact-logging, data-hygiene, sync, data-protection, voter-data-access-rules]
level: practitioner
status: draft
description: "Use an NGP VAN/NationBuilder-class voter file: build target universes with filters and scores, cut turf, push lists to canvass apps, log results consistently, keep data clean and lawful."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building target lists, cutting turf and logging contacts in a voter file

**Goal:** turn the voter file into the right people to contact, in walkable/callable
batches, and get every contact result back in the same day so tomorrow's lists are
better than today's.

Platforms differ: in the US, NGP VAN/VoteBuilder (Democratic and progressive), the
GOP Data Center and i360 (Republican/conservative), PDI and others; NationBuilder and
party systems elsewhere. Access to electoral registers, permitted uses, and data
protection rules **vary by jurisdiction** (e.g. GDPR applies to voter data in the EU and
UK). UI names below follow NGP VAN conventions and are **from general familiarity, not
re-verified against the current release** — map them to your platform's equivalents.

## 1. Know your data
- Source: official voter registration file (+ vote history: which past elections each
  person voted in, not how) enhanced with commercial data, modelled scores (e.g.
  support and turnout probability 0–100) and the campaign's own contact history.
- Check the **file date** and when vote history was last loaded; early-vote/ballot-
  return data may be updated daily during the voting window.
- Learn the household and address model — lists can be by person or by household/door.

## 2. Build a universe
Start from the campaign plan's targets (see campaign-management):
1. **Create a list** filtered by geography (district, precincts), then
   vote history (e.g. voted in 1 of last 4 comparable elections), scores
   (support 40–60 = persuasion; support > 70 and turnout < 60 = GOTV), age, etc.
2. **Exclude**: already-contacted with a final result, strong opponents, deceased/
   moved flags, do-not-contact requests, people who've already voted (during GOTV).
3. Save the search criteria with a clear name and date ("PERS_D3_v2_2026-10-01") so
   it can be rebuilt; record the count.
4. Sanity-check a sample of records; check counts against expectations.

## 3. Cut turf
- **Walk turf:** contiguous areas sized for a 2–3 hour shift (roughly 50–80 doors in
  suburban areas, fewer rural, more dense urban — tune from your own completion data).
  Avoid crossing major roads; keep apartment complexes whole; respect access rules.
- **Call lists:** sized per shift; exclude numbers you may not dial under local
  telemarketing/consent rules.
- Assign turfs to teams in a shared tracker; push to the mobile canvass app (e.g.
  MiniVAN) via list numbers/QR codes or the platform's assignment feature.

## 4. Log results consistently
Define a small, fixed set of fields before contact starts:
- **Contact result:** not home, refused, moved, wrong number, inaccessible, deceased.
- **Survey questions:** e.g. support ID 1–5, top issue, voting plan (postal/early/
  election day).
- **Activist codes / tags:** volunteer interest, yard sign, donor prospect, needs ride.
Train volunteers on exact meanings; mismatched coding (one canvasser's "3" is another's
"2") poisons targeting. Sync apps before leaving staging; data-entry paper lists the
same day.

## 5. Reporting and hygiene
- Daily: attempts, contacts, IDs by level, by turf and by volunteer — catch fake or
  sloppy data early (impossibly fast door times, all "1"s).
- Merge duplicates; apply moved/deceased flags; honour opt-outs everywhere.
- **Access control:** least-privilege user roles, 2FA, no exporting lists to personal
  devices or spreadsheets without need; remove access at the end of the campaign.
- Retain or delete data per the platform's terms and local law after the election.

## Gotchas
- Old files and lagging vote history make GOTV chase people who've already voted.
- Over-tight filters produce universes too small to hit the vote goal.
- Coding schemes changed mid-campaign break comparisons.

## Verify
- [ ] File date and vote-history currency checked.
- [ ] Universe criteria saved, named and counted; exclusions applied.
- [ ] Turfs sized from completion data and assigned in a tracker.
- [ ] Fixed result/survey codes defined and trained; same-day sync.
- [ ] Access roles, 2FA and data-retention rules in force.
