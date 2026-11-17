---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.federated-identity-pattern
name: federated-identity-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-implementation-patterns, federated-identity-pattern, openid-connect, oauth2, saml, identity-provider, claims-based-authentication]
level: practitioner
status: docs-checked
description: "Delegate application authentication to an external identity provider: STS and claims, auth code with PKCE, home-realm discovery, ID token validation and IdP as a dependency."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/federated-identity", "https://openid.net/specs/openid-connect-core-1_0.html", "https://datatracker.ietf.org/doc/html/rfc9700", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federated identity

Delegate authentication to a trusted identity provider (IdP). It separates authentication from authorisation and limits credential exposure to the original IdP; the application sees only claims in a token.

## How it works (Azure Architecture Center)
1. The service trusts an IdP or security token service (STS).
2. The consumer authenticates with the IdP/STS and requests a token.
3. The STS returns a token carrying claims (identity, possibly roles and finer rights); it may transform or augment claims by rules.
4. The consumer presents the token to the service, which authorises from claims (claims-based access control).

Trusted IdPs include corporate directories, on-premises federation services, STSs and social IdPs. Use it for enterprise SSO, multi-partner B2B, SaaS with per-tenant IdPs, and workload access where tenant automation calls your APIs without a user and you authorise with tenant-scoped claim validation. Skip it with a single IdP, or when the app uses custom user stores or cannot handle claims-based standards: retrofitting is complex and costly.

## Steps
1. **Do not build credential storage into each app**; point components at the STS (the Azure example uses Microsoft Entra ID, with web app and API both validating tokens and enforcing authorisation from claims such as roles or scopes).
2. **Flow choice.** Use the authorization code flow with PKCE (the Azure example). RFC 9700 says public clients MUST use PKCE, recommends it for confidential clients, and the authorisation server MUST support it; clients SHOULD NOT use the implicit grant, and the resource owner password credentials grant MUST NOT be used.
3. **Home-realm discovery** when the STS has several IdPs: decide automatically from email address or user name, application subdomain, IP range or a browser cookie; otherwise show a page listing trusted IdPs.
4. **Map claims.** Social IdPs often return only an email, sometimes a name, or just a unique identifier, so the app keeps its own user record (usually created at first sign-in) and injects extra claims after each authentication. In OIDC, `sub` is a locally unique, never reassigned identifier within its issuer, so key users on issuer plus `sub`. Amazon Cognito user pools illustrate the bridge model: they take an OIDC ID token or SAML assertion from an IdP, map its claims to a user profile and then issue their own tokens to your app.
5. **Validate the ID token** (OpenID Connect Core): `iss` must exactly match the issuer identifier; `aud` must contain your `client_id` and no untrusted extra audiences; check the signature using the issuer's keys (a token fetched directly from the token endpoint over TLS may rely on TLS server validation instead); current time must be before `exp` (small leeway for clock skew is allowed); if you sent a `nonce`, the claim must be present and match.
6. **Authorisation stays in the app**: each component decides from claims.
7. **Resilience**: authentication can be a single point of failure. Deploy the identity mechanism across the same regions as the app. Azure notes the IdP typically has a high service-level objective and that DR plans then need not cover authentication components.
8. Optional: enforce MFA with Conditional Access in Entra ID; trust partner tenants through cross-tenant access settings without changing app components.

## Gotchas
- A multi-tenant IdP issues tokens for many tenants: validate issuer and audience so outsiders are not admitted.
- Using email as the user key breaks when it changes; use issuer plus `sub`.

## Verify
- [ ] Tokens with wrong issuer, wrong audience or past `exp` are rejected (tested).
- [ ] Neither implicit grant nor password grant is enabled on the IdP client.
- [ ] Behaviour during IdP outage is known and monitored.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Federated Identity pattern (last updated 2026-07-02); OpenID Connect Core 1.0 (ID token validation, `sub`); RFC 9700 (OAuth 2.0 Security BCP); Amazon Cognito user pool federation overview.
Removed as unconfirmed: the `alg: none` rejection and `nbf` checks (not stated in the sections read), groups-overage and `tid`/`oid` claims, front/back-channel logout, SCIM and just-in-time provisioning advice, and the list of vendor STS products beyond those named above.
Method: documentation only; no commands were run.
