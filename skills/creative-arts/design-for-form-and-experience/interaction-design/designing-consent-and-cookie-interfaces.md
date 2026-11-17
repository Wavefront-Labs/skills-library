---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-consent-and-cookie-interfaces
name: designing-consent-and-cookie-interfaces
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [consent-ui, cookie-banner, consent-management, privacy-consent-design, cookie-consent, gdpr-consent-ui]
level: practitioner
status: draft
description: "Design consent and cookie interfaces that are clear and fair: granular choices, equal prominence for accept and reject, plain language, and withdrawal as easy as giving."
sources:
  - "European Data Protection Board, Guidelines 05/2020 on consent under Regulation 2016/679 (edpb.europa.eu)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Consent and cookie interfaces

This is design guidance, not legal advice. Requirements differ by country and law (for example GDPR and ePrivacy rules in the EU and UK, and state laws in the US). Confirm requirements with your privacy counsel.

## Principles (as in EDPB consent guidelines under GDPR)
GDPR consent should be freely given, specific, informed and unambiguous, given by a clear affirmative action. In practice that means:
- **No pre-ticked boxes;** silence or inactivity is not consent.
- **Equal ease of accepting and rejecting:** a "Reject" option at the same level and with equal visual weight as "Accept".
- **Granularity:** separate purposes (analytics, marketing, personalisation) rather than one bundle; strictly necessary cookies need no consent under the ePrivacy rules, but check the specifics.
- **Informed:** say who is collecting, for what purpose, and for how long, in plain language, with a link to details.
- **Withdraw as easily as it was given:** a persistent link to preferences, which works in one or two steps.
- **No access conditioned on consent** unless necessary for the service (the so-called cookie wall is restricted in many places).

## Design
1. Layer the notice: a short banner, then detailed preferences.
2. Do not use misleading styles (a bright accept, a grey reject; see `...interaction-design.auditing-a-design-for-dark-patterns`).
3. Make the banner accessible: keyboard and screen reader operable, focus managed, not covering essential content (see `...interaction-design.designing-keyboard-operability-and-focus-order`).
4. Record consent (timestamp, version of text, choices) and respect it in code (do not load trackers before consent where required).
5. Re-ask only when things change, not on every visit.

## Verify
- [ ] Accept and reject require the same number of clicks.
- [ ] Nothing is pre-selected.
- [ ] Preferences can be changed from every page.
