---
id: computing-software.it-support-helpdesk.user-support-communication.writing-support-emails-and-ticket-updates
name: writing-support-emails-and-ticket-updates
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, email-support, written-communication, support-email-writing, ticket-updates, bluf, next-steps, customer-updates]
level: intro
status: draft
description: "Write support emails and ticket updates users act on: answer first, one ask per message, numbered steps, explicit next update time, and subject lines that keep the ticket thread."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.plainlanguage.gov/guidelines/"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# writing-support-emails-and-ticket-updates

Goal: the user knows, in the first two lines, what's happening and what (if
anything) they need to do — and replies land back on the ticket.

## Structure (BLUF — bottom line up front)
1. **Status/answer** in the first sentence: "Your laptop is fixed and ready
   to collect from the IT desk." / "We need one thing from you to continue."
2. **What you need from them** (one ask; if several, numbered).
3. **What happens next and when**: "I'll update you by 3 pm tomorrow,
   even if there's no change."
4. Short context/details for those who want it.
5. Ticket number and how to reply.

## Example update
> Subject: INC0012345 – Outlook not syncing – waiting on you
>
> Hi Sam, we've found the cause: your mailbox is full (50 GB of 50 GB).
>
> **Could you** delete or archive older mail so it's under 45 GB? The
> steps are below and take about 10 minutes.
>
> 1. In Outlook, open File → Tools → Mailbox Cleanup.
> 2. Click "Find items larger than" 5000 KB and delete what you don't need.
> 3. Empty Deleted Items.
>
> I'll check the mailbox size at 2 pm tomorrow. If you'd rather we move
> mail to your online archive for you, just reply "archive".
>
> Ticket INC0012345 – reply to this email to update it.

## Rules
- Keep the ticket number in the subject, reply from the ITSM tool (not
  personal mailbox) so the thread stays attached.
- One topic per email; separate issues get separate tickets.
- Plain language — define unavoidable terms once.
- Bold the ask, not random words. No walls of text; < 150 words for most
  updates.
- Don't say "should be fixed" — say what you tested.
- Pending-user tickets: state the auto-close policy politely ("If I don't
  hear back by Friday I'll close this; reply any time to reopen").

## Gotchas
- Don't paste passwords, recovery keys or sensitive data into email.
- Reply-all chains with managers copied: keep the same tone and facts as a
  direct message; never blame the user.
- Timezones: give times with zone for distributed users.

## Verify
Reread as the user: can they act without replying "what do you mean?"
Track it — fewer clarification replies and faster user responses per ticket.
