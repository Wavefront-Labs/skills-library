---
id: computing-software.general-digital-literacy.email-clients.adding-a-video-meeting-link-to-an-event
name: adding-a-video-meeting-link-to-an-event
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, calendar, add-meeting-link, teams-meeting, google-meet]
level: intro
status: docs-checked
description: "Add a Teams or Google Meet link to a calendar invite, make it the default for new events, and avoid duplicate or wrong meeting links."
sources:
  - https://support.microsoft.com/en-us/outlook/make-every-meeting-online
  - https://support.google.com/calendar/answer/9896550
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Add a video meeting link to an event

## Outlook (Microsoft 365 accounts only)
- New Outlook: Settings > Calendar > Events and invitations > tick **Add online meeting to all meetings**, choose a meeting provider from the list, then Save. The option is on by default if you have a Teams license.
- Classic Outlook for Windows: File > Options > Calendar > under Calendar options go to **Add online meeting to all meetings**, select Add Meeting Provider, tick the box, pick the account and the default provider.
- The setting applies to Microsoft 365 accounts only.

## Google Calendar (web)
- Create an event or open one you can edit, find the conferencing field and click **Add Google Meet video conferencing**, then Save. Click **Remove** to take it off.
- A conferencing add-on from the Google Workspace Marketplace appears in the **Add conferencing** drop-down. Work or school admins control which add-ons are available.
- To add Meet to every event you create: Settings > Event settings > turn on **Automatically add Google Meet video conferences to events I create**.
- The Meet code stays linked to the original event until it expires, and that event's guest list controls who can join and who sees recordings and chat history.

## Gotchas
- An event can have only one conference. Pasting conference details into the location or description, or using a browser extension, can leave several conferences on one event.

## Verify
- [ ] Open the saved event: one join link is shown and the guest list is correct.

## Checked
2026-10-27. Microsoft Support "Make every meeting online" and Google Calendar Help "Add or remove a video conference" (current pages). Confirmed: Outlook setting names and paths, Microsoft 365-only limit, Meet add and auto-add settings, one conference per event. Removed unconfirmed Zoom, Apple Calendar and copied-event claims.
Method: documentation only; no commands were run.
