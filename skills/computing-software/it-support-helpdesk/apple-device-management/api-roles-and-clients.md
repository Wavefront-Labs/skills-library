---
id: computing-software.it-support-helpdesk.apple-device-management.api-roles-and-clients
name: api-roles-and-clients
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-api, api-roles-and-clients, api-clients, oauth, least-privilege]
level: practitioner
status: draft
description: "Create least-privilege API roles and clients in Jamf Pro using OAuth client credentials instead of shared admin accounts."
sources:
  - "https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview"
  - "https://developer.jamf.com/jamf-pro/reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# api-roles-and-clients

Goal: secure automation access.
- Settings > System > API Roles and Clients: create a Role with specific privileges, then a Client bound to the role with a token lifetime.
- Request a token: `POST /api/oauth/token` with `grant_type=client_credentials`, `client_id`, `client_secret`.
- Store the secret in a vault, never in scripts or policy parameters.
- One client per integration and rotate secrets on staff change.
- Audit through Change Management logs.
Practice: Prefer read-only roles for reporting and separate roles for write tasks, set short token lifetimes and alert on unexpected client activity in the audit logs.
Gotcha: tokens are short-lived; scripts that cache one overnight get 401, so request a new token per run.
Verify:
- The client can only perform listed actions.
- Secret is not in repo or script text.
