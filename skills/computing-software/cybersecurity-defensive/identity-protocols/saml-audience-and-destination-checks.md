---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-audience-and-destination-checks
name: saml-audience-and-destination-checks
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-audience-and-destination-checks, saml-security-considerations, audience, audiencerestriction, destination, issuer, confused-deputy, identity-protocols]
level: practitioner
status: docs-checked
description: "Reject assertions meant for another SP: AudienceRestriction equals the SP entityID, Destination matches the ACS, Issuer is the expected IdP."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audience, Destination and Issuer checks

Goal: block cross-SP assertion replay.

Checks the SP must perform:
1. `Conditions/AudienceRestriction/Audience` identifies this SP: within one restriction the audiences are an OR (one match is enough) and multiple restrictions are evaluated independently and combined as an AND. The profile requires an assertion with a bearer confirmation to carry an `AudienceRestriction` that includes the SP's unique identifier.
2. `Response/@Destination`, when present, must identify the location where the message was received, or the message must be discarded.
3. `Issuer` is the expected IdP (practice; the profile also has the SP verify signatures on the assertion or response).
4. The `Recipient` in a bearer SubjectConfirmationData matches the ACS URL that received the response.

Gotchas:
- Audience restriction states that the asserting party makes no representation to anyone outside the audience, so an SP that ignores it may accept an assertion issued for another SP.
- Compare the identifier as an exact string (practice).
- If no `Audience` elements are present, no audience restriction is imposed; a bearer assertion without one does not meet the profile.

Verify: take an assertion from one test SP and present it to another.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Core 2.5.1.4 (AudienceRestriction semantics) and Destination definition, and Profiles 4.1.4.2-4.1.4.3 (required AudienceRestriction, Recipient check). Swapped the source from the security considerations PDF, which does not cover these checks, to Core and Profiles.
