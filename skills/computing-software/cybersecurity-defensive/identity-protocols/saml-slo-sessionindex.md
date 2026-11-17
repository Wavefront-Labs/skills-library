---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-slo-sessionindex
name: saml-slo-sessionindex
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-slo-sessionindex, saml-single-logout, sessionindex, nameid, logout, session-store, identity-protocols]
level: advanced
status: docs-checked
description: "Match logout messages to sessions using NameID and SessionIndex from the AuthnStatement, and store them at login."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SessionIndex and NameID matching in logout

Goal: terminate the right session on a LogoutRequest.

Method: at login, store `NameID` (including Format and SPNameQualifier) and `AuthnStatement@SessionIndex` against the local session. A LogoutRequest identifies the principal with an identifier that strongly matches the one in the authentication assertion, plus `SessionIndex` elements. A session participant must include at least one `SessionIndex`; a session authority (or someone acting for it) may omit them to terminate all of the principal's applicable sessions. The IdP must examine the identifier and the `SessionIndex` elements to decide which sessions to end.

Gotchas:
- Transient NameIDs differ per session, so matching works only if you stored the same value.
- An IdP that supports Single Logout must include `SessionIndex` in its authentication statements; if it is missing you cannot ask for per-session logout.
- The request's `Issuer` must be present and identify the requesting entity; the requester must authenticate itself, by signing or a binding-specific mechanism.
- `SessionIndex` values may be small integers or the assertion ID; do not use them to correlate a user across providers.

Verify: unit test with two concurrent sessions for one user and a LogoutRequest naming one SessionIndex.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Profiles and Core to text and read Profiles 4.1.4.2 and 4.4 (SessionIndex requirements, LogoutRequest usage) and Core AuthnStatement SessionIndex text. Removed the exact-comparison and no-case-folding advice (not stated; the spec says strong matching per Core 3.3.4) and the Issuer-equals-session-IdP check as worded.
