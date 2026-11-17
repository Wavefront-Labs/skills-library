---
id: business-finance.accounting.financial-reporting.revenue-recognition-five-step-model
name: revenue-recognition-five-step-model
category: business-finance
field: accounting
product: financial-reporting
tags: [financial-reporting, revenue-recognition, ifrs-15, asc-606, five-step-model, performance-obligations, transaction-price, variable-consideration, standalone-selling-price, contract-assets, contract-liabilities, deferred-revenue, principal-vs-agent, saas-revenue, over-time-recognition, point-in-time, gaap, ifrs, disclosure-notes]
level: advanced
status: gated
description: "Apply the IFRS 15 / ASC 606 five-step model: identify contracts and performance obligations, set and allocate price, recognise over time or at a point, and document it."
sources: ["IFRS 15 Revenue from Contracts with Customers (IASB)", "ASC 606 (FASB)", "https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revenue recognition: the five-step model (IFRS 15 / ASC 606)

**Goal:** decide *how much* revenue to recognise and *when*, for any customer contract,
in a way an auditor can follow from your memo. IFRS 15 and ASC 606 were issued together in May 2014 and share the five-step core model (confirmed on the IFRS Foundation IFRS 15 page; IFRS 15 applies to periods beginning on or after 1 January 2018); differences are in the detail (noted below where known).

## The five steps
1. **Identify the contract.** Enforceable rights and obligations, approved by both
   parties, payment terms identifiable, commercial substance, and collection
   *probable*. Combine contracts signed near the same time with the same customer
   if they were negotiated as a package. Note: "probable" is a higher threshold under
   US GAAP than IFRS — one of the real differences (gated: unconfirmed, source is paywalled or blocked).
2. **Identify performance obligations (POs).** A promised good/service is a separate
   PO if it is *capable of being distinct* and *distinct in the context of the
   contract* (not highly integrated with, or significantly modifying, other promises).
   Typical SaaS split: subscription access, implementation (often distinct if a third
   party could do it), premium support. Don't forget implied promises — free upgrades,
   customer options to buy more at a discount (a *material right*).
3. **Determine the transaction price.** Fixed consideration plus **variable
   consideration** (rebates, bonuses, usage, penalties, refunds) estimated by expected
   value or most-likely amount, **constrained** so a significant reversal is highly
   probable not to occur. Adjust for significant financing components (usually ignored
   if payment is within a year of delivery, a practical expedient (gated: unconfirmed, source is paywalled or blocked)) and consideration payable to the customer.
4. **Allocate the price** to POs in proportion to **standalone selling prices** (SSP).
   Use observable prices where you have them; otherwise adjusted market assessment,
   expected cost plus margin, or (only in narrow cases) the residual approach.
   Discounts go proportionally to all POs unless evidence shows they belong to one.
5. **Recognise revenue when (or as) each PO is satisfied.** *Over time* if one of:
   customer consumes the benefit as you perform (subscriptions, cleaning), you enhance
   an asset the customer controls, or you create an asset with no alternative use and
   have an enforceable right to payment for work to date. Otherwise *at a point in
   time* when control passes (indicators: legal title, physical possession, risks and
   rewards, acceptance, right to payment).

## Measuring progress over time
- **Output methods** (milestones, units delivered) or **input methods** (cost-to-cost,
  hours). Exclude inefficiencies and uninstalled materials from cost-to-cost.
- Time-elapsed (straight line) suits stand-ready obligations like subscriptions.

## Balance-sheet consequences
- Cash before performance → **contract liability** (deferred revenue).
- Performance before an unconditional right to invoice → **contract asset**; once the
  right is unconditional it becomes a **receivable**.
- Incremental costs to obtain a contract (sales commissions) are capitalised and
  amortised if the benefit lasts more than a year (practical expedient otherwise (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- **Principal vs agent:** if you don't control the good before it transfers (a
  marketplace), you report only your commission (net), not gross sales.
- **Contract modifications:** a change that adds distinct goods at SSP is a new
  contract; otherwise you either restart prospectively or catch up cumulatively.
- **Bill-and-hold and consignment** rarely qualify for early recognition.
- **Licences of IP:** "right to access" (over time) vs "right to use" (point in time)
  — a frequent judgement area; check the specific standard paragraphs.
- Detailed differences between IFRS and US GAAP (licensing, collectability, shipping
  as fulfilment) are not confirmed here (gated: unconfirmed, source is paywalled or blocked); read the standards before relying on them.

## Verify
- [ ] A short memo per contract type walks through all five steps with judgements.
- [ ] Every PO has an SSP with its evidence, and allocation sums to the price.
- [ ] Variable consideration estimates and the constraint are documented and reviewed
      each period.
- [ ] Contract asset/liability roll-forwards tie to the ledger.
- [ ] Disclosures cover disaggregated revenue, contract balances, remaining POs and
      key judgements.
