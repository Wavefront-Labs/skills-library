---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-replay-and-time-validation
name: saml-replay-and-time-validation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-replay-and-time-validation, saml-security-considerations, replay, clock-skew, notbefore, notonorafter, id-cache, identity-protocols]
level: practitioner
status: docs-checked
description: "Prevent SAML replay with an assertion ID cache until NotOnOrAfter, enforce NotBefore and NotOnOrAfter, and keep clocks within a few minutes."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replay protection and clock skew

Goal: accept each assertion once and only within its window.

Method:
- For bearer assertions the SP must prevent replay by keeping the set of used assertion ID values for as long as the assertion would be valid by the `NotOnOrAfter` in its `SubjectConfirmationData`; reject repeats.
- Check `NotBefore` and `NotOnOrAfter` on the Conditions and `NotOnOrAfter` on the SubjectConfirmationData, subject to allowable clock skew between the providers.
- The security considerations document says IdP and SP should make a reasonable effort to keep their clocks within at most a few minutes of each other, and mentions time synchronisation services for that.

Gotchas:
- If several nodes accept responses, the used-ID set must be shared between them, otherwise a replay to another node is not seen (practice).
- Assertion lifetime is not session lifetime: an `AuthnStatement` `SessionNotOnOrAfter` can set when the SP security context should be discarded.
- SAML time values are xs:dateTime expressed in UTC with no time zone component.

Verify: post the same response to two nodes and confirm the second POST is rejected on both.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Profiles 4.1.4.3-4.1.4.5 (replay rule, NotOnOrAfter, SessionNotOnOrAfter), Security and Privacy Considerations 6.4 (clock settings differing by at most a few minutes) and Core 1.3.3 (UTC). Removed the 1-5 minute skew figure, the 5 minute window, NTP and Redis/database advice (not stated).
