---
id: business-finance.banking.retail-banking.account-onboarding-and-kyc
name: account-onboarding-and-kyc
category: business-finance
field: banking
product: retail-banking
tags: [banking, retail-banking, account-opening, customer-onboarding, kyc, know-your-customer, cdd, customer-due-diligence, edd, enhanced-due-diligence, aml, beneficial-ownership, ubo, sanctions-screening, pep, crs, fatca, risk-rating, branch-operations, mule-accounts, small-business-banking]
level: intro
status: docs-checked
description: "Open personal and small-business bank accounts correctly: needs-based product choice, ID verification, beneficial owners, sanctions/PEP screening, risk rating and EDD."
sources: ["https://www.ecfr.gov/current/title-31/section-1010.230", "https://www.legislation.gov.uk/uksi/2017/692/regulation/5", "https://www.irs.gov/instructions/iw8"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opening a personal or small-business account: onboarding and KYC at the front line

**Goal:** open accounts correctly first time — right product, identity verified,
customer due diligence (CDD) recorded — so the account isn't frozen later and the
branch doesn't fail its next compliance review.

*Draft: requirements differ by country and by each bank's policy. This describes the
common shape of FATF-style customer due diligence; your bank's procedures override it.*

## 1. Needs conversation before product
Ask what the account is for (salary, savings, business takings), expected monthly
volume, cash usage, international payments, and whether they need an overdraft or card.
This both picks the right product (fees, minimum balance, interest) and **is part of
due diligence**: the stated purpose and expected activity become the baseline that
transaction monitoring compares against later.

## 2. Identify and verify (personal)
- **Identify:** full name, date of birth, residential address (plus nationality / tax
  residency where required).
- **Verify** from reliable independent sources: typically one government photo ID
  (passport, driving licence, national ID) plus, where policy requires, proof of
  address (recent utility bill or bank statement). Electronic verification against
  credit-bureau or government databases is now common.
- Check: photo matches the person, document not expired, names/dates consistent,
  security features present. Copy or scan per procedure.
- **Tax self-certification** (CRS/FATCA): record tax residencies and TINs; where US status is indicated, follow your bank's FATCA procedure.

## 3. Small business (sole trader, partnership, company)
Add: legal entity verification (company registry extract), nature of business,
directors/partners, and **beneficial owners** — natural persons who ultimately own
or control the entity above the local threshold (US CDD rule: 25 percent or more of equity interests, 31 CFR 1010.230(d); UK MLRs reg. 5: more than 25% of shares or voting rights). Verify each beneficial
owner and each signatory. Get the mandate: who can sign, single or joint, limits.

## 4. Screening and risk rating
- Screen all parties against **sanctions** and **PEP** (politically exposed person)
  lists; check adverse media where policy says.
- Assign the customer risk rating per the bank's model (geography, product, cash
  intensity, PEP, business type).
- **High risk → enhanced due diligence (EDD):** source of funds/wealth evidence,
  senior manager approval. Don't open first and fix later.

## 5. Complete and explain
Set up the account, card, online banking; explain fees, overdraft terms, complaints
process and deposit-protection scheme coverage. Record everything in the core system
the same day.

## Gotchas
- **Name mismatches** between ID and proof of address (maiden name, transliteration):
  resolve and document, don't ignore.
- **Tipping off:** if something seems suspicious, don't tell the customer you're
  concerned or reporting. Escalate internally to the MLRO/compliance per procedure.
- **Third-party presence** — someone else answering for the applicant, or several
  unrelated applicants with the same address/phone — is a red flag for mule accounts.
- Declining someone for lack of a standard ID can exclude vulnerable customers; many
  banks have alternative-ID procedures (e.g. letters from a recognised authority) and
  basic-account rules. Know yours.
- Periodic review: KYC isn't one-off; refresh on a risk-based cycle and on trigger events.

## Verify
- [ ] Account purpose and expected activity are recorded.
- [ ] ID verified against an original or approved electronic check; expiry checked.
- [ ] Beneficial owners above threshold and all signatories identified and verified.
- [ ] Sanctions/PEP screening done and the risk rating set; EDD done if high risk.
- [ ] Tax self-certification captured; fees and key terms explained.

## Checked

Date checked: 2026-10-25. Jurisdiction: US federal and UK; the rest is general FATF-style practice (bank policy governs).
Sources read: eCFR 31 CFR 1010.230(d) (25 percent or more of equity interests; control prong); legislation.gov.uk SI 2017/692 reg. 5 (more than 25%). The specific list of FATCA US indicia was not confirmable from free pages in this review, so the skill now defers to the bank's FATCA procedure instead of listing them.

Method: documentation only; no commands were run.
