---
id: sales-marketing.technical-b2b-sales.sales-engagement-platforms.outbound-cadences-in-outreach-salesloft-apollo
name: outbound-cadences-in-outreach-salesloft-apollo
category: sales-marketing
field: technical-b2b-sales
product: sales-engagement-platforms
tags: [sales-engagement-platforms, outreach, outreach-io, salesloft, apollo, apollo-io, hubspot-sequences, sequences, cadences, outbound, cold-email, cold-calling, sdr, bdr, personalisation-at-scale, merge-fields, snippets, ab-testing, reply-handling, meeting-booking, email-deliverability, spf, dkim, dmarc, domain-warmup, unsubscribe, gdpr, can-spam]
level: practitioner
status: draft
description: "Run outbound at volume in Outreach, Salesloft or Apollo: multi-channel cadence design, tiered personalisation, deliverability setup (SPF/DKIM/DMARC, volume caps), reply triage and A/B tests."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Outbound cadences in Outreach, Salesloft and Apollo

**Goal:** a multi-touch outbound sequence that lands in inboxes, sounds written for the
reader, books meetings, and stops automatically when someone replies.

The three tools differ in names (Outreach "sequences", Salesloft "cadences", Apollo
"sequences") and menus change often; steps below describe concepts that all three
support. Check current UI labels in your tenant — exact menu paths are not verified here.

## 1. Deliverability first (before any volume)
- **Separate sending domain or subdomain** for cold outbound (e.g. `get-<brand>.com` or
  `mail.<brand>.com`), so problems don't hit your main domain.
- DNS: **SPF** record including your mail provider, **DKIM** signing enabled, **DMARC**
  record at least `p=none` with reporting, moving to `quarantine` once clean. Check with
  any DMARC/SPF lookup tool.
- **Warm up** new mailboxes: start low (a few dozen emails/day) and ramp over weeks.
- **Daily caps** per mailbox in the platform's settings (many teams keep cold sends to
  low hundreds per mailbox per day or less). Major mailbox providers now expect bulk
  senders to keep spam complaints very low (around 0.3% is a commonly cited ceiling)
  and to offer one-click unsubscribe.
- Plain-text style, few links, no images or tracking pixels on first touches if open
  tracking hurts placement — test it.
- Verify emails (the platform's verification or a separate service) — bounces above a
  few percent damage the domain.

## 2. Cadence design (example: 14–21 days, 8–10 touches)
| Day | Channel | Purpose |
|---|---|---|
| 1 | Email (manual, personalised) | Relevance + one question |
| 1 | LinkedIn view / connect | Familiarity |
| 3 | Call + voicemail | Human touch, reference email |
| 5 | Email (reply in same thread) | New angle: proof point |
| 8 | Call | |
| 10 | LinkedIn message | Short, no pitch |
| 13 | Email | Case study / insight |
| 17 | Call | |
| 21 | Email "breakup" | Permission to close the loop |
Set **exit rules**: on reply, meeting booked, bounce, out-of-office (pause and resume
after return date), unsubscribe. Make sure the sequence's "finish on reply" setting is on.

## 3. Personalisation at scale (tiered)
- **Tier 1 accounts** (top ~10%): fully manual first email, researched trigger, manual tasks.
- **Tier 2**: template with a researched first line + persona-specific body.
- **Tier 3**: persona/industry template with merge fields.
Merge-field hygiene: preview every email; set fallbacks (e.g. `{{first_name | there}}` —
syntax differs per tool) and filter out records with blank or ALL-CAPS fields.
Email body pattern: trigger/observation (1 line) → problem peers have (1–2 lines) →
proof (1 line) → low-friction ask ("Worth a 15-min look?"). Under ~100 words.

## 4. Reply triage (daily)
Categorise every reply: interested → book (send calendar link or two specific times);
referral → thank and sequence the new contact referencing the referrer; not now →
set a dated follow-up task; objection → answer personally; unsubscribe/hostile → remove
and mark do-not-contact immediately. Log the reply category in the platform for reporting.

## 5. Test and measure
A/B test one variable at a time (subject line or first line or CTA) with enough volume to
judge (a few hundred sends per variant at least). Track: delivered, reply rate, positive
reply rate, meetings booked, meetings held, pipeline created. Reply rate beats open rate —
open tracking is unreliable due to privacy features in mail clients.

## Compliance
Honour opt-outs promptly, include sender identity and a postal address where required
(e.g. US CAN-SPAM), and check consent/legitimate-interest rules for your recipients'
country (GDPR in the EU/UK, CASL in Canada is stricter). Get legal sign-off on your basis.

## Gotchas
- Sending from the main domain at volume → company-wide deliverability problems.
- Merge-field failures ("Hi {{first_name}}") reaching prospects.
- Two reps sequencing the same contact — enable the platform's duplicate/ownership guard.
- Automated steps continuing after a reply in a different thread or channel; check sync with CRM.

## Verify
- [ ] SPF, DKIM and DMARC pass for the sending domain; mailboxes warmed with caps set.
- [ ] Bounce rate under a few percent and complaint rate tracked.
- [ ] Sequence exits on reply, meeting, bounce, unsubscribe; OOO pauses.
- [ ] Every template previewed against real records with fallbacks.
- [ ] Positive reply rate and meetings held reported weekly.
