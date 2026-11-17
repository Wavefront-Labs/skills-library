---
id: computing-software.digital-forensics-incident-response.evidence-handling.handling-a-broken-or-incomplete-chain-of-custody
name: handling-a-broken-or-incomplete-chain-of-custody
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [custody-gap, chain-of-custody, evidence-integrity, hash-verification, dfir]
level: advanced
status: draft
description: "Handle a broken or incomplete chain of custody: document the gap honestly, establish integrity by hashes and corroboration, take statements and limit the impact on findings."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://www.law.cornell.edu/rules/fre/rule_901", "https://www.swgde.org/documents/published-complete-listing", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handling a broken or incomplete chain of custody

Gaps happen: an IT admin pulled the drive before IR arrived, a courier lost a form, a seal was cut without a record. Courts generally treat custody gaps as going to the **weight** of evidence rather than automatic exclusion, if the proponent can show the item is what it claims and was not altered. Hiding a gap is far worse than disclosing it.

## Immediately
1. Stop and record the gap in the case notes: what is missing (who held the item, between which times), how you discovered it.
2. Do not try to reconstruct the form retrospectively as if contemporaneous; add a dated memo explaining the gap.
3. Secure the item now and start a correct chain from this point.

## Establish integrity another way
- **Hashes**: if an acquisition hash exists from before the gap, re-hash; a match proves the image did not change. For original media, compare against any earlier image or the collection hash.
- **Internal consistency**: file-system timestamps and logs show no activity during the gap window (e.g. no mounts in `setupapi.dev.log`/USB history for that period, last-shutdown time precedes the gap).
- **Corroboration**: the same events visible in independent sources (SIEM, cloud logs, email server) that were never in the gap.
- **Statements**: written statements from everyone who may have held the item, with times, what they did, and where it was stored. Access logs for the storage location, CCTV, courier tracking.

## Reporting
State the gap in the report's limitations section: dates, what is known, the integrity checks performed and their results, and which findings rely on the affected item. Where a finding depends only on the affected item and integrity cannot be shown, downgrade confidence or withdraw it.

## Prevent repeats
Feed the cause into procedure: first-responder training for IT staff, tamper-evident bags in every office, digital custody records with mandatory fields.

## Gotchas
- Native hash of a live system changes constantly; for live collections the anchor is the hash of the collected output at time of collection.
- Opposing experts look for gaps; disclose them in your own report first.

## Verify
The case file contains a gap memo, statements, integrity test results, and the report's limitations section names the gap and its effect on conclusions.
