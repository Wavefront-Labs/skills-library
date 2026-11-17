---
id: computing-software.it-support-helpdesk.apple-device-management.self-service-branding-and-categories
name: self-service-branding-and-categories
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-self-service, self-service-branding-and-categories, self-service, branding]
level: practitioner
status: draft
description: "Configure Self Service branding, categories and featured items so staff find approved apps and fixes without raising tickets."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Self_Service.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# self-service-branding-and-categories

Goal: give users a clear app store.
- Settings > Self Service > Branding: icon, name, banner; Categories group items; Featured highlights popular.
- Policy > Self Service tab: make available, add display name, description, icon, category.
- Self Service+ (macOS) adds a modern UI and Notifications (confirm feature set).
- Require login via SSO under Settings > Self Service > Login.
- Use consistent icons from the app bundle.
Practice: Review the most requested tickets quarterly and publish matching items, so Self Service steadily replaces repeat requests and lowers helpdesk load.
Gotcha: items disappear for users out of scope; empty Self Service usually means smart group scope rather than a broken app.
Verify:
- A test user in scope sees the item.
- Branding appears after relaunching Self Service.
