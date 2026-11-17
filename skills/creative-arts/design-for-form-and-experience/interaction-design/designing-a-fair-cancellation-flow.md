---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-a-fair-cancellation-flow
name: designing-a-fair-cancellation-flow
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [cancellation-flow, subscription-cancellation, unsubscribe-flow, click-to-cancel, roach-motel, retention-ethics]
level: practitioner
status: draft
description: "Design a fair cancellation flow: cancel in the same channel as signing up, a few clear steps, honest retention offers, confirmation, and legal points to check."
sources:
  - "Interaction Design Foundation literature (interaction-design.org/literature)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fair cancellation flows

Cancelling a subscription should be as easy as starting one. Hard cancellations are a recognised dark pattern (roach motel; see `...interaction-design.auditing-a-design-for-dark-patterns`) and can attract regulator action and complaints.

## Legal context
Rules on subscription cancellation differ by country and change over time (the United States has a federal law on online negative option marketing and state auto-renewal laws, and the status of FTC "click to cancel" rulemaking has changed, so check current status; the EU and UK also have consumer rules). This skill does not state the current law; involve counsel.

## Design principles
1. **Same channel:** if sign-up is online, cancel online without a phone call or chat with an agent.
2. **Findable:** a clear "Cancel subscription" link in account or billing settings, not hidden in help text.
3. **Few steps:** ideally one or two screens: confirm identity if needed, confirm cancellation, show the end date.
4. **Honest retention:** one optional offer (pause, downgrade, discount) with an equally clear "Continue to cancel" button; no confirmshaming and no repeated prompts.
5. **Clarity:** explain what happens to data, billing end date and any refund, and if access continues until the period ends.
6. **Confirmation:** on-screen and by email, with a way to reverse (resume) if appropriate.
7. **Reason survey** optional and skippable.
8. **Accessible:** keyboard, labels, plain language.

## Test
Time-to-cancel in usability tests with new users; compare with time-to-subscribe; track cancellation completion and complaint volume.

## Verify
- [ ] A new user can cancel in under two minutes unaided.
- [ ] No step blocks the path with a forced call or hidden link.
- [ ] Confirmation states the end date and data handling.
