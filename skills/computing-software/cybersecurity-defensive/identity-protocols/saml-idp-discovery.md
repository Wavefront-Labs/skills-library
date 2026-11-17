---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-idp-discovery
name: saml-idp-discovery
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-idp-discovery, saml-advanced-profiles, idp-discovery, wayf, common-domain-cookie, home-realm, discovery-service, identity-protocols]
level: advanced
status: docs-checked
description: "Choose an IdP in multi-IdP SAML federations: the Identity Provider Discovery profile (common domain cookie _saml_idp) and AuthnRequest Scoping."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IdP discovery and home realm selection

Goal: send each user to the right IdP.

Method: the SAML Profiles specification defines an Identity Provider Discovery profile built on a common domain cookie shared by the IdPs and SPs of a deployment. The cookie is named `_saml_idp`; its value is a space-separated list of base64-encoded IdP identifier URIs, then URL-encoded, with the most recently established IdP session last. It must be set with Path `/`, Domain `.[common-domain]` (leading period) and marked secure. After authenticating a principal the IdP may set it; the SP obtains it through an exchange with an HTTP server in the common domain. Other options: the `Scoping/IDPList` in the AuthnRequest names the IdPs the requester trusts. A discovery-service redirect with `entityID` and `return` parameters is a separate specification that this page does not cover.

Gotchas:
- Validate that an IdP identifier you obtain is one you have metadata for; do not accept arbitrary values (practice).
- The common domain cookie only works inside the one common domain the deployment predetermines, and which entities host web servers there is a deployment issue.
- The cookie may be session-only or persistent, chosen uniformly across the deployment.

Verify: submit an unknown entityID to the return URL and confirm it is rejected.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Profiles to text and read section 4.3 (Identity Provider Discovery profile and common domain cookie) and the Core Scoping description. Removed the discovery-service parameters (entityID, return, returnIDParam), email-domain and per-tenant alternatives, and the multi-tenant leak remark (not in this specification); description updated to match.
