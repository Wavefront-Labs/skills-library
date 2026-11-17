---
id: law-government.tax-law.estate-and-gift-tax-planning.transfer-tax-analysis-and-gifting-instruments
name: transfer-tax-analysis-and-gifting-instruments
category: law-government
field: tax-law
product: estate-and-gift-tax-planning
tags: [estate-and-gift-tax-planning, tax-law, estate-tax, gift-tax, transfer-tax, inheritance-tax, iht, unified-credit, basic-exclusion-amount, annual-exclusion, form-709, form-706, portability, dsue, marital-deduction, qtip, qdot, generation-skipping-transfer-tax, gst-tax, grat, ilit, crummey-powers, slat, idgt, valuation-discounts, family-limited-partnership, section-2036, adequate-disclosure, potentially-exempt-transfer, nil-rate-band]
level: advanced
status: docs-checked
description: "Running a transfer-tax analysis and choosing lifetime instruments: exemptions, marital deduction, GST, GRATs, ILITs, valuation discounts, gift-tax returns and their traps."
sources: ["https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax", "https://www.law.cornell.edu/uscode/text/26/2001", "https://www.law.cornell.edu/uscode/text/26/2035", "https://www.law.cornell.edu/uscode/text/26/2036", "https://www.law.cornell.edu/uscode/text/26/2503", "https://www.law.cornell.edu/uscode/text/26/2056", "https://www.law.cornell.edu/uscode/text/26/6075", "https://www.law.cornell.edu/uscode/text/26/6501", "https://www.irs.gov/pub/irs-drop/rp-22-32.pdf", "https://www.gov.uk/inheritance-tax", "https://www.gov.uk/inheritance-tax/gifts", "https://www.gov.uk/government/publications/rates-and-allowances-inheritance-tax-thresholds-and-interest-rates/inheritance-tax-thresholds-and-interest-rates"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Transfer-tax analysis and gifting instruments

**Goal:** estimate the client's transfer-tax exposure, then pick and document the
instruments that reduce it without creating income-tax, control or family problems. Jurisdiction: US
federal estate, gift and GST tax (checked current on 2026-10-24) is the model, with UK inheritance tax (IHT) contrasts;
exemption amounts and rates are changed by legislation and inflation indexing — always
pull the current year's figures.

## 1. Build the exposure model
1. Balance sheet by owner (H, W, joint, trusts) and by **title and beneficiary
   designation** — life insurance, retirement accounts and closely held interests drive most
   estates.
2. Value: market value for listed assets; qualified appraisal for real estate and private
   business interests; note any discount arguments.
3. Compute: gross estate − deductions (debts, expenses, marital, charitable) − remaining
   exemption (US: basic exclusion amount less lifetime taxable gifts; $15,000,000 for 2026 and $13,990,000 for 2025, per the IRS; indexed after) = taxable amount × top rate (US 40% on amounts over $1,000,000 under IRC §2001(c); UK IHT standard 40%, nil-rate band £325,000 (listed to 5 April 2031) and residence nil-rate band £175,000 (listed to 5 April 2030), giving up to £500,000 when a home passes to descendants, per gov.uk; the 36% charity rate applies if 10% or more of the net estate goes to charity).
4. Model both deaths, both orders, and state-level estate or inheritance taxes, whose
   thresholds can be far lower than federal ones.

## 2. Use the free tools first

| Tool | US | UK analogue |
|---|---|---|
| Annual exclusion gifts | Per donee per year, indexed ($19,000 for 2025 and 2026 per the IRS; indexed under §2503(b)); present-interest gifts only | Annual exemption (£3,000), small gifts (£250), normal expenditure out of income |
| Spousal transfers | Unlimited marital deduction for US-citizen spouse; non-citizen surviving spouse needs a QDOT for the estate-tax marital deduction (§2056(d)) | Spouse exemption (limits can apply for non-UK-domiciled spouses — check) |
| Unused exemption of first spouse | **Portability** (DSUE) — via a timely Form 706 (or the Rev. Proc. 2022-32 late election below) | Transferable nil-rate band (confirm on gov.uk) |
| Direct tuition/medical payments | Excluded if paid directly to the school or medical provider (§2503(e)) | Normal expenditure out of income rules |

## 3. Choose lifetime instruments
- **GRAT:** grantor keeps an annuity for a term; appreciation above the statutory rate
  passes gift-tax-free. Risk: grantor death in the term.
- **ILIT:** irrevocable trust owns life insurance outside the estate; **Crummey**
  withdrawal notices make premium gifts annual-exclusion gifts. Policy interests transferred
  within three years of death can be pulled back into the estate (§2035(a)).
- **SLAT:** gift to a trust for the spouse and descendants; uses exemption while keeping
  indirect access. Plan for divorce and the reciprocal-trust doctrine.
- **Sale to an intentionally defective grantor trust (IDGT):** freezes value; grantor
  pays the trust's income tax.
- **Family entities (FLP/LLC):** lack-of-control and marketability discounts. Respect
  formalities; personal-use assets, commingling and deathbed formation invite inclusion
  under US s.2036.
- **Charitable trusts (CRT/CLT)** where charitable intent exists.
- UK: lifetime gifts are usually **potentially exempt transfers** that fall out after
  seven years (taper relief reduces the tax on gifts made 3 to 7 years before death: 32%, 24%, 16%, 8%, and only
  where gifts exceed the £325,000 threshold; within 3 years 40%); gifts with reservation of benefit stay in the estate.

## 4. Compliance
- US gift tax return (Form 709) due 15 April after the calendar year of the gift (§6075(b)), with an income-tax
  extension also extending it; file even when no tax is due if exemption is used or GST is allocated.
- **Adequate disclosure** on the 709 (appraisal, method, discounts) starts the
  limitations period (§6501(a): three years after the return is filed; §6501(c)(9): an inadequately disclosed
  gift stays open); without it the IRS can revalue later.
- Allocate GST exemption deliberately; review automatic allocation rules.
- Estate tax return (Form 706) due nine months after death (§6075(a));
  portability can still be elected late, up to the fifth anniversary of death, under Rev. Proc. 2022-32, but only for estates not otherwise required to file under §6018(a); later relief needs a §301.9100-3 ruling.

## Gotchas
- Gifting low-basis assets loses the death basis step-up; compare income-tax cost.
- State estate taxes can make a federally exempt estate taxable.
- Retained powers (to change beneficiaries, live in the house) pull assets back in.
- Missing Crummey notices or appraisal deadlines.

## Verify
- [ ] Exposure modelled for both deaths with current-year exemption figures cited.
- [ ] Titling and beneficiary designations match the plan.
- [ ] Each instrument's income-tax and control consequences explained in writing.
- [ ] Appraisals obtained; 709/706 filing and GST allocations diaried.
- [ ] Annual maintenance (notices, annuity payments, entity formalities) assigned.

## Checked

Checked 2026-10-24. Jurisdiction: US federal transfer taxes and UK inheritance tax. Sources: IRS "What's New - Estate and gift tax"; Cornell LII text of 26 U.S.C. §§2001, 2035, 2036, 2503, 2056, 6075 and 6501; IRS Rev. Proc. 2022-32 (summarised in an IRS search result); gov.uk Inheritance Tax, gifts and thresholds pages.

Confirmed: 2026 basic exclusion amount $15,000,000 ($13,990,000 for 2025); annual exclusion $19,000 for 2025 and 2026; 40% top rate above $1,000,000; tuition and medical exclusion only when paid directly; QDOT rule; Form 709 due 15 April and Form 706 due nine months after death; adequate-disclosure limitation rule; Rev. Proc. 2022-32 five-year late portability for estates not required to file; UK nil-rate band £325,000 (to 5 April 2031), residence nil-rate band £175,000 (to 5 April 2030), £500,000 combined, 36% charity rate at 10%, seven-year rule and taper table, £3,000 annual and £250 small-gift exemptions. Removed as unconfirmed: the higher annual limit for non-citizen spouses and the earlier statement that Form 706 is extendable.

Method: documentation only; no commands were run.
