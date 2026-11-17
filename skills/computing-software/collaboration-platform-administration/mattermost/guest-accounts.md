---
id: computing-software.collaboration-platform-administration.mattermost.guest-accounts
name: guest-accounts
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [guest-accounts, guest-access, magic-link, single-channel-guest]
level: practitioner
status: docs-checked
description: "Enable and manage Mattermost guest accounts: capabilities, magic link, LDAP and SAML guest filters, promote and demote, deactivation and billing."
sources: ["https://docs.mattermost.com/administration-guide/onboard/guest-accounts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Guest accounts

Guest accounts let outsiders such as vendors and contractors collaborate with controlled access to channels and people. A system admin must first enable guest access (System Console > Authentication > Guest Access, Enable Guest Access). By default only system admins can invite guests; Enterprise and Professional customers can delegate that through permissions. Guests carry a GUEST badge, and channels containing guests show "This channel has guests" in the header.

Guests can pin messages, use non-restricted slash commands, favourite and mute channels, update their profile, use different authentication methods, and leave channels they were added to. They cannot discover public channels, join open teams, DM or group-message people outside their shared channels, invite people, or create channel checklists.

Authentication: email invitation plus AD/LDAP, SAML 2.0, or (from v11.3) magic link passwordless login. For magic links, enable passwordless authentication for guests via email in Guest Access and save; the emailed link expires in 48 hours. For LDAP, fill the Guest Filter under AD/LDAP > User Filters > additional filters. For SAML, fill the Guest Attribute. Removing the guest role in the identity system does not auto-promote them; promote manually.

Roles: System Console > User Management > Users offers Demote to Guest (keeps existing memberships, restricts discovery) and Promote to Member. Filter by Guests (all), in a single channel, or in multiple channels.

Disable: set Enable Guest Access to false, or deactivate a single guest; guests are marked deactivated, logged out and sessions revoked. Re-enabling reinstates the filter or attribute and reactivates matching guests at the next sync.

Billing: guests in exactly one active channel are single-channel guests, free up to a 1:1 ratio with licensed seats; guests in several active channels count as paid users. Exceeding the ratio only produces soft warnings. Guests cannot be given an expiry date, MFA applies to guests only if enforced for everyone, and upload limits are server-wide. Restrict who can register via Whitelisted Guest Domains.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/onboard/guest-accounts (limits, authentication, roles, billing FAQ). Nothing removed.

Method: documentation only; no commands were run.
