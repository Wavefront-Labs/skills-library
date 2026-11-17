---
id: computing-software.cybersecurity-defensive.authelia.validating-forwarded-authentication
name: validating-forwarded-authentication
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, forwarded-headers, validation, x-forwarded-for, access-control, networks, proxy]
level: practitioner
status: docs-checked
description: "Run Authelia's post-change validation of forward authentication, including the network-rule test that proves your proxy does not trust a spoofed X-Forwarded-For."
sources:
  - https://www.authelia.com/reference/guides/validating-forwarded-authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia's guide says to validate the proxy integration in these situations: after initial configuration; after changing the proxy configuration or integration URL; after changing the `server.address`; after changing a protected app's proxy configuration; after changing access control rules; and when upgrading the proxy, since a proxy bug or a changed default can break the integration.

General operation test, needed by everyone:

1. Pick an application that uses the integration and requires authentication.
2. Make sure you are logged out of Authelia.
3. Visit the application and confirm you are redirected to the Authelia portal and asked for the expected level of authentication.

Network access control test, critical if any rule uses `networks`:

1. Complete the general test first.
2. Pick an application on a domain such as `app.example.com`.
3. Add this rule at the very top of the access control rules:

```yaml
access_control:
  rules:
    - domain: 'app.example.com'
      policy: 'bypass'
      networks:
        - '169.254.1.2'
```

4. Run `curl -i -H 'X-Forwarded-For: 169.254.1.2' https://app.example.com`.
5. Confirm the response has `302` on the first line (the guide's example shows `HTTP/2 302`, a `location` header pointing at the Authelia portal, and `302 Found` in the body).
6. Remove the temporary rule.

The reason: these steps ensure your proxies do not arbitrarily trust the `X-Forwarded-For` header, which would otherwise let a client claim a trusted network address.

## Checked

2026-11-08. Read the full Authelia Validating Forwarded Authentication page. Confirmed the scenarios requiring validation, the general operation test, the network access control test steps, the rule and the expected 302 response. Removed the claim that a direct application response is the failure sign and the suggestion to re-run check-policy, which the page does not state.

Method: documentation only; no commands were run.
