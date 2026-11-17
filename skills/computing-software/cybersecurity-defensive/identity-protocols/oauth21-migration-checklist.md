---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth21-migration-checklist
name: oauth21-migration-checklist
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth21-migration-checklist, oauth-2-1, migration, implicit-to-code, password-grant, inventory, enforcement, identity-protocols]
level: practitioner
status: docs-checked
description: "Move apps off implicit, password and loose redirects toward the OAuth 2.1 draft: inventory, replace flows, require PKCE, exact redirect URIs."
sources:
  - https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating clients to OAuth 2.1 behaviour

Goal: retire legacy OAuth patterns without outages. OAuth 2.1 is still an Internet-Draft (revision 17, October 2026, expiring 4 May 2027 when checked), so treat the requirements below as the draft's current text and re-check the revision.

Plan, with the draft's requirement for each step:
1. Inventory clients and grants from authorization server logs: grant type, `response_type`, redirect URI patterns, PKCE use, and whether access tokens are sent in URI queries.
2. Browser-based apps: the draft says they MUST use the authorization code grant; the Implicit grant (`response_type=token`) and Resource Owner Password Credentials grant are not defined and MUST NOT be used. It lists three patterns: backend for frontend, token-mediating backend, and the app as a public OAuth client (section 9).
3. Native apps: the draft says system-browser authorization requests are more secure than embedded user agents, which let the host app copy credentials and cookies (sections 8 and 8.5.1).
4. Password-grant clients have no direct 2.1 replacement in the draft; move them to the authorization code grant where a user is present, or to a grant that fits the case (for example client credentials for services, which section 4.2 defines for confidential clients only).
5. Redirect URIs: compare with exact string matching (changes-from-2.0 list); replace wildcard or partial registrations with explicit URLs.
6. PKCE: clients MUST use `code_challenge` and `code_verifier` and authorization servers MUST enforce them (except under section 7.5.1 conditions, where it is still RECOMMENDED); the `plain` method is removed. Authorization servers MUST reject requests without a `code_challenge` unless those conditions apply.
7. Tokens in URLs: clients MUST NOT send the access token in a URI query parameter, and resource servers MUST ignore access tokens in a URI query parameter.
8. Refresh tokens: when client authentication is not possible (public clients), the authorization server SHOULD issue sender-constrained refresh tokens or use refresh token rotation (section 4.3.1).
9. Announce deadlines to third parties, then disable the legacy grants and behaviours at the authorization server.

Gotchas:
- Old mobile apps remain in the field for a long time; plan enforcement by client or app version.
- Staged enforcement (log-only first, then enforce) is a rollout technique, not a draft requirement.

Verify: authorization server logs show no implicit or password grants and no query-string tokens before you remove support.

## Checked

2026-11-09. Read draft-ietf-oauth-v2-1-17 (sections 4.1 PKCE, 4.2, 4.3 refresh, 5 resource requests, 7.5.1, 8 native apps, 9 browser-based apps, and the changes-from-OAuth-2.0 list), and the datatracker API record for the current revision. Removed: the 30-day zero-usage rule, "report-only mode", the DPoP and device-flow recommendations (not in the draft), and the claim that webview apps MUST change (the draft states the drawbacks, not a MUST).
Method: documentation only; no commands were run.
