---
id: sales-marketing.retail-sales.pos-operation.tendering-overrides-and-end-of-day-reconciliation
name: tendering-overrides-and-end-of-day-reconciliation
category: sales-marketing
field: retail-sales
product: pos-operation
tags: [pos-operation, pos, point-of-sale, till, cash-register, square, square-pos, shopify-pos, lightspeed, tendering, split-tender, cash-handling, card-payments, discounts, price-override, manager-override, loyalty-lookup, refunds, end-of-day, z-report, x-report, cash-up, till-reconciliation, float, over-short, retail-sales]
level: intro
status: draft
description: "Operate a retail POS (Square, Shopify POS, Lightspeed): ring and tender sales, apply discounts and overrides correctly, look up loyalty, and reconcile the till at end of day."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tendering, overrides and end-of-day reconciliation

**Goal:** every transaction is right first time, every discount is authorised and
recorded, and the till balances at close. Exact screens differ between Square, Shopify
POS, Lightspeed and legacy tills — the routine below is the same; menu names are
approximate and change with app updates.

## 1. Start of shift
- Log in under **your own staff PIN/account** — never someone else's. Every refund and
  override is traced to the login.
- Count the **float** (opening cash) with a supervisor or second count and record it
  (Square: *Cash management / start drawer*; Shopify POS: *Cash tracking session*;
  Lightspeed: *Open register* — confirm in your version).
- Test the card terminal is paired and the receipt printer has paper.

## 2. Ringing the sale
1. Scan every item (don't type SKUs unless it won't scan; mistyped codes break stock).
   For no-barcode items use the product search, not an "open price" key, unless policy allows.
2. Attach the **customer/loyalty profile** before tender (search by phone or email) so
   points and purchase history record. Ask: "Are you a member?"
3. Apply discounts **at the right level**: line-item (one product) vs cart (whole sale). Use
   the predefined discount codes, not a manual price change, so reporting shows why.
4. **Overrides** (price change, discount beyond your limit, no-receipt refund) need a
   manager PIN — that's a control, not an annoyance. Enter a reason note.

## 3. Tendering
- **Card:** let the customer tap/insert; never key card numbers manually unless it's an
  approved process (manual entry carries higher fees and fraud liability on most processors).
- **Cash:** state the amount received out loud ("from £50"), leave the note on the
  drawer ledge until change is counted back, then put it away. Prevents "I gave you a £50" disputes.
- **Split tender:** enter the first payment amount (e.g. gift card balance), then the rest
  on a second tender. Check the remaining balance shown before taking the second.
- Offer the receipt (print/email/SMS).

## 4. Refunds and voids
- **Void** = cancel a sale in progress or same-day before settlement (platform-dependent).
  **Refund** = reverse a completed sale — look up the original transaction and refund to
  the original tender.
- Never process a refund to your own card or a colleague's; most businesses treat that as
  gross misconduct.

## 5. End of day
1. Run an **X report** (mid-day snapshot, doesn't reset) if you need a check; the **Z report**
   or close-of-drawer at end resets totals (terms vary — Square and Shopify use "close
   drawer/session" rather than X/Z).
2. Count cash by denomination, twice. Subtract float → cash takings.
3. Compare to the POS expected cash: record **over/short**. Small variances happen; a
   recurring short of the same size is a pattern to investigate.
4. Card total: compare POS card total to the terminal batch/settlement report.
5. Bag the cash with a deposit slip, record seal number, store per policy.
6. Leave the next day's float counted and recorded.

## Gotchas
- Offline mode: many cloud POS systems can take card payments offline but they're
  processed later and can decline — know your limits and whether policy allows it.
- Discounts applied after tax vs before tax change the total; check your configuration.
- Gift cards are cash-equivalent; treat activations with the same care.
- Don't leave the drawer open or logged in when stepping away.

## Verify
- [ ] Float counted and recorded at open; logged in under your own PIN.
- [ ] Every discount uses a named code; overrides carry a manager PIN and reason.
- [ ] Refunds go to the original tender against the original sale.
- [ ] Cash counted twice at close; over/short recorded; card totals match the terminal batch.
- [ ] Next float prepared and deposit bagged per policy.
