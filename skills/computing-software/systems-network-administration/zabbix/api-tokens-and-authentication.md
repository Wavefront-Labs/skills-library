---
id: computing-software.systems-network-administration.zabbix.api-tokens-and-authentication
name: api-tokens-and-authentication
category: computing-software
field: systems-network-administration
product: zabbix
tags: [api, api-tokens, auth-token, regenerate, token, auth]
level: practitioner
status: docs-checked
description: "Create and manage API tokens for the Zabbix API, including expiry, regeneration and permission inheritance."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/users/api_tokens
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Zabbix API accepts API tokens for authentication. Each token is assigned to a single user and inherits that user's permissions, so requests are authorised according to that user's role and permissions.

Create a token with the Create API token button on the API tokens page. Fields: Name, User (one only, and it cannot be changed later), Description (optional), Set expiration date and time (untick for no expiry), Expiry date (format YYYY-MM-DD hh:mm:ss) and Enabled (untick to create it disabled).

Important behaviour:
- The Auth token value is shown only once, right after you click Add. Copy it and save it somewhere safe before clicking Close.
- It cannot be viewed again. If lost or exposed, edit the token and click Regenerate. After you confirm, the previously generated token becomes invalid.
- Tokens can be filtered by name, assigned user, expiry date, creator and status. Click the status in the list to enable or disable a token, or mass enable and disable from the list.
- Users without access to the Administration menu can see and modify their own tokens under User profile > API tokens only if Manage API tokens is allowed in their user role.

Practice: create a dedicated low-privilege user and role for each integration and give its token an expiry date, rather than reusing a Super admin token.

## Checked

2026-11-09. Confirmed against the API tokens page: inheritance of permissions, field list, one-time display of the Auth token, Regenerate invalidating the old value, filters, and the Manage API tokens role permission. Removed: the Users > API tokens menu path, the per-method API page examples (host.create, history.get) and the unfetched /manual/api source; dropped the json-rpc tag.
Method: documentation only; no commands were run.
