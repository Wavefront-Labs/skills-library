---
id: computing-software.systems-network-administration.netbird.api-authentication
name: api-authentication
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, rest-api, bearer-token, authorization-header, api-rate-limits]
level: intro
status: docs-checked
description: "Authenticate NetBird API calls with an OAuth2 bearer token or personal access token, with curl examples, best practices and cloud rate limits."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/ipa/guides/authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two token types:
- OAuth2 bearer token from your identity provider: `Authorization: Bearer {token}`.
- Personal access token (PAT), created in the dashboard under User settings: `Authorization: Token {token}`.

```
curl https://api.netbird.io/api/users -H "Authorization: Bearer {token}"
curl https://api.netbird.io/api/users -H "Authorization: Token {token}"
```

Best practice:
- Use service users rather than personal accounts for organisation-wide calls.
- For MSP multi-tenant accounts, scope calls to a tenant (see the MSP API access guide).
- Keep tokens safe and reset one if you suspect it has been compromised.

Cloud limits: 120 requests per minute with bursts up to 1,200; contact support@netbird.io for more.

## Checked

2026-11-04. Confirmed against the NetBird API authentication guide: the two auth methods, header formats, curl examples against `https://api.netbird.io/api/users`, service user advice, MSP pointer, 120 requests per minute with burst of 1200 on cloud, support contact. Removed the list of other endpoints, which this page does not give.
Method: documentation only; no commands were run.
