---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-pkce-confidential-clients
name: oauth-pkce-confidential-clients
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-pkce-confidential-clients, oauth-pkce, pkce, confidential-client, bff, web-app, defense-in-depth, identity-protocols]
level: practitioner
status: docs-checked
description: "Apply PKCE to server-side web apps too: protects against code injection even when a client secret exists, with session storage of the verifier."
sources:
  - https://www.rfc-editor.org/rfc/rfc7636
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCE for confidential clients and BFFs

Goal: use one flow shape for every client.

Method: RFC 9700 RECOMMENDS PKCE for confidential clients (it is mandatory for public clients). Server-side apps generate the verifier at the start of login, keep it bound to the user agent that started the transaction, and send it at the token exchange together with client authentication. The PKCE challenge must be transaction-specific and securely bound to the client and user agent.

Gotchas:
- A server using PKCE can rely on it for CSRF protection only if it has ensured the AS supports PKCE (RFC 9700 section 2.1).
- Servers should detect and prevent constant `code_challenge` values; a constant value gives no protection.

Verify: capture the callback and confirm that exchange fails without the verifier.

## Checked

2026-11-02. Confirmed against RFC 9700 section 2.1.1 (PKCE recommended for confidential clients, transaction-specific challenge, CSRF protection) and RFC 7636 (verifier required at redemption). Removed: cookie recipe, framework names and legacy AS remark (not in either document).
Method: documentation only; no commands were run.
