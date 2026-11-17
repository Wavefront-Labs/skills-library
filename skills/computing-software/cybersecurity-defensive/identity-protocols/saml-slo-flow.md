---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-slo-flow
name: saml-slo-flow
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-slo-flow, saml-single-logout, slo, logoutrequest, logoutresponse, single-logout, identity-protocols]
level: advanced
status: docs-checked
description: "Trace SAML SLO: LogoutRequest to the IdP, IdP fan-out to other session participants, LogoutResponse and the status outcomes."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single Logout flow and messages

Goal: terminate a user's sessions across all SPs.

Method: the SP sends `samlp:LogoutRequest` (principal identifier, at least one SessionIndex, optional NotOnOrAfter) to the IdP's single logout service, through the user agent with the Redirect, POST or Artifact binding, or directly with SOAP. The IdP determines the sessions to end, sends LogoutRequests to the other session participants, collects their LogoutResponses, then returns a final LogoutResponse to the original requester. The second-level status `PartialLogout` indicates that not all other session participants confirmed logout. An IdP acting as session authority can also start the flow itself.

Gotchas:
- The profile prefers an asynchronous (front-channel) binding for the original request because it gives the IdP the best chance of propagating logout to the other participants; a synchronous binding that bypasses the user agent constrains the IdP to a similar binding for the propagation.
- LogoutRequest and LogoutResponse must be signed when the HTTP POST or Redirect binding is used; with a synchronous binding the sender must authenticate itself by signing or another binding-supported mechanism.
- A participant must answer a LogoutRequest with a LogoutResponse that carries an appropriate status code, including on error.

Verify: log in to two SPs, log out of one, and check both sessions end.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Profiles section 4.4 (Single Logout profile steps, bindings, signing rules, LogoutRequest/LogoutResponse usage) and Core PartialLogout and LogoutRequest NotOnOrAfter text. Removed the claims that front-channel SLO is fragile, that SOAP is more reliable, and that many IdPs only end their own session (not in the spec).
