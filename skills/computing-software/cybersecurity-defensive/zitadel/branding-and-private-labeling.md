---
id: computing-software.cybersecurity-defensive.zitadel.branding-and-private-labeling
name: branding-and-private-labeling
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, branding, private-labeling, login-ui, theming]
level: practitioner
status: docs-checked
description: "Brand ZITADEL's login and emails per instance or organization, and trigger an organization's branding with a domain scope or project setting."
sources:
  - https://zitadel.com/docs/guides/manage/customize/branding
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Branding can be set on the instance, as the default for all organizations, or on an organization. You customize light and dark themes separately and see a live preview. Click Apply settings for it to take effect on the login and on emails.

Settings:

- Logo for the chosen theme and an icon for smaller components such as the console home button
- Four colors: background, primary (buttons, links, highlights), warn (errors and warnings) and font color
- A font, best uploaded as a ttf file; it appears in the font part but not in the preview
- Advanced behavior: hide the login name suffix (domain) on the login page, and disable the "Powered by ZITADEL" watermark

To make an application show an organization's branding, either send the Organization Domain scope in the authorization request, which also restricts login to that organization's users, or set the private labeling option on the project to define which branding triggers.

The OIDC authentication request playground lets you try organization policies and branding.

Reset policy removes the organization's customization so the system defaults apply again.

## Checked

2026-11-08. Read in full: the brand customization page; the default settings page was used for the icon setting. All claims confirmed.

Method: documentation only; no commands were run.
