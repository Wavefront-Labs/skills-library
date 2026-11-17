---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-subject-confirmation
name: saml-subject-confirmation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-subject-confirmation, saml-assertions, subjectconfirmation, bearer, recipient, inresponseto, notonorafter, identity-protocols]
level: practitioner
status: docs-checked
description: "Validate SubjectConfirmationData for the bearer method: Recipient, NotOnOrAfter, InResponseTo and Address checks that bind an assertion to one request."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SubjectConfirmation and bearer data

Goal: apply the bearer subject-confirmation checks the Web Browser SSO profile requires.

Method: the method URI is `urn:oasis:names:tc:SAML:2.0:cm:bearer`. In `SubjectConfirmationData` the relying party must check:
1. `Recipient` equals the exact ACS URL that received the POST.
2. `NotOnOrAfter` has not passed, subject to allowable clock skew between the providers.
3. `InResponseTo` equals the ID of the AuthnRequest it sent; an unsolicited (IdP-initiated) response must not carry it.
4. `Address`, if present, may be checked against the user agent's client address (a MAY in the profile).

Gotchas:
- An assertion can hold several SubjectConfirmation elements; satisfying any one is sufficient to confirm the subject.
- `NotBefore` must not appear on bearer confirmation data.
- For the POST binding the profile requires the assertion to be signed, and the SP must not accept a bearer assertion twice: keep the used assertion IDs for as long as the assertion would be valid by its `NotOnOrAfter`.
- An assertion with a bearer confirmation must contain an `AudienceRestriction` naming the SP.
- An assertion whose subject confirmation requirements cannot be met should be discarded and not used to establish a security context.

Verify: replay the same response and confirm the second use is rejected.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Profiles section 4.1.4.2-4.1.4.5 (bearer confirmation data requirements, response processing rules, POST replay rule, unsolicited responses) and the SAML Core Subject text (any one confirmation suffices). Removed the 1-3 minute skew figure and the NAT/proxy remark about Address (not stated), and added the profiles PDF as a source.
