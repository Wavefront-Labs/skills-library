---
id: law-government.tax-law.international-tax-law.treaty-withholding-and-permanent-establishment-analysis
name: treaty-withholding-and-permanent-establishment-analysis
category: law-government
field: tax-law
product: international-tax-law
tags: [international-tax-law, tax-law, cross-border-tax, double-tax-treaty, tax-treaty, oecd-model-convention, un-model-convention, treaty-residence, tie-breaker, permanent-establishment, pe, dependent-agent, withholding-tax, wht, dividends, interest, royalties, beneficial-ownership, principal-purpose-test, ppt, limitation-on-benefits, lob, multilateral-instrument, mli, transfer-pricing, arms-length-principle, form-w-8ben-e, certificate-of-residence, foreign-tax-credit]
level: advanced
status: docs-checked
description: "Working a cross-border payment through a tax treaty: residence, permanent establishment, withholding rates, anti-abuse tests, documentation and transfer-pricing touchpoints."
sources: ["https://www.oecd.org/en/publications/model-tax-convention-on-income-and-on-capital-2025-full-version_db32e18b-en.html", "https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/beps-mli/mli-frequently-asked-questions.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Treaty, withholding and permanent-establishment analysis

**Goal:** answer the three recurring cross-border questions — who may tax this income,
at what rate must the payer withhold, and has the foreign enterprise created a taxable
presence — with a written analysis that survives audit. The OECD Model Convention is the
frame; actual treaties deviate article by article, and domestic law always comes first. Checked 2026-10-24 against the
OECD Model (2025 edition) and OECD MLI materials. Not tax advice.

## 1. Start with domestic law
1. Characterise the payment under the **source country's** domestic law (dividend,
   interest, royalty, service fee, capital gain, business profit).
2. Find the domestic withholding rate and any domestic exemption (EU directives, portfolio
   interest exemptions, participation exemptions). A treaty can only reduce tax, not create it.

## 2. Find and read the right treaty
- Confirm the treaty is in force and its effective date for withholding taxes.
- Check whether the **Multilateral Instrument (MLI)** modifies it — read the synthesised
  text and both countries' reservations and notifications.
- Read the relevant article, its protocol, and any competent-authority agreements;
  use the OECD Commentary as an interpretive aid (weight varies by country).

## 3. Residence and entitlement
- Recipient must be a **resident** of the treaty partner (liable to tax there). For dual
  residents apply the tie-breaker (read the treaty's residence article).
- Transparent entities (partnerships, LLCs) — look through to members as the treaty or
  domestic rules require.
- **Beneficial ownership** of dividends, interest and royalties: conduit companies with
  back-to-back obligations fail.
- Anti-abuse: **principal purpose test (PPT)** — would obtaining the benefit be one of the
  principal purposes of the arrangement? — and any limitation-on-benefits (LOB) article in the treaty.

## 4. Rates and mechanics

| Income | Typical OECD-model outcome (verify the actual treaty) |
|---|---|
| Dividends | OECD Model Art. 10: check the treaty's rates and holding thresholds |
| Interest | OECD Model Art. 11: check the treaty's rate |
| Royalties | OECD Model Art. 12: check the treaty's rate |
| Business profits | OECD Model Art. 7: taxable in the source state only if attributable to a PE |

Mechanics: relief at source (payer holds residence certificate or status documentation, for US payments for example Form
W-8BEN-E) or refund afterwards (file within the reclaim limitation period). Keep documents
current; many expire after a fixed period.

## 5. Permanent establishment
- **Fixed place PE:** a place of business at the enterprise's disposal through which
  business is carried on; time thresholds set by the treaty (check).
- **Dependent agent PE:** a person habitually concluding contracts, or playing the
  principal role leading to them (post-MLI wording, where adopted).
- **Exceptions:** preparatory or auxiliary activities, now subject to anti-fragmentation rules.
- Remote employees and service PEs (where the treaty has one) are active risk areas; record days, roles and authority to sign.
If a PE exists, attribute profits under the treaty's business-profits article and domestic rules, and coordinate with transfer pricing.

## 6. Transfer-pricing touchpoint
Related-party payments must be at arm's length; withholding relief does not cure a
mispriced royalty. Check that the transfer-pricing documentation supports the payment.

## Gotchas
- Applying the OECD model rate rather than the treaty's actual rate.
- Ignoring MLI changes to an older treaty.
- Hybrid entities: the payer and recipient country may classify them differently.
- Expired residence certificates — the payer bears the under-withholding.

## Verify
- [ ] Domestic characterisation and rate documented before treaty analysis.
- [ ] Treaty in force, MLI-modified text checked, article cited precisely.
- [ ] Residence, beneficial ownership, PPT/LOB each addressed in writing.
- [ ] PE facts (days, contracts, premises) recorded and conclusion stated.
- [ ] Withholding documentation valid on the payment date; foreign tax credit position confirmed.

## Checked

Checked 2026-10-24. Jurisdiction: OECD Model Tax Convention and OECD MLI (treaty text always controls). Sources: OECD Model Tax Convention 2025 full version page and OECD MLI FAQ, via OECD search results; IRS Form W-8BEN-E page.

Confirmed: OECD Model article numbers 7, 10, 11, 12 and business profits taxable at source only through a PE; MLI principal purpose test and dependent-agent and anti-fragmentation changes; Form W-8BEN-E is the US foreign-entity status certificate. Removed as unconfirmed: the generic rate outcomes for dividends, interest and royalties, the treaty-specific time thresholds, the UN-model service PE remark, the authorised OECD approach wording and the LOB detail.

Method: documentation only; no commands were run.
