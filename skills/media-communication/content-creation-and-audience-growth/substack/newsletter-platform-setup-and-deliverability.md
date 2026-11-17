---
id: media-communication.content-creation-and-audience-growth.substack.newsletter-platform-setup-and-deliverability
name: newsletter-platform-setup-and-deliverability
category: media-communication
field: content-creation-and-audience-growth
product: substack
tags: [substack, ghost, beehiiv, buttondown, newsletter, newsletter-platform, email-deliverability, spf, dkim, dmarc, custom-domain, recommendations, subscriber-import, platform-migration, spam-folder, gmail-promotions, double-opt-in, welcome-email, email-publishing, csv-export]
level: practitioner
status: docs-checked
description: "Set up a newsletter on a hosted platform and meet Gmail sender rules: SPF/DKIM/DMARC, one-click unsubscribe, spam rate, clean imports."
sources: ["https://support.google.com/mail/answer/81126"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Newsletter platform setup and deliverability

**Goal:** launch (or move) an email publication on a hosted platform (Substack, Ghost,
Beehiiv, Buttondown or similar) so that it reaches inboxes and keeps ownership of your
list. Growth tactics themselves: see
`media-communication.content-creation-and-audience-growth.newsletter-growth.signup-funnels-and-list-health`.

## 1. Choosing a platform
Compare discovery features, domain control and pricing on each vendor's current pages;
feature sets and prices change often, so none are restated here. Whatever you pick,
confirm you can **export subscribers as CSV** at any time and test it in week one; that is
your exit door.

## 2. Domain and authentication (the deliverability foundation)
Gmail's email sender guidelines (requirements in force from 1 February 2024):
- **All senders to Gmail:** SPF or DKIM authentication for the sending domain; valid
  forward and reverse DNS (PTR) records for sending IPs; a TLS connection; a spam rate
  below 0.3% in Postmaster Tools; messages formatted to RFC 5322; no impersonation of
  Gmail From: headers.
- **Senders of more than 5,000 messages a day to Gmail:** SPF and DKIM and DMARC (the DMARC
  policy may be `none`); the From: domain aligned with the SPF or DKIM domain; marketing and
  subscribed messages must support one-click unsubscribe (headers `List-Unsubscribe-Post:
  List-Unsubscribe=One-Click` and `List-Unsubscribe`) plus a visible unsubscribe link in the
  body.
- DKIM keys for personal Gmail must be 1024 bits or longer; 2048 bits is recommended.
- The SPF record must include every sender for the domain, including third-party senders
  such as your newsletter platform.
- If you use an email service provider, verify that it authenticates your domain with SPF and
  DKIM. A hosted platform sending under its own domain handles this for you; the DNS work
  is yours when you use a custom sending domain.

## 3. Launch setup checklist
1. Publication name, one-sentence pitch, about page, author bio.
2. Welcome email (automated) saying what is coming and how often.
3. Sending cadence decided and written on the signup page.
4. Confirm each address before subscribing it (Google's subscription guidance: make sure
   recipients opt in, confirm each address, periodically check they want to stay). Avoid
   opt-in forms that are checked by default.
5. Every message needs an easy way to unsubscribe.

## 4. Importing and migrating
- Import only people who opted in to you. Google's guidance: do not purchase email addresses
  and do not send to people who did not sign up; they mark messages as spam and future
  messages to them will be marked as spam.
- Migrating platforms: export subscribers (check how free and paid are exported), export posts,
  import, then set redirects from old post URLs where the platform allows. Paid-subscription
  moves are platform specific; follow both platforms' migration docs.

## 5. Staying out of spam
- Warm up: increase sending volume slowly, send at a consistent rate, start with engaged
  subscribers, and avoid sudden spikes such as suddenly doubling previous volume.
- Keep the Postmaster Tools spam rate below 0.10% and never reach 0.30% or higher.
- Google suggests considering unsubscribing recipients who do not open or read your messages
  (note Google does not track open rates and cannot verify third-party open rates).
- Do not hide content with HTML/CSS, keep links visible and understandable, and keep sender
  display names to the sender's identity (no subject text in the display name).
- Check regularly that your domain is not flagged in Google Safe Browsing.

## Verify
- [ ] A test email to a Gmail account lands in the inbox, not spam.
- [ ] Gmail "Show original" shows SPF, DKIM and DMARC all **PASS** (custom domain).
- [ ] Subscriber CSV export downloaded and opens correctly.
- [ ] Welcome email fires on a fresh test signup.
- [ ] After a migration, three old post URLs resolve to the new location.

## Checked

Date: 2026-11-09.

Confirmed on the Gmail email sender guidelines page (support.google.com/mail/answer/81126, reached from the cited Workspace URL): all items in section 2, the 0.10% and 0.30% spam-rate figures, the 5,000-message threshold, one-click unsubscribe headers, DKIM key length, subscription and importing guidance, warm-up guidance, display-name and hidden-content guidance, Safe Browsing check, and that Google does not track open rates. Removed because not stated there or on other pages read: the platform comparison table and rules of thumb, Yahoo requirements, the one-SPF-record rule, the DMARC record syntax example, Substack export format and Stripe migration notes, recommendation-network advice, the 20,000-email example and the 6-month re-permission and 90-180 day pruning figures. The Substack and Ghost help landing pages could not be used as sources and were dropped.

Method: documentation only; no commands were run.
