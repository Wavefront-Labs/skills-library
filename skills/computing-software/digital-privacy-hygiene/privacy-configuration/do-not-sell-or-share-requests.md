---
id: computing-software.digital-privacy-hygiene.privacy-configuration.do-not-sell-or-share-requests
name: do-not-sell-or-share-requests
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, do-not-sell, ccpa, global-privacy-control]
level: practitioner
status: docs-checked
description: "Use Do Not Sell or Share links, Global Privacy Control and authorised agents to opt out of sale and cross-context ad sharing under the CCPA, per the California AG."
sources:
  - "https://oag.ca.gov/privacy/ccpa"
  - "https://cppa.ca.gov/regulations/"
  - "https://globalprivacycontrol.org/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Do not sell or share requests

**Goal:** tell businesses to stop selling or sharing your personal information for cross-context behavioural
advertising, using the right the California Consumer Privacy Act (CCPA, as amended by the CPRA) gives you.

## What the right covers
You may ask a business to stop **selling** or **sharing** your personal information. "Sharing" means sharing for
cross-context behavioural advertising: targeting ads from your activity across many websites. After an opt-out, the
business generally cannot sell or share your data unless you later authorise it, and must wait at least 12 months
before asking you to opt back in. Similar opt-out rights exist in other US state laws; check the state's regulator for
the rules that apply to you, because this skill only covers California.

## How to opt out
1. A business that sells or shares personal information must show a clear and conspicuous "Do Not Sell or Share My
   Personal Information" link on its website. If you cannot find it, look in the privacy policy, where the link must
   also appear if the business sells or shares.
2. The business cannot make you create an account to opt out and should not require identity verification, though it
   may ask basic questions to match you to records. Information it asks for may be used only for that purpose.
3. It must respond as soon as feasible, up to a maximum of 15 business days from receipt.
4. If the link or method is broken or hard to find, you can report the business to the California Attorney General
   (oag.ca.gov consumer complaint form).

## Do it once for many sites: Global Privacy Control
GPC is a browser or extension setting that sends an opt-out signal to every site you visit. The California AG says that
for businesses collecting personal information online a user-enabled signal like GPC is an acceptable opt-out method
and must be honoured as a valid request to stop sale or sharing. The GPC site says Brave and DuckDuckGo send it on by
default and Firefox offers it in settings; extensions include Privacy Badger and OptMeowt. GPC was adopted as a work
item of the W3C Privacy Working Group in November 2024 and is still being standardised.

## Authorised agents
You may authorise another person, or a business registered with the California Secretary of State, to submit a CCPA
request. The business may ask the agent for proof of your signed permission, or ask you to verify directly or confirm
the permission.

## Limits and gotchas
- A GPC signal applies to the browser or device that sends it.
- Service providers acting for a business may refuse an opt-out sent to them; send it to the business itself.
- Exceptions exist (legal obligations, publicly available information, some medical and credit reporting data).
  If a request is refused, ask the business for its reasons.
- Businesses may sell the data of a consumer they know is under 16 only with opt-in: from the parent for under 13,
  from the child for 13 to 15.
- CalPrivacy (the California Privacy Protection Agency) now publishes the CCPA regulations and is exploring
  opt-out preference signal rules; check its regulations page for the current text.

## Checked
Checked 2026-11-08 against the California Attorney General CCPA page (opt-out FAQs B1 to B8, authorised agent FAQ),
the CalPrivacy regulations page and the Global Privacy Control home page. Removed: the list of other states, the
"Your Privacy Choices" wording, the claim that other states treat GPC as valid, the mobile ad ID and loyalty-portal
tips, and the claim that signed-in opt-outs apply to the account, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
