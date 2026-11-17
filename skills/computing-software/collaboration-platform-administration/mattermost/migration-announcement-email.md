---
id: computing-software.collaboration-platform-administration.mattermost.migration-announcement-email
name: migration-announcement-email
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [migration-announcement, end-user-communication, password-reset, onboarding]
level: intro
status: docs-checked
description: "Template email telling users you moved to Mattermost: password reset by email, login, app download and where to ask questions."
sources: ["https://docs.mattermost.com/administration-guide/onboard/migration-announcement-email.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migration announcement email

The documentation provides a sample email for telling end users about a move to Mattermost. Replace every bold item with your details: the old system name, the Mattermost URL, the support channel and support email, and the sign-off.

Template content:
- To: End users. Subject: Moving to Mattermost.
- Opening: we are moving from the old system to Mattermost as the collaboration platform, and existing users and data have been imported so communication, file sharing and collaboration can continue.
- Getting started, in four steps:
  1. Open a browser, go to the Mattermost URL and select "I forgot my password" to set a new password, using the email address from the previous system.
  2. After resetting, log in with the email and the new password.
  3. Download the Mattermost desktop and mobile apps, and read the end user documentation for a quick start.
  4. Bookmark the URL for next time.
- Questions: post in your support channel or email the support address, then a friendly sign-off.

Send the message when the cut-over is complete and the server is verified, and mention the support contact prominently so first-day issues reach one place.

## Checked

Confirmed against the Migration announcement email page: the template fields, subject and the four getting-started steps. Removed the claim that imported accounts do not carry the old password, which the page does not state.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/migration-announcement-email page (source rst from the mattermost/docs repo).
