---
id: defence-public-safety.intelligence-and-espionage.open-source-intelligence.osint-collection-plan-source-evaluation-and-reporting
name: osint-collection-plan-source-evaluation-and-reporting
category: defence-public-safety
field: intelligence-and-espionage
product: open-source-intelligence
tags: [intelligence-and-espionage, open-source-intelligence, osint, publicly-available-information, pai, collection-plan, intelligence-requirements, source-evaluation, admiralty-code, verification, geolocation, chronolocation, archiving, wayback-machine, chain-of-custody, berkeley-protocol, bellingcat, mh17, corporate-records, sanctions-research, disinformation, opsec, research-ethics, data-protection, gdpr, intelligence-studies]
level: practitioner
status: draft
description: "OSINT as a discipline: requirement-driven collection planning, source evaluation and verification, preservation for evidence, analyst OPSEC, legal and ethical limits, and graded OSINT reporting."
sources: ["UC Berkeley Human Rights Center and OHCHR, 'Berkeley Protocol on Digital Open Source Investigations' (2020/2022)", "NATO Open Source Intelligence Handbook (2001, unclassified)", "Bellingcat, MH17 investigation publications (2014-2016)", "Williams and Blum, 'Defining Second Generation Open Source Intelligence', RAND (2018)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OSINT: collection planning, source evaluation and reporting

**Goal:** answer a defined question from publicly available information to a standard
an analyst, editor or court will accept: planned, verified, preserved and graded.
Scope here is organisations, events, places, equipment and networks (e.g. sanctions
evasion, conflict events, supply chains). Profiling or locating a private individual is
a separate, heavily regulated activity and is deliberately not covered.

## 1. Start from a requirement, not a search box
Write the question, why it matters and who will use the answer. Break it into
sub-questions and **indicators** (what would be visible if X were true). Then a
collection plan: which source types could show each indicator — corporate registries,
procurement and court records, shipping/aviation tracking, satellite imagery, official
statements, trade data, academic papers, media, social media posted by the subject
organisation. OSINT without a plan becomes endless browsing and confirmation bias.

## 2. Evaluate every source and item
- Grade **source reliability** and **information credibility** separately (A–F / 1–6,
  as in HUMINT; see `defence-public-safety.intelligence-and-espionage.humint-tradecraft.source-handling-lifecycle-and-reporting-discipline`).
- Ask: who created it, how would they know, why was it published, is it first-hand?
- Count independent sources, not copies. Ten articles citing one press release are one
  source — "circular reporting" is the most common OSINT error.
- State-linked outlets, PR firms and coordinated accounts publish to be found by OSINT
  researchers. Treat convenience as a warning sign.

## 3. Verify user-generated content
Provenance (who first posted it), **geolocation** (match terrain, buildings, signage to
maps and imagery), **chronolocation** (shadows, weather records, events visible), and
manipulation checks. The Bellingcat MH17 work (2014–16) is the public exemplar of
combining these into a chain an international investigation later corroborated.
Detailed image method: `media-communication.editorial-photography-and-photojournalism.image-verification.verifying-an-image-provenance-geolocation-and-manipulation`.

## 4. Preserve as you go
Online material disappears. Capture the page (archive service plus local capture with
URL, timestamp, and a hash of the file), keep original media rather than screenshots
where lawful, and log every step. The Berkeley Protocol sets the standard for material
that may become evidence; work that cannot be reproduced is weak in court and in peer review.

## 5. Analyst OPSEC
Research can alert the subject: some platforms show who viewed a profile, and visits
appear in server logs. Organisations use separate research environments and accounts
created under policy. Gotcha: creating false personas or accessing anything behind a login
or paywall you are not entitled to may breach law, platform terms and professional rules
— and it stops being open source. Get organisational and legal sign-off.

## 6. Law and ethics
"Publicly available" does not mean "free to use for any purpose". Data-protection law
(e.g. UK/EU GDPR) applies to personal data found online; government use may require
authorisation as directed surveillance if research becomes systematic monitoring of a
person (UK RIPA guidance says so explicitly). Minimise personal data, avoid publishing
bystanders' details, and assess harm before release. Uncertainty: thresholds differ by
jurisdiction and by whether you are state, journalist or private sector.

## 7. Reporting
Bottom line first; key judgements with estimative language and confidence; each claim
footnoted to a preserved source; gaps and what further collection would close them;
alternative explanations. Distinguish "no evidence found" from "evidence of absence".

## Verify
- [ ] A written requirement and collection plan existed before collection.
- [ ] Every key claim rests on independent sources, not copies of one origin.
- [ ] Each cited item is archived with URL, timestamp and hash.
- [ ] Research stayed within lawful access and organisational authorisation.
- [ ] Personal data was minimised and harm of publication assessed.
