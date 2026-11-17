---
id: computing-software.cybersecurity-defensive.security-architecture.continuous-access-evaluation
name: continuous-access-evaluation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [zero-trust, continuous-access-evaluation, cae, session-revocation, entra-id, sign-in-frequency, critical-event-evaluation]
level: advanced
status: docs-checked
description: "Make access decisions continuous rather than at login: Entra Continuous Access Evaluation, strict location enforcement, sign-in frequency, and CAE-aware apps vs token lifetimes."
sources: ["https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation", "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation-strict-enforcement", "https://csrc.nist.gov/pubs/sp/800/207/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuous access evaluation

Zero trust (NIST SP 800-207) says access is evaluated per session and re-evaluated as conditions
change. Plain OAuth falls short: by default an Entra access token is valid for one hour, so it stays
usable after the user is disabled or moves to another network. CAE closes the gap with a two-way
"conversation" between the token issuer and the resource, based on the OpenID Continuous Access
Evaluation Profile (CAEP).

## Entra CAE
- **Critical event evaluation** (needs no Conditional Access policy): Exchange Online, SharePoint
  Online and Teams subscribe to events: user deleted or disabled, password changed or reset, MFA
  enabled for the user, admin revoked all refresh tokens, Entra ID Protection high user risk.
  Target is near real time; up to 15 minutes of propagation latency may be seen.
- **Conditional Access policy evaluation**: Exchange Online, SharePoint Online, Teams and Microsoft
  Graph sync key Conditional Access policies; IP-location enforcement is instant.
- The resource rejects the token with a 401 plus claim challenge; a CAE-capable client bypasses its
  cache and goes back to Entra, which re-evaluates all conditions.
- CAE sessions get long-lived tokens (up to 28 hours) and the configurable token lifetime policy is
  not honoured for them; this is normal. Non-CAE clients keep the default one-hour lifetime.
- Sign-in frequency is honoured with or without CAE.

## Strict location enforcement (preview)
- Standard mode (default): if the resource sees a disallowed IP but Entra sees an allowed one, Entra
  issues a short-lived (one-hour) token that suspends IP checks at the resource.
- Strictly enforce location policies: access is blocked whenever the IP seen by the resource is not
  allowed. Use only when egress IPs are dedicated and enumerable for both Entra and all resource traffic.
- Rollout: build an IP-based location policy, test on a small user subset, use the sign-in log column
  "IP address (seen by resource)" and the "Continuous Access Evaluation Insights" workbook to find IPs
  to add to named locations, then widen. Do not enable it if traffic to non-Microsoft 365 apps goes
  through Global Secure Access.
- Configure: Conditional Access policy, Session controls, "Customize continuous access evaluation".

## Limits to know
- CAE sees only IP-based named locations, not country/region or MFA trusted IPs; include IPv4 and IPv6.
- If location policies total more than 5,000 IP ranges, real-time location enforcement is skipped
  (one-hour token); other events are still enforced.
- Guest users are not supported by CAE.
- Policy and group membership changes can take up to a day to reach resource providers (two hours in
  some optimised cases); to apply now, use "Revoke Session" on the user profile or the
  revoke-mgusersign PowerShell command.
- Re-enabling a just-disabled user: about 15 minutes latency in SharePoint Online and Teams, 35-40
  minutes in Exchange Online.
- Client and app support varies (Office web apps and Teams calls/chat are partial or unsupported):
  check the support tables on the CAE page.

## Beyond Microsoft
- CAEP (OpenID Shared Signals) is the industry standard behind CAE.
- For your own apps: short access token lifetimes with refresh token rotation, server-side session
  checks against a revocation list, and re-auth for sensitive actions.

## Incident use
Disabling a user or revoking sessions takes effect quickly on CAE resources; non-CAE apps (third-party
SAML apps, legacy clients) keep sessions until their own token or cookie expires: revoke those
separately in each app.

## Verify
Test user signed into Outlook: disable the user and confirm access fails within the documented
15-minute window; for strict location, connect from an unlisted IP and confirm the token is rejected.

## Checked
2026-11-01. Confirmed against the two Microsoft Learn CAE pages (updated 2026-04 and 2026-03): one-hour
default token, critical events list, 15-minute latency, 28-hour CAE tokens, 5,000-range limit, guest
and location-type limits, strict vs standard mode, rollout steps, enable-after-disable latencies,
revoke options; NIST SP 800-207 page for the zero-trust framing. Removed: Okta/Google support claim,
"60-90 minute" token, Graph as critical-event subscriber, token protection and 8h sign-in frequency
advice, 5-15 minute own-app lifetimes, "CAE token type" log note, default-on claim.
Method: documentation only; no commands were run.
