---
id: computing-software.systems-network-administration.netbird.service-users-and-tokens
name: service-users-and-tokens
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, service-users, personal-access-tokens, api-automation, msp-tenant-token]
level: practitioner
status: docs-checked
description: "Create NetBird service users and access tokens for automation, choose roles, handle token display and rate limits, and scope MSP tokens to a tenant."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/public-api/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service users are non-interactive accounts for the public API, so automation (Ansible, Terraform, cURL, integrations) keeps working when employees leave.

Create a service user: Team > Service Users, assign a role. The User role is read-only; Admin allows writes.

Create a token: Team > select yourself or a service user > create token, set expiration (tokens cannot be modified afterward). Copy it immediately: NetBird stores only a hash.

Use: `Authorization: Token {token}`. The API grants whatever the associated user may do.

Rate limit on the cloud service: 120 requests per minute, bursts up to 1,200; contact support@netbird.io for more.

Security:
- Treat tokens like passwords and limit the scope of access granted to each service user.

MSP accounts: a PAT of an MSP user reaches every tenant that user can reach. Append `?account=<tenant_id>` to target one tenant. Use MFA on the underlying SSO identity, rotate tokens, and store them in a secrets manager.

## Checked

2026-11-04. Confirmed against the NetBird service users and tokens page: purpose, Team Service Users path, role semantics, token expiry and hash-only storage, Token header, cloud rate limit, MSP tenant scoping advice. Removed a general secrets manager bullet, which the page states only for MSP tokens.
Method: documentation only; no commands were run.
