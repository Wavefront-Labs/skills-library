---
id: sales-marketing.real-estate-sales-leasing.real-estate-crm.pipeline-stages-and-drip-campaigns
name: pipeline-stages-and-drip-campaigns
category: sales-marketing
field: real-estate-sales-leasing
product: real-estate-crm
tags: [real-estate-crm, crm, follow-up-boss, kvcore, boldtrail, lofty, chime, agentbox, rex, vaultre, pipeline, pipeline-stages, lead-routing, smart-lists, action-plans, drip-campaign, nurture, past-client-nurture, appraisal-to-listing, conversion-rate, tags, data-hygiene, sms-consent, email-marketing, real-estate-agent]
level: practitioner
status: draft
description: "Run an agent's pipeline in a real-estate CRM such as Follow Up Boss or kvCORE: stages, tags and smart lists, lead routing, drip and nurture campaigns, and appraisal-to-listing tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pipeline stages and drip campaigns in a real-estate CRM

**Goal:** every lead and past client sits in the right stage, gets the right
follow-up automatically, and surfaces for a personal call at the right moment.
Common systems: **Follow Up Boss**, **kvCORE/BoldTrail**, **Lofty (Chime)** in the
US; **AgentBox, Rex, VaultRE** in Australia; many agency-supplied CRMs.
**Status draft:** feature names below follow Follow Up Boss-style concepts
(stages, smart lists, action plans) — map to your system's equivalents.

## 1. Define stages (keep them few)
Example set:
- **Lead** — new, uncontacted.
- **Attempted contact**.
- **Active — buyer** / **Active — seller (appraisal booked/done)**.
- **Nurture** — real but 3+ months away.
- **Under contract / listed**.
- **Closed / Past client**.
- **Trash / not a lead** (with reason).
Each stage has a definition and a "next action" rule, written down so the team
uses them the same way.

## 2. Tags and custom fields
- Source (portal, open home, farm, referral, SOI) — required for ROI.
- Buyer criteria: price range, suburbs/areas, beds — enables matching new listings.
- Seller: property address, estimated value, timeframe, appraisal date.
- Key dates: purchase anniversary, birthday, lease expiry (investors).
Avoid tag sprawl: a fixed tag list, reviewed quarterly.

## 3. Lead intake and routing
- Connect portals, website forms, open-home sign-in apps and ad lead forms so leads
  arrive automatically (email parsing or native integrations).
- Route to the right agent (round robin, by area, by price); set response alerts.
- Speed-to-lead target: first call within 5–15 minutes in business hours;
  auto-text acknowledgement after hours where consent rules allow.

## 4. Smart lists = your daily call list
Build saved filters that drive daily work, e.g.:
- New leads not yet called.
- Active buyers not contacted in 7 days.
- Nurture contacts not contacted in 30 days.
- Appraisals done, no listing decision, last contact > 14 days.
- Past clients with purchase anniversary this month.
Work them top to bottom every day; log each call outcome.

## 5. Drip/action plans
- **New buyer lead**: day 0 text + email, day 1 call, day 3 email with listings
  matching criteria, day 7 call, then weekly listing alerts for 4 weeks, then move
  to nurture.
- **Appraisal follow-up**: thank-you + CMA summary day 0, call day 3, market
  update day 14, new comparable sales as they happen, monthly call.
- **Past client nurture**: monthly market email, quarterly call, anniversary
  message with home-value estimate, annual check-in.
Write messages that sound personal and give useful information; pause automation
as soon as the person replies (most CRMs can do this).

## 6. Appraisal-to-listing tracking
Report monthly: appraisals done → listings won (conversion %), listings won by
source, average days from appraisal to listing, lost-to-competitor reasons.
Low conversion with plenty of appraisals = presentation or pricing problem
(see cma-and-listing-presentation).

## 7. Consent and hygiene
- Record consent for email and especially SMS marketing (e.g. US TCPA, Australian
  Spam Act, UK PECR/GDPR); include unsubscribe in every marketing message.
- Merge duplicates weekly; fix bounced emails; archive dead leads with reason.

## Gotchas
- Too many stages → nobody updates them.
- Drips that never stop after the contact replies look robotic.
- Importing contacts without consent for marketing.
- Measuring leads instead of appointments and listings.

## Verify
- [ ] Stages defined in writing with next-action rules.
- [ ] Every contact has source and stage; tag list controlled.
- [ ] Leads route automatically with response alerts.
- [ ] Smart lists drive a daily call plan; outcomes logged.
- [ ] Action plans pause on reply; consent recorded; monthly appraisal-to-listing report.
