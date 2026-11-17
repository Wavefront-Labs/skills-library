---
id: business-finance.compliance.aml-kyc.customer-due-diligence-and-risk-rating
name: customer-due-diligence-and-risk-rating
category: business-finance
field: compliance
product: aml-kyc
tags: [aml-kyc, compliance, aml, kyc, anti-money-laundering, cdd, customer-due-diligence, edd, enhanced-due-diligence, sdd, beneficial-ownership, ubo, pep, politically-exposed-person, sanctions-screening, ofac-50-percent-rule, adverse-media, customer-risk-rating, source-of-funds, source-of-wealth, ongoing-monitoring, periodic-review, sar, str, tipping-off, fatf]
level: practitioner
status: gated
description: "Onboard and risk-rate customers for AML: verify identity, identify beneficial owners, screen sanctions/PEP/adverse media, apply EDD where risk is high, and keep KYC current through periodic review."
sources: ["https://www.ecfr.gov/current/title-31/section-1010.230", "https://www.ecfr.gov/current/title-31/section-1020.320", "https://www.legislation.gov.uk/uksi/2017/692/regulation/5", "https://ofac.treasury.gov/faqs/398", "https://eur-lex.europa.eu/eli/reg/2024/1624/oj/eng"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Customer due diligence and risk rating — know who you're dealing with

**Goal:** before (and throughout) a relationship, establish who the customer really is,
who ultimately owns and controls them, what they'll do with you, and how risky that is —
and apply proportionate checks. The international baseline is the FATF Recommendations;
national law (e.g. EU AML Directives/Regulation, UK MLRs, US BSA and FinCEN CDD rule) sets
the exact requirements. **Your firm's AML policy and local law prevail over the general
practice below. Written for US, UK and EU practice as understood in October 2026; the EU
AML Regulation (EU) 2024/1624 replaces national rules from 10 July 2027 (gated: unconfirmed, source is paywalled or blocked). EUR-Lex returned no text for this review, so confirm which regime
and date applies to your customer and have a qualified compliance officer approve any procedure.**

## 1. Identify and verify
- **Individuals:** full name, date of birth, address; verify against reliable independent
  sources — government ID with liveness/biometric check, electronic verification, documents.
- **Entities:** legal name, registration number, registered address, legal form, directors,
  proof of existence (registry extract), constitutional documents for complex structures.
- **Beneficial owners (UBOs):** natural persons who own or control the entity — the common
  threshold is **25%** ownership or voting rights (US CDD rule: 25% or more; UK MLRs: more than 25%; the EU AMLR is reported as 25% or more, with lower thresholds possible for some higher-risk categories (gated: unconfirmed, source is paywalled or blocked). The official text could not be retrieved, so check Regulation (EU) 2024/1624), *plus* anyone with control by
  other means; if nobody qualifies, the senior managing official. Trace through layers; draw
  the ownership chart. Verify UBO identity, and compare with public registers where they exist
  (discrepancies may be reportable in some regimes).
- **Purpose and intended nature** of the relationship: products, expected volumes, counterparties,
  geographies — this is the baseline monitoring compares against.

## 2. Screen
- **Sanctions** — customer, UBOs, directors against applicable lists (UN, EU, UK OFSI, US OFAC).
  Apply the **ownership rule**: under OFAC's 50% rule, an entity owned 50% or more in aggregate
  by blocked persons is itself blocked even if not listed (OFAC's rule looks at ownership only, not control). Check the EU and UK regimes' own ownership and control tests. A true match means freeze/stop and report per the regime — this is not a risk-based choice.
- **PEPs** — politically exposed persons, family members and close associates. PEP status
  requires **EDD** and senior-management approval, not automatic rejection.
- **Adverse media** — search name variants with risk keywords; document relevance.
Tune fuzzy-matching; document how each potential match was discounted.

## 3. Risk-rate the customer
Score factors, then set Low / Medium / High:
- Customer type and structure (opaque trusts, nominee shareholders, bearer shares, shell
  companies), occupation/industry (cash-intensive, crypto, gambling, arms), PEP status.
- Geography — residence, incorporation, operations, counterparties (FATF grey/black lists,
  sanctions exposure, high corruption).
- Products and channels — non-face-to-face, cash, cross-border transfers, private banking.
- Expected activity — volume and value relative to profile.
Rating drives due-diligence depth and review frequency; *firm policy sets the review cycle*.

## 4. Enhanced due diligence (EDD)
For high risk: establish **source of funds** (where this money came from) and **source of
wealth** (how the customer became wealthy) with evidence, not just a statement; senior
approval; closer ongoing monitoring; understand the rationale for complex structures.

## 5. Ongoing monitoring and review
- Transaction monitoring against the expected profile; alerts investigated and documented.
- Event-driven reviews: change of ownership, adverse news, unusual activity, sanctions changes.
- Periodic refresh of KYC by risk rating.
- **Suspicion:** escalate internally to the MLRO/BSA officer, who decides on a SAR/STR filing.
  Never tell the customer (**tipping-off** is an offence in many regimes). US banks must file a SAR no later than 30 calendar days after initial detection (up to 60 days if no suspect is identified; 31 CFR 1020.320), for activity of at least $5,000. Other regimes set their own deadlines.

## Gotchas
- Stopping at the first corporate layer; UBOs are natural persons.
- Accepting the customer's own org chart without registry corroboration.
- Treating PEPs as prohibited (de-risking) or, opposite, approving without EDD.
- Expected-activity fields left vague ("various"), so monitoring has no baseline.
- Exiting a customer because of suspicion without considering reporting obligations first.

## Verify
- [ ] Identity verified from independent sources; UBOs traced to natural persons with a chart.
- [ ] Sanctions, PEP and adverse-media screening done; matches dispositioned in writing.
- [ ] Risk rating calculated with documented factors; EDD completed where High.
- [ ] Purpose and expected activity recorded specifically enough to monitor against.
- [ ] Review date set by rating; suspicion escalation path known to staff.

Related: business-finance.compliance.compliance-program-management.obligations-register-and-regulatory-change.

## Checked

Date checked: 2026-10-25. Jurisdiction: US federal (BSA/FinCEN, OFAC), UK (England, Wales, Scotland, NI), EU.
Sources read: eCFR 31 CFR 1010.230 (beneficial owner: 25 percent or more of equity interests; control prong is a single individual with significant responsibility to control, manage or direct) and 31 CFR 1020.320 (SAR within 30 calendar days of initial detection, up to 60 days if no suspect identified; $5,000 threshold); legislation.gov.uk SI 2017/692 reg. 5 (more than 25% of shares or voting rights, or control); OFAC FAQ 398 (50 percent rule is ownership only; control is not considered).
Not confirmed: the EU AMLR application date of 10 July 2027 and its 25% beneficial-ownership threshold. EUR-Lex returned empty pages; only secondary sources support them, so both carry the gated marker.

Method: documentation only; no commands were run.
