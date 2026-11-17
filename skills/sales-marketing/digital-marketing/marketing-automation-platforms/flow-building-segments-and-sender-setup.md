---
id: sales-marketing.digital-marketing.marketing-automation-platforms.flow-building-segments-and-sender-setup
name: flow-building-segments-and-sender-setup
category: sales-marketing
field: digital-marketing
product: marketing-automation-platforms
tags: [marketing-automation-platforms, marketing-automation, klaviyo, mailchimp, hubspot-marketing-hub, braze, esp, email-service-provider, flows, journeys, customer-journeys, workflows, segments, dynamic-segments, lists, templates, dynamic-content, personalisation-tags, liquid, sending-domain, dedicated-ip, shared-ip, ip-warm-up, domain-warm-up, dkim, spf, dmarc, suppression, sms-marketing, push-notifications]
level: practitioner
status: draft
description: "Run lifecycle programmes in Klaviyo, Mailchimp, HubSpot or Braze: sending-domain setup and warm-up, dynamic segments, flow/journey building with filters and splits, templates and dynamic content."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Marketing automation platforms — setup, segments, flows

**Goal:** a correctly authenticated, warmed-up sending setup and a set of
well-built automated flows that trigger on the right events, for the right people.
Strategy (which flows, cadence) is in
`sales-marketing.digital-marketing.email-marketing.list-segmentation-flows-and-deliverability`.

Vocabulary differs: Klaviyo **flows**, Mailchimp **Customer Journeys**, HubSpot
**workflows**, Braze **Canvas**. Feature availability depends on plan tier; check vendor
docs for exact steps.

## 1. Sender setup
1. **Branded sending domain** (e.g. `send.example.com`): add the DNS records the
   platform gives you — DKIM (CNAME/TXT), SPF include where required, and a DMARC record
   on the root domain. Verify inside the platform.
2. From-name and from-address people recognise; a monitored reply-to.
3. **Shared vs dedicated IP:** most senders stay on the platform's shared pools.
   Dedicated IPs suit high, consistent volume (often cited as hundreds of thousands
   of emails per month or more) and need warming.
4. **Warm-up:** for a new domain/IP, start with your most engaged contacts and increase
   daily volume over roughly 2–6 weeks; platforms like Braze and Klaviyo publish
   warm-up schedules — follow theirs.

## 2. Data in
- Install the platform's e-commerce or CRM integration (Shopify/WooCommerce/Salesforce)
  and web tracking script; confirm events arrive (Klaviyo: *Analytics › Metrics*; Braze:
  custom events; HubSpot: contact timeline).
- Map key properties: consent status, signup source, first order date, total orders,
  predicted or computed fields.
- Import historic lists with consent evidence only; set unsubscribed/bounced contacts to
  suppressed on import.

## 3. Segments
- Use **dynamic segments** (rules re-evaluated automatically) over static lists, e.g.
  "Placed order at least once in last 365 days AND opened/clicked email in last 90 days".
- Core segments: engaged 30/90/180 days, customers vs never-purchased, VIP by spend,
  lapsed, by category interest, by location (for send-time or legal reasons).
- Name segments consistently (`ENG_90d`, `CUST_VIP`); document the rule in its description.

## 4. Building a flow
1. **Trigger:** event (Started Checkout, Placed Order), list/segment entry, date
   property (birthday), or API event.
2. **Flow filters:** who should exit (e.g. "Placed Order zero times since starting
   this flow" for abandoned cart) — the filter that stops embarrassing emails.
3. **Time delays** between messages; respect quiet hours/time zones where supported.
4. **Conditional splits** on behaviour or properties (first-time vs repeat buyer).
5. **Messages:** email, SMS, push, in-app — with consent per channel. SMS needs its own
   opt-in and has strict legal rules (e.g. US TCPA, carrier registration).
6. **A/B tests** within the flow on subject or content once volume allows.
7. Set **smart sending / frequency caps** so flows and campaigns don't pile up.
Preview with a real profile, send tests to seed inboxes (Gmail, Outlook, Apple Mail),
then set live (or manual-review mode first if available).

## 5. Templates and dynamic content
- Build a master template with brand header/footer, legal address and unsubscribe link.
- Personalisation tags / Liquid-style syntax with **fallbacks**, e.g. first name → "there"
  (check your platform's syntax). Dynamic product blocks pull cart or recommended items.
- Test rendering on mobile and dark mode.

## 6. Ongoing monitoring
Per flow monthly: recipients, click rate, conversion rate, revenue per recipient,
unsubscribe and spam complaint rates; deliverability dashboards (bounce, complaint).

## Gotchas
- Flows built before the integration backfills data may trigger on old events — check
  "skip profiles who previously…" settings at launch.
- Missing exit filters send abandoned-cart emails to people who already bought.
- Merge-tag errors ("Hi {{ first_name }}") reach thousands; always preview with empty fields.
- Switching ESP restarts warm-up and loses engagement history; plan migrations carefully.

## Verify
- [ ] Sending domain authenticated (DKIM/SPF/DMARC) and verified in the platform.
- [ ] Warm-up schedule followed for any new domain or IP.
- [ ] Integration events visible on a test profile.
- [ ] Every flow has trigger, exit filters, delays and frequency limits; tested in seed inboxes.
- [ ] Personalisation fallbacks present; monthly flow metrics reviewed.
