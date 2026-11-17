---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-self-service-catalogue
name: jamf-self-service-catalogue
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf, jamf-pro, jamf-self-service, self-service-plus, ticket-deflection, macos-app-catalogue, bookmarks, macos-management]
level: practitioner
status: draft
description: "Run Jamf Self Service as the Mac app store and fix-it portal: making policies available, categories and featured items, user-run fixes, notifications, and deflecting tickets."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Jamf_Self_Service_for_macOS.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Self_Service_Configuration_Settings.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policy_Management.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-self-service-catalogue

Goal: Mac users install approved apps and run common fixes themselves,
without admin rights or a ticket.

## Publishing an item
Policy → Self Service tab → "Make the policy available in Self Service":
- Display name, button text ("Install", "Fix"), description written for
  users (what it does, how long, whether it restarts).
- Icon, **categories**, **Feature** on main page.
- "Ensure that users view the description" for disruptive items.
- Execution frequency usually **Ongoing** so users can re-run.
- Scope to the groups who should see it (Self Service shows only in-scope
  items).

## Good catalogue items for support
| Item | Payload |
|---|---|
| Approved apps (Zoom, Slack, VS Code) | Package or Installomator script |
| "Fix printing" | script: reset printing system + re-add printers |
| "Reset Teams / Outlook cache" | script, user-context |
| "Update inventory" | Maintenance → Update inventory |
| "Get temporary admin" (if policy allows) | privileges script with timeout and logging |
| Fonts, printers, VPN profile | Printers / configuration profile payload |
| OS update nudge | link to Software Update or erase-install workflow |
Configuration profiles can also be made available in Self Service.

## Configuration
Settings → Self Service → macOS: branding, login (SSO) requirements, install
automatically, notifications (Self Service or Notification Center), URL
scheme (`jamfselfservice://content?entity=policy&id=123&action=execute`) —
put these links in KB articles and ticket replies.

## Measure deflection
Policy logs per Self Service item = uses; compare with ticket categories
for the same issue before/after publishing.

## Gotchas
- User-context scripts need to run as the logged-in user — Self Service
  policies still run as root; handle with `launchctl asuser`.
- Items that require a restart without warning generate angry tickets.
- Keep the catalogue curated — stale versions erode trust.

## Verify
A standard user sees the item, runs it, and the policy log shows Completed;
the matching ticket category volume drops over the following month.
