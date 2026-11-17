---
id: computing-software.general-digital-literacy.email-clients.managing-email-and-calendar
name: managing-email-and-calendar
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email, calendar, gmail, outlook, outlook-com, apple-mail, thunderbird, google-calendar, compose, reply-all, bcc, cc, attachments, filters, rules, labels, folders, archive, search-operators, undo-send, calendar-invites, time-zones, scheduling, phishing, inbox-zero]
level: intro
status: docs-checked
description: "Write clear email, handle attachments and Reply All safely, organise with archive/labels/filters, search fast, send calendar invites, spot phishing."
sources:
  - https://support.google.com/mail/answer/1284885
  - https://support.google.com/mail/answer/7190
  - https://support.google.com/mail/answer/6579
  - https://support.google.com/mail/answer/6584
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing email and calendar — clear messages, a controllable inbox, invites that work

**Goal:** send email people act on, keep the inbox manageable with rules instead of
willpower, and schedule meetings without time-zone mistakes. Product-specific steps
below are for Gmail; for Outlook, Apple Mail or Thunderbird, look up the equivalent in
that product's own help.

## 1. Writing a message that gets acted on
- **Subject = the ask + any deadline:** `Approve Q3 budget by Fri 17 Oct`, not `Budget`.
- First line states the request; context after. One topic per email so replies don't
  fork. Use bullets for multiple questions so each can be answered.
- **To** = people who must act; **Cc** = people who need to know; **Bcc** = recipients
  who must not see each other (e.g. an announcement to an external list).
- **Reply All** only when everyone on the thread needs your answer. Remove people as a
  thread narrows; add a note ("moving Sam to Bcc").
- Turn on **Undo Send**. In Gmail on a computer: Settings › See all settings › Undo Send,
  choose a cancellation window of 5, 10, 20 or 30 seconds, then Save changes.
- Write the email *before* adding recipients for anything sensitive, so an early Enter
  can't send a half-draft.

## 2. Attachments
- Gmail's attachment limit is 25 MB on personal accounts (Workspace admins set it for
  work and school accounts). Above it, Gmail removes the attachments and inserts a
  Google Drive link. For large or frequently-updated files, **share a cloud link** with
  the right permission instead of attaching a copy.
- Say in the body what is attached and name the file meaningfully
  (`2026-10-14_invoice_0042.pdf`).
- Send PDFs for anything that should not be edited.

## 3. Keeping the inbox under control
- Process each message once: do it (<2 min), schedule it, delegate it, or archive it.
- **Filters** do the sorting. Gmail on a computer: click the search options icon in the
  search box, enter criteria, click Create filter, choose the action (the page lists
  applying a label, archiving, deleting, starring and forwarding), then Create filter.
  Typical: newsletters get a "Read later" label and are archived.
- Keep the number of labels or folders small; search beats elaborate filing.
- Unsubscribe with the mail client's own unsubscribe option rather than links in
  suspicious mail.

## 4. Search operators that save hours
- Gmail: `from:`, `has:attachment`, `larger:`, `older_than:`, `subject:`, `filename:`,
  `is:unread` and `before:` are all documented operators, e.g.
  `from:alex has:attachment larger:10M older_than:1y`. `before:` takes `2026/01/01`
  (year/month/day) or `01/31/2026` (month/day/year). Large-attachment searches are the
  fastest way to free storage.
- Other products use different syntax: check their search help.

## 5. Calendar invites
- Create the event in the calendar and **add guests there**; don't send a plain email
  saying "let's meet at 3".
- Always check the **time zone** when typing a time for someone abroad, and spell out
  zones in the text too ("15:00 London / 10:00 New York").
- Add the video link, agenda and any document link **in the invite**. Edit the event
  itself to change it — forwarding an invite or sending a second one creates duplicates.
- Reply Yes / No / Maybe so the organiser's count is accurate.

## 6. Phishing check before you click
Look at the real sender address (not just the display name), hover over links to see
the true destination, and be suspicious of urgency, payment changes and login prompts.
When in doubt, go to the site by typing its address, or call the sender on a known number.

## Verify
- [ ] Subjects state the ask; the request is in the first line.
- [ ] Undo Send is enabled; Reply All used deliberately.
- [ ] Large files go as links with checked permissions.
- [ ] At least one filter routes recurring mail out of the inbox.
- [ ] Meetings are sent as calendar invites with time zone, link and agenda inside.

## Checked
2026-11-01. Confirmed from Gmail Help: Undo Send path and 5/10/20/30 s windows,
search operators and `before:` formats, filter steps and actions, 25 MB limit with
Drive link. Removed: Outlook settings and limits, recall, keyboard shortcuts, Outlook
operators, the Bcc reply-all aside, scheduling-assistant and Find-a-time claims,
label-count figure, and Google Calendar specifics.
Method: documentation only; no commands were run.
