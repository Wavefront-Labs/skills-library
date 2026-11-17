---
id: computing-software.cloud-infrastructure-engineering.portainer.access-the-portainer-api
name: access-the-portainer-api
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [api, access-token, authentication, https]
level: practitioner
status: docs-checked
description: "Create a Portainer user and access token to call the API, and understand that API rights match the user's UI rights."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/api/access.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API access is per user, and its reach equals that user's permissions: a user who can see only one environment gets only that environment through the API.

Steps:

1. Create a Portainer user for the integration.
2. Log in as that user, click the username at the top right and choose My account.
3. In the Access tokens section click Add access token, enter a recognisable Description, and enter the account password (required for security).
4. Copy the token when it is shown and keep it somewhere safe; you cannot view it again after creation.

Requests go over HTTPS to port 9443 (or 9000 for legacy HTTP). The docs also include an API documentation page and an examples page with sample calls. The token gives the same access as the user would have in the UI. Send it in the `X-API-Key` header, for example `GET /api/stacks`. A non-admin user calling an admin-only endpoint such as `/settings` gets an Access denied error.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the per-integration-user advice (not on the page); added the X-API-Key header and the access-denied behaviour.

Method: documentation only; no commands were run.
