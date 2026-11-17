---
id: sales-marketing.pricing-and-promotions-execution.promotional-offer-execution.offer-setup-signage-audit-and-sunset
name: offer-setup-signage-audit-and-sunset
category: sales-marketing
field: pricing-and-promotions-execution
product: promotional-offer-execution
tags: [promotional-offer-execution, promotions, promo-execution, offer-setup, promo-setup, pos-pricing, price-file, signage, shelf-edge-label, sel, ticketing, price-accuracy, scanning-accuracy, promo-codes, coupon-codes, discount-codes, stacking-rules, exclusions, terms-and-conditions, offer-end, sunset, promo-calendar, retail-operations, ecommerce]
level: practitioner
status: draft
description: "Run a promotion cleanly at the customer end: set the offer up in POS and e-commerce, audit signage against scanned price, handle promo codes and stacking, and end it on time."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offer setup, signage audit and sunset

**Goal:** the price the customer sees on the sign, the website and the receipt is
the same, from the first minute of the promotion to the last — and the offer
switches off cleanly. Pricing errors cost margin, complaints and, in many
places, regulatory penalties (scanning/price-accuracy laws and codes).
The *strategy* (what to offer) is set upstream; this is execution.

## 1. Offer brief (one page, before setup)
Mechanic (e.g. 25% off, 3-for-2, $10 off $50), eligible SKUs (list, not
description), channels (stores, online, app), start and end date **and time with
time zone**, exclusions, stacking rules, redemption limits, code(s), funding
(vendor-funded?), signage needed, customer-facing T&Cs.

## 2. Set up in systems
- **POS/price management**: load promo price or rule with effective dates;
  check it targets the exact SKU list (not a whole category by accident).
- **E-commerce**: price rule or discount (e.g. Shopify discounts, Salesforce
  Commerce promotions, Magento cart price rules); set start/end, minimum
  spend, customer eligibility, usage limits (per code, per customer).
- **Promo codes**: unique single-use codes for targeted offers (prevents sharing
  on coupon sites); generic codes for broad campaigns with an overall cap.
- **Stacking rules**: decide explicitly whether the offer combines with loyalty
  discounts, staff discount, other codes, sale items. Default to "does not stack"
  unless the brief says otherwise, and state it in T&Cs.
- Test: scan/cart test transactions for 3–5 SKUs including edge cases (excluded
  item, minimum spend just under, two offers together).

## 3. Signage and labels
- Print signs/shelf-edge labels from the same price file loaded to POS, not retyped.
- Each sign: offer, price, unit price if required, valid dates, key conditions.
- Put up at the agreed time (e.g. after close the night before); take down old signs first.

## 4. Day-one price audit
In each store (or a sample), within the first hours:
- Pick 10–20 promoted items + 5 nearby non-promoted; scan each and compare to the sign.
- Online: check product page price, cart price, and price after code at checkout.
- Log errors with item, sign price, scanned price, fix and time. Fix by correcting
  the system *or* the sign — whichever is wrong — and escalate patterns
  (whole category wrong = setup error).
- Many retailers' policies (or local codes) give the customer the lower displayed
  price or more when a scanning error occurs — follow yours.

## 5. Handling the offer at the till
- Know the mechanic and exclusions; explain clearly why an item doesn't qualify.
- Codes that fail: check expiry, eligibility, minimum spend, already used;
  override only within authority (see authority-limits-price-match-and-audit-trail).
- Honour signed prices that are visibly displayed even if wrong, per policy, then fix the sign.

## 6. Sunset
- End date/time loaded in systems at setup, not manually on the day.
- Signs down at close on the last day; sweep the store (endcaps, window, secondary placements).
- Online: banners, emails and ads referencing the offer stopped; codes expire.
- Next morning: audit a sample of items back to normal price.
- Post-promo report: sales and margin vs plan, redemption count, error log.

## Gotchas
- Time zones and midnight: online offers ending "Sunday" — whose midnight?
- Leftover signs after the offer ends are the most common pricing complaint.
- Generic codes leak to coupon sites; cap usage.
- Unit price and "was/now" claims have legal rules in many places (reference-price rules).

## Verify
- [ ] Brief lists SKUs, channels, dates/times with time zone, stacking and exclusions.
- [ ] Test transactions passed for normal and edge cases before go-live.
- [ ] Signs generated from the same price file; day-one audit done and logged.
- [ ] End dates loaded at setup; signs and online assets removed on time.
- [ ] Post-promo check confirms prices reverted; results reported.
