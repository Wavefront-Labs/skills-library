---
id: law-government.corporate-and-commercial-law.contract-drafting.clause-architecture-indemnities-and-liability-caps
name: clause-architecture-indemnities-and-liability-caps
category: law-government
field: corporate-and-commercial-law
product: contract-drafting
tags: [contract-drafting, corporate-and-commercial-law, contract-drafting, commercial-contracts, drafting, clause-architecture, defined-terms, recitals, operative-provisions, representations-and-warranties, covenants, conditions, shall-vs-will, ambiguity, indemnity, indemnification, hold-harmless, defence-of-claims, limitation-of-liability, liability-cap, consequential-loss, exclusion-clause, carve-outs, boilerplate, governing-law, jurisdiction-clause, entire-agreement, force-majeure, assignment, notices, severability, termination, plain-language, ucta, adams-manual-of-style]
level: practitioner
status: docs-checked
description: "Drafting commercial contracts: document architecture, defined terms, operative language (shall/will/may), indemnities, limitation of liability, and boilerplate that matters."
sources: ["Unfair Contract Terms Act 1977 s3 (https://www.legislation.gov.uk/ukpga/1977/50/section/3)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contract drafting: architecture, indemnities and liability caps

**Goal:** a contract that says exactly what the deal is, allocates risk deliberately, and
can't be read two ways in a dispute. Principles apply across common-law systems;
enforceability of exclusions and penalties varies by jurisdiction and by consumer vs
business context.

## 1. Architecture
Standard order: title and parties → recitals (background, not obligations) → definitions
→ operative provisions (the deal) → representations and warranties → covenants →
conditions → term and termination → risk allocation (indemnities, liability limits) →
boilerplate → signatures → schedules. Put commercial detail (pricing, specs, SLAs) in
schedules so the body stays stable.

## 2. Language that works
- **Categories of contract language**: obligations ("shall"
  — or "must"), discretion ("may"), conditions ("must ... in order to"), declarations
  (statements of fact as representations), and language of performance ("hereby grants").
  Use "shall" only for obligations of a party and consistently.
- **Defined terms:** define once, capitalise, use identically. Don't bury obligations in
  definitions.
- **One concept, one word:** if you use "Products" and "Goods", a court may find two
  meanings.
- Avoid "and/or", "including" without "without limitation" where it matters, and
  undefined "reasonable efforts" vs "best efforts" (meanings vary by jurisdiction — define
  the efforts standard or list the steps).
- Numbers: one form, with time periods anchored ("within 30 days after the Delivery Date").

## 3. Indemnities
An indemnity is a promise to cover specific losses, often beyond what contract damages
would give. Draft:
- **Trigger:** third-party claims only, or also direct losses between the parties? Be explicit.
- **Scope:** "Losses arising out of [specific matters]" — e.g. IP infringement, breach of
  data protection obligations, personal injury, breach of law.
- **Procedure:** prompt notice, control of defence, cooperation, no settlement without
  consent, mitigation.
- **Interaction with caps:** say whether the indemnity is inside or outside the liability cap.
- Watch "hold harmless" and "defend" — in some US states they add separate duties.

## 4. Limitation of liability
- **Exclusion of indirect/consequential loss:** meaning differs between jurisdictions. Better:
  list excluded heads explicitly (lost profits, revenue, data, goodwill), and say whether
  they're excluded as direct losses too.
- **Cap:** fixed sum or multiple of fees, per claim or aggregate,
  per year or for the term.
- **Carve-outs** (uncapped): fraud, wilful misconduct, death/personal injury caused by
  negligence (check whether the governing law allows exclusion), confidentiality breaches, IP
  indemnity, payment obligations. Every carve-out is a negotiation point.
- Statutory controls: e.g. under s3 of the UK Unfair Contract Terms Act 1977, a party
  dealing on the other's written standard terms cannot exclude or restrict its liability for
  its own breach unless the term is reasonable; consumer contracts are covered by the
  Consumer Rights Act 2015.

## 5. Boilerplate that actually matters
Governing law and jurisdiction/arbitration; entire agreement (and non-reliance — check
it doesn't purport to exclude fraud); assignment and change of control; notices (addresses,
email validity); force majeure (defined events, notice, mitigation, termination after X
days); counterparts and e-signatures; order of precedence between body and schedules.
Read every boilerplate clause against this deal.

## 6. Review pass
Read once for the commercial deal, once for each party's obligations (make a table of who
does what by when), once for defined terms and cross-references, once for risk.

## Gotchas
- Penalty clauses and liquidated damages are tested differently in each jurisdiction; check
  the governing law.
- Cross-references break after renumbering — use automatic numbering.
- Precedents carry a previous deal's quirks; strip them.

## Verify
- [ ] Every obligation names who, what and when.
- [ ] Defined terms used consistently; no undefined capitals.
- [ ] Indemnity scope, procedure and cap interaction stated.
- [ ] Liability exclusions, cap and carve-outs checked for enforceability in the governing law.

## Checked
Checked 2026-10-24. Jurisdiction: common-law drafting practice, with England and Wales for the statutory example. Source read 2026-10-24: Unfair Contract Terms Act 1977 s3 (reasonableness for liability for breach under the other party's written standard terms; consumer contracts under the Consumer Rights Act 2015 s62). Removed unconfirmed statements about the Ken Adams framework, the English reading of consequential loss, personal injury exclusion, Cavendish v Makdessi, and the 12-month fee cap example. General information, not legal advice.
Method: documentation only; no commands were run.
