---
id: computing-software.cybersecurity-defensive.pomerium.hosted-authenticate-service
name: hosted-authenticate-service
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [hosted-idp, hosted-authenticate, idp-provider, testing, native-ssh]
level: intro
status: docs-checked
description: "Use the Pomerium-hosted authenticate service for testing without IdP credentials, including its limits and the settings native SSH needs."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The hosted authenticate service is a Pomerium-run IdP needing no client ID or secret. It works with open-source Pomerium, Zero and Enterprise, is enabled by default, and offers email/password, Google or GitHub login. It still needs a route and policy, for example a route with `pass_identity_headers: true` and an `allow` block using `or` with an `email` `is` criterion.

Native SSH compatibility needs two extra settings:
- `authenticate_service_url` (you choose it, e.g. `https://authenticate.localhost.pomerium.io`)
- `idp_provider: hosted`

Limitations:
- Only those three sign-in options.
- Session tokens cannot be refreshed, so users re-authenticate about every hour.
- No uptime commitment for the free service.

Data collected includes IP address, OS version, internal domain name and session details (email, name, domain), governed by the Terms of Service.

The page presents it as a quicker way to deploy and test Pomerium. For your own IdP see configure-custom-idp-urls.

## Checked

2026-11-04. Confirmed against the Authentication page: hosted authenticate service editions, default enablement, three sign-in options, example route, native SSH settings, one-hour re-authentication, no uptime commitment, data collected. Replaced an unstated recommendation with the page's own framing.

Method: documentation only; no commands were run.
