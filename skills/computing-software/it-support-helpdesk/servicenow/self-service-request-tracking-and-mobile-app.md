---
id: computing-software.it-support-helpdesk.servicenow.self-service-request-tracking-and-mobile-app
name: self-service-request-tracking-and-mobile-app
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, my-requests-tracking, mobile-self-service, service-portal, now-mobile, notifications]
level: practitioner
status: gated
description: "Help users track their requests and incidents on the portal and Now Mobile app, and tune notifications so updates reach them without driving status-chasing calls."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/build/service-portal/concept/c_ServicePortal.html"
  - "https://www.servicenow.com/docs/bundle/zurich-mobile/page/administer/tablet-mobile-ui/concept/now-mobile-app.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/notification/concept/c_EmailNotifications.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# self-service-request-tracking-and-mobile-app

"Any update on my ticket?" calls are a symptom: users can't see status or don't trust it.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Portal: My Requests / My Tickets
- Employee Center / Service Portal list shows the user's open incidents and RITMs with
  state, stage progress and last update. Make sure:
  - Additional comments (customer-visible) are used for updates; work notes don't show.
  - RITM stages are configured so progress isn't stuck on "Fulfilment" for a week.
  - Users can comment, attach files, and resolve/reopen from the ticket page.
- Watch lists: users can add colleagues; managers can see requests they approved.

## Now Mobile app
- Users install **Now Mobile** (employee) and sign in with the instance URL or QR code;
  SSO via the IdP. Admins publish the app config (catalog, ticket list, knowledge).
- Push notifications for state changes and comments replace some emails; configure them
  under the mobile push notification settings.
- Mobile catalog items need mobile-friendly variables (avoid complex UI policies/client
  scripts that only work on desktop; test each item on a phone).
- Support: "can't log in to the app" is usually the wrong instance URL, SSO not enabled
  for mobile, or MDM app protection blocking; check the app is allowed in the MAM policy.

## Notifications that reduce chasing
- On assignment: who has it and expected next step.
- On every customer-visible comment, with a reply-to that updates the ticket.
- On hold/awaiting caller: what you need and by when, with auto-close date.
- Don't send on every internal field change.

## Measure
Track contacts that are status chases (category or a "status request" contact reason).
Falling numbers after portal/mobile improvements show it worked.

## Verify
A test user can see an open request's stage and last comment on portal and mobile, reply
from email, and receives one notification per meaningful change.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
