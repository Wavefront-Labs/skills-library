---
id: sales-marketing.pricing-and-promotions-execution.discount-application-and-overrides.authority-limits-price-match-and-audit-trail
name: authority-limits-price-match-and-audit-trail
category: sales-marketing
field: pricing-and-promotions-execution
product: discount-application-and-overrides
tags: [discount-application-and-overrides, discount, price-override, override, manager-override, discount-authority, authority-matrix, price-match, price-matching, price-beat, competitor-price, damaged-goods-discount, reason-codes, audit-trail, exception-report, pos, point-of-sale, cashier, retail-operations, shrink, sweethearting, loss-prevention]
level: intro
status: draft
description: "Apply discounts correctly at the till: know authority limits, verify and process price-match requests, use overrides with judgement and reason codes, and keep an audit trail that survives review."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authority limits, price match and the audit trail

**Goal:** give customers the discounts they're entitled to — quickly and
consistently — and only those, with every exception recorded so the business can
see where margin went. Overrides are where honest mistakes, inconsistent service
and internal theft (e.g. "sweethearting" discounts for friends) all hide.

## 1. Know the authority matrix
Most retailers define who may approve what. Typical shape (**illustrative —
use your store's actual policy**):
| Discount / override | Cashier | Supervisor | Store manager |
|---|---|---|---|
| Scanned price ≠ shelf price (correct to shelf) | yes | – | – |
| Damaged/display item | up to 10% | up to 25% | above |
| Price match (verified) | – | yes | – |
| Goodwill/service recovery | – | up to $X | above |
| Any manual price entry | – | yes | – |
Learn yours; if in doubt, call the supervisor — the customer waits 1 minute
instead of you breaching policy.

## 2. Price-match requests
Policy usually specifies:
- **Eligible competitors** (named list or "local stores", sometimes major online sites).
- **Identical item**: same brand, model number, size, colour, condition (new).
- **In stock** at the competitor and **currently** advertised at that price.
- **Exclusions**: marketplace sellers, clearance/open-box, membership-only prices,
  bundles, flash sales, errors, prices including rebates.
Process:
1. Ask the customer to show the price (website on phone, ad).
2. Verify: open the competitor page yourself on the store device if allowed; check
   model number, stock and that the price is current; check delivery charges if policy
   compares delivered price.
3. Apply via the POS **price-match function** with reason code, competitor and price
   recorded — not a generic manual override.
4. If declined, explain the specific reason politely and, if appropriate, offer an
   alternative (similar item on promotion).

## 3. Override judgement
Before overriding, ask:
- Is there a correct function for this (promo not applying, coupon, price match)?
  Fix the cause rather than keying a manual price.
- Is it within my authority?
- Would I make the same decision for any customer? (Consistency is fairness.)
- Is there a real reason — damage, error, service failure — that I can describe in
  one line?
Red flags: a regular asking for "the usual discount", pressure from friends or
family, discounts at the end of a shift, overrides on high-value small items.

## 4. Audit trail
- Every discount uses a **reason code** and, where required, the approver's ID —
  never share manager credentials or cards.
- Add a note for unusual cases (receipt number of the damaged item, competitor URL).
- Keep competitor evidence where policy requires (screenshot or ad).
- Managers review the **override/exception report** daily or weekly: overrides by
  cashier, by reason, by time; investigate outliers (e.g. one cashier with 5× the
  average discount value).

## 5. Customer conversation
- Lead with what you *can* do.
- Explain policy briefly; don't blame the system or head office.
- Escalate calmly when beyond your authority rather than improvising.

## Gotchas
- Manual price entry for a missing promo hides a setup error — report it.
- Matching an online price that excludes delivery while your price includes it.
- Approver credentials left logged in on a till = unaudited discounts.
- Local consumer law may override store policy for scanning errors — follow it.

## Verify
- [ ] You can state your authority limits for each discount type.
- [ ] Price matches verified for identical item, eligible seller, current and in stock.
- [ ] Correct POS function and reason code used; approver ID recorded.
- [ ] No shared credentials; unusual cases annotated.
- [ ] Exception report reviewed regularly and outliers followed up.
