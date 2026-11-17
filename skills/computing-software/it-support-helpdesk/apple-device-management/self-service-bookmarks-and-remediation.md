---
id: computing-software.it-support-helpdesk.apple-device-management.self-service-bookmarks-and-remediation
name: self-service-bookmarks-and-remediation
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-self-service, self-service-bookmarks-and-remediation, self-service-remediation, user-self-help]
level: practitioner
status: draft
description: "Use Self Service policies for common repairs such as printer installs, VPN reinstall and cache resets, with confirmation prompts and reboot options."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Self_Service.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# self-service-bookmarks-and-remediation

Goal: let users fix common issues themselves.
- Create a policy with a script (flush DNS, reset printing, rebuild Spotlight), set Self Service, and add a user message before and after.
- Options: Require restart, "Install on login" and a user logout prompt.
- Use Bookmarks for web links such as IT portal pages.
- Add a Self Service plug-in `jamfHelper` prompt for confirmation: `/Library/Application\ Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper -windowType utility -description "Continue?" -button1 Yes`.
Practice: Include a clear completion message and a log line for each fix so the helpdesk can tell whether the user already tried it before raising a ticket.
Gotcha: scripts triggered from Self Service run as root without a logged-in user context; use `$3` and `stat /dev/console` for the user.
Verify:
- Fix runs from Self Service on a test Mac.
- Policy log shows Completed with the user recorded.
