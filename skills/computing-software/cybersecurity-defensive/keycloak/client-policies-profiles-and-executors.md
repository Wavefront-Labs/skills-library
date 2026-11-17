---
id: computing-software.cybersecurity-defensive.keycloak.client-policies-profiles-and-executors
name: client-policies-profiles-and-executors
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, client-policies, client-profiles, executors, fapi]
level: practitioner
status: docs-checked
description: "Enforce client configuration rules with Keycloak client conditions, executors, profiles and policies, including secure client URI executors and Full Scope Disabled."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/client-policies.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client policies profiles and executors
Client Policies let an administrator set what configuration a client may have, validate client configuration, and require conformance to profiles such as FAPI and OAuth 2.1. Settings are enforced at client creation and update, and also during OIDC requests tied to a client. They cover what Client Registration Policies (OIDC Dynamic Client Registration only) cover, plus other registration and configuration paths; the docs say Client Registration is planned to be replaced by Client Policies.

Four building blocks:
- **Condition**: decides which client and when a policy applies. Cannot be used alone. Provided conditions include: how the client is created/updated (Dynamic Client Registration, anonymous or authenticated, or Admin REST API), author of the client (role or group), Client Access Type (confidential, public, bearer-only, which is deprecated), Client Scope, Client Role, Client Domain Name/Host/IP, Client Attribute (several attributes are ANDed; repeat the condition for OR), Any Client, ACR Condition, Grant Type, Identity Provider Alias.
- **Executor**: the action run on a client; cannot be used alone, only in a profile. It reacts to events (client create/update, authorization, token, token refresh, revocation, introspection, userinfo requests, logout with refresh token) and can autoconfigure settings and then validate. Examples: enforce PKCE, holder-of-key tokens, HTTPS redirect URIs without wildcards, client secret rotation, DPoP binding (when the dpop feature is enabled), lightweight access tokens, allowed protocol mapper types (`allowed-protocol-mappers`).
- **Profile**: a set of executors. Global profiles are pre-configured for FAPI 1 Baseline, FAPI 1 Advanced, FAPI CIBA, FAPI 2 and OAuth 2.1.
- **Policy**: conditions plus the profiles applied when they match.

Configure under *Realm settings* > *Client policies* tab (per realm); everything is also available through the Admin REST API. A common pattern is a Client Role condition with a "marker role" created on the target clients.

Client URIs: Secure Client URIs enforces HTTPS without wildcards on all configured URI fields; SAML Secure Client URIs enforces HTTPS for SAML clients' URI fields; the Secure Client URIs Pattern executor validates only the URIs you select against a list of permitted regular-expression patterns, and the docs point to it for preventing SSRF.

Full Scope: the `full-scope-disabled` (Full Scope Disabled) executor with Auto-configure On, in a policy, turns Full Scope Allowed off on every new or updated client; existing clients are not changed. With the Any Client condition it also hits `security-admin-console` and `admin-cli`, which can lock you out of the Admin Console; the page suggests excluding them, for example with a `fsa-permitted-marker-role` client role plus a Client Role condition with Negative logic.

Client Policies are evaluated for protocol mapper create, update and delete on clients through the Admin REST API, not for mapper operations on client scopes.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/client-policies.adoc. Removed: the SSRF details (which fields, "empty list blocks every URI") that sit in a dedicated section not read, and the invented localhost Verify step; "OIDC requests" and building blocks rewritten from the page.
Method: documentation only; no commands were run.
