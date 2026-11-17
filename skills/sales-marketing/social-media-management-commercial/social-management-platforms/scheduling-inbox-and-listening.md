---
id: sales-marketing.social-media-management-commercial.social-management-platforms.scheduling-inbox-and-listening
name: scheduling-inbox-and-listening
category: sales-marketing
field: social-media-management-commercial
product: social-management-platforms
tags: [social-management-platforms, hootsuite, sprout-social, buffer, later, agorapulse, meta-business-suite, social-media-scheduling, multi-account-scheduling, unified-inbox, smart-inbox, social-listening, keyword-queries, boolean-search, social-reporting, approval-workflows, user-permissions, social-media-management, utm-parameters]
level: practitioner
status: draft
description: "Run the social stack (Hootsuite, Sprout Social, Buffer, Later): connect accounts safely, schedule with approvals, triage a unified inbox, build listening queries and a monthly report."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scheduling, unified inbox and listening

**Goal:** one place to plan, approve, publish, answer and measure across every brand
account, with access controlled so nobody can post as the brand by accident.

**Note:** feature sets, plan tiers and menu names change frequently across Hootsuite, Sprout
Social, Buffer, Later, Agorapulse and the native Meta Business Suite; listening, approvals
and advanced reporting are usually on higher tiers. Confirm on the vendor's current plan page.

## 1. Connect accounts properly
- Connect business/creator accounts, not personal ones: Instagram must be a professional
  account linked to a Facebook Page for most third-party publishing; LinkedIn company pages
  need a page admin to authorise.
- Connect using a **brand-owned admin login** where possible, so access survives staff
  changes. Re-authorise when tokens expire (tools usually email a warning).
- **Roles:** give each user least privilege — e.g. contributors can draft, only approvers
  can publish. Turn on two-factor authentication on the tool and every connected platform.

## 2. Scheduling workflow
1. Draft in the tool from the content calendar (see
   sales-marketing.social-media-management-commercial.content-calendar-planning.pillars-cadence-and-calendar).
2. Customise per network: caption length, hashtags, first comment, aspect ratio, alt text.
3. Add **UTM parameters** to links so web analytics attribute traffic, e.g.
   `?utm_source=instagram&utm_medium=social&utm_campaign=autumn_launch` (most tools can
   auto-append).
4. Submit for **approval**; approver checks spelling, links, claims, tags, timing.
5. Schedule at your audience's peak time (tools suggest times; your own data wins).
6. Preview on mobile before publishing.
Keep a **pause all** procedure: know where to pause the queue in a crisis.

## 3. Unified inbox
- Pull comments, mentions and DMs from all networks into one stream.
- Set **rules/tags**: auto-tag messages containing "refund", "broken", "order" as
  complaints; route to the right person; mark complete when handled.
- Use saved replies as templates, personalised every time.
- Track response time and volume in the inbox report.
Some message types (e.g. certain DMs or ad comments) may not sync via APIs — check
natively on each platform daily.

## 4. Social listening queries
Build Boolean queries for brand, products, competitors, and category:
```
("Acme Coffee" OR "acmecoffee" OR @acmecoffee OR #acmecoffee)
  AND NOT ("acme coffee table" OR jobs OR hiring)
```
- Include misspellings and product names; exclude ambiguous meanings.
- Watch: mention volume, sentiment (spot-check — automatic sentiment misreads sarcasm),
  top themes, spikes. Set alerts for spikes over normal volume.
- Data coverage varies by network (some platforms restrict API access), so listening is
  a sample, not a census.

## 5. Monthly report (one page)
- Per network: followers growth, reach/impressions, engagement rate, top 3 posts, link clicks
  (from UTMs in web analytics), conversions/revenue where tracked.
- Inbox: volume, median response time, complaint themes.
- Listening: share of voice vs competitors, notable spikes.
- **So what:** three actions for next month.

## Gotchas
- Scheduled posts don't stop themselves during breaking news — someone must check.
- Third-party publishing can't use every native feature (some music, stickers, collabs);
  publish natively when needed.
- Disconnected accounts silently fail to post — check the tool's failed-posts view daily.
- Sentiment scores are approximate; never report them without manual checks.

## Verify
- [ ] All accounts connected via brand-owned admin access with 2FA.
- [ ] Roles enforce draft vs publish permissions; approvals on.
- [ ] Every link carries UTM parameters.
- [ ] Inbox rules route complaints; response time measured.
- [ ] Listening queries tested for false positives; spike alerts set.
- [ ] Monthly report ends with three actions.
