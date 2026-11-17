---
id: sales-marketing.digital-marketing.email-marketing.list-segmentation-flows-and-deliverability
name: list-segmentation-flows-and-deliverability
category: sales-marketing
field: digital-marketing
product: email-marketing
tags: [email-marketing, email-list, list-building, opt-in, double-opt-in, lead-magnet, segmentation, rfm, lifecycle-email, automation-flows, welcome-series, abandoned-cart, browse-abandonment, post-purchase, win-back, sunset-policy, campaigns, subject-lines, deliverability, spf, dkim, dmarc, bulk-sender-requirements, one-click-unsubscribe, spam-complaints, gdpr, can-spam]
level: practitioner
status: draft
description: "Sell through email: build a consented list, segment by behaviour, run core automated flows (welcome, abandoned cart, post-purchase, win-back), send campaigns and protect deliverability."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Email marketing — list, segments, flows, deliverability

**Goal:** an email programme where automated flows earn steadily in the background,
campaigns go to people who want them, and messages reach the inbox.
Platform setup is in
`sales-marketing.digital-marketing.marketing-automation-platforms.flow-building-segments-and-sender-setup`.

## 1. Build the list (with consent)
- Signup forms: site footer, checkout opt-in, a timed or exit-intent pop-up with a clear
  offer (discount, guide, early access).
- Collect only what you'll use (email + first name; maybe one preference question).
- **Consent:** GDPR/UK GDPR and similar laws need clear opt-in for marketing; CAN-SPAM
  (US) requires honest headers, a physical address and working unsubscribe. Double
  opt-in improves list quality; consider it where law or deliverability warrants.
- Never buy lists.

## 2. Segment
Start with a few segments that change what you'd say:
- **Lifecycle:** subscriber never purchased / first-time buyer / repeat buyer / lapsed.
- **Engagement:** opened or clicked in the last 30/90/180 days.
- **RFM** (recency, frequency, monetary) for stores with order history.
- Interest/category from clicks or purchases.
Send most campaigns to engaged segments; mail the unengaged rarely.

## 3. Core automated flows (build these before more campaigns)
| Flow | Trigger | Typical shape |
|---|---|---|
| **Welcome** | Signup | 3–5 emails over ~1–2 weeks: deliver the offer, brand story, best-sellers, social proof |
| **Abandoned cart / checkout** | Cart or checkout started, no order | 2–3 emails: ~1 h, ~24 h, ~48–72 h; show the items; incentive only in the last, if at all |
| **Browse abandonment** | Product viewed, no cart | 1–2 emails with viewed items |
| **Post-purchase** | Order placed | Thanks + what to expect, how-to/usage, review request, cross-sell |
| **Win-back** | No purchase in X days (based on your repurchase cycle) | 2–3 emails, reminder → incentive → last chance |
| **Sunset** | No engagement in ~90–180 days | Re-permission email, then suppress non-responders |
Timings are common starting points; test your own.

## 4. Campaigns
- Calendar: a steady cadence (e.g. 1–3 per week for e-commerce) plus key moments.
- One main message and one primary call to action per email.
- Subject line: specific, under ~50 characters, preview text that adds information.
- Design for mobile first; keep image-to-text balanced; alt text on images.
- A/B test one element at a time (subject, offer, send time) with a meaningful sample.

## 5. Deliverability
- Authenticate your sending domain: **SPF**, **DKIM**, **DMARC** (start at `p=none`,
  monitor reports, tighten over time). Major mailbox providers (Gmail, Yahoo) require
  these for bulk senders since 2024, plus **one-click unsubscribe** and spam complaint
  rates kept low (Google publishes a threshold of 0.3%, recommending well under 0.1%).
- **Warm up** new domains/IPs: start with your most engaged segment and increase volume
  gradually over weeks.
- Watch bounce rate, complaint rate, and Google Postmaster Tools reputation.
- Suppress hard bounces and long-term non-engagers.

## Gotchas
- Open rates are inflated by Apple Mail Privacy Protection; judge on clicks, orders and revenue.
- Over-discounting in flows trains customers to wait for codes.
- Sending everyone everything raises complaints and hurts the inbox placement of all mail.
- Requirements from mailbox providers and privacy law change — recheck yearly.

## Verify
- [ ] Every signup source records consent and source.
- [ ] Welcome, abandoned-cart, post-purchase and win-back flows live and reporting revenue.
- [ ] Campaigns go to engaged segments; sunset policy active.
- [ ] SPF, DKIM, DMARC pass; one-click unsubscribe works.
- [ ] Complaint rate and bounce rate monitored per send.
