---
id: computing-software.it-support-helpdesk.servicenow.inbound-email-actions-for-tickets
name: inbound-email-actions-for-tickets
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, inbound-email-actions, email-to-ticket, watermark, reply-matching, mail-loops, sys-email]
level: practitioner
status: gated
description: "Make ServiceNow email-to-ticket reliable: inbound action types, watermark reply matching, unknown senders, auto-reply loops, and diagnosing mail that never became a ticket."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/notification/concept/c_InboundEmailActions.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/notification/concept/c_WorkingWithWatermarks.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/notification/reference/r_EmailProperties.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inbound-email-actions-for-tickets

Email is still the biggest channel on many desks. Inbound email actions
(`sysevent_in_email_action`) decide whether a message creates a ticket, updates one, or is
ignored.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## How a message is classified
1. **Reply**: matched by watermark (`Ref:MSG0001234`) in subject/body, or `In-Reply-To`
   header, or record number prefix in the subject (e.g. `INC0012345`) if
   `glide.email.reply_subject_prefix` style matching is on. Reply actions update the record.
2. **Forward**: subject starts with a forward prefix (`FW:`, `Fwd:`); handled by forward
   actions, usually creating a new ticket.
3. **New**: neither of the above.

Actions run in **Order**; set *Stop processing* on the one that should win, or several may
fire.

## Base "Create Incident" pattern
- Target table incident, type New, condition on recipient (e.g. sent to servicedesk@).
- Script maps `email.subject` to short description, `email.body_text` to description,
  caller from `email.from` (sys_user lookup), contact type email.
- Attachments are copied automatically; inline images arrive as attachments too.

## Unknown senders
- `glide.user.trusted_domain` and "Automatically create users for incoming emails from
  trusted domains" control whether a new user is created. Off is safer: route unknown
  senders to a triage queue with caller = Guest and the address in description.

## Loops and noise
- Ignore auto-replies: condition `!email.headers.includes('Auto-Submitted: auto-replied')`
  and check `X-Auto-Response-Suppress`/`Precedence: bulk`.
- Instance notifications should carry `Auto-Submitted: auto-generated`, so other systems
  don't reply.
- Two systems mailing each other (vendor tool <-> ServiceNow) can create thousands of
  tickets. Add a sender exclusion and a rate check.

## Diagnose "my email never became a ticket"
1. System Mailboxes > Inbound > Received / Junk: find the message in `sys_email` by
   sender and time.
2. Open it: **Target** field and the email log show which action ran or "skipped".
3. Junk: the mail matched a spam/ignore rule (`glide.email.ignore.*`) or the sender is
   blocked in Email Filters.
4. Not there at all: check the mail flow (forwarding rule from Exchange, POP3/IMAP/OAuth
   account status in Email Accounts).

## Gotchas
- Watermarks stripped by the user's mail client or a security gateway turn replies into
  new tickets. Keep the record number in the subject as a second match key.
- HTML signatures and disclaimers bloat `description`; trim with `email.body_text` and a
  signature delimiter.

## Verify
Send test mails (new, reply with watermark, reply with only number in subject, forward,
auto-reply) and confirm each lands as intended in the email log.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
