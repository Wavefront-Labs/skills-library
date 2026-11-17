---
id: computing-software.cybersecurity-defensive.zitadel.service-account-personal-access-token
name: service-account-personal-access-token
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, service-accounts, personal-access-token, pat, management-api]
level: practitioner
status: docs-checked
description: "Create a ZITADEL personal access token for a service account, grant it a role, and call the management API with it."
sources:
  - https://zitadel.com/docs/guides/integrate/service-accounts/personal-access-token
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A personal access token (PAT) is a ready-to-use token you send as an Authorization header. Human PATs are not supported; only service accounts can have them.

Create one: under Service Accounts choose New, enter a username and display name, open the Personal Access Token menu in the user's detail, and choose New. Set an expiration date, or leave it empty for no expiry. Copy the token from the dialog, as it is shown only once.

To use ZITADEL's APIs the service account needs permissions. On the organization's detail page use the "+" button at top right, search for the service account and give it a role, for example Org Owner.

Call an API directly:

```bash
curl --request GET \
  --url ${CUSTOM_DOMAIN}/management/v1/orgs/me \
  --header 'Authorization: Bearer {PAT}'
```

Security notes from the guide: store keys securely and never embed secrets in code or applications, use secure key management, keep validity short, and handle verification failures.

The guide presents the PAT as an alternative to private key JWT and client credentials; set an expiration date unless the token must not expire.

## Checked

2026-11-08. Read in full: the personal access token guide for service accounts. Removed the unsupported advice about break-glass credentials and preferring other methods.

Method: documentation only; no commands were run.
