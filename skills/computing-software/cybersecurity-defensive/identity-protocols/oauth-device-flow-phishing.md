---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-device-flow-phishing
name: oauth-device-flow-phishing
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-device-flow-phishing, oauth-device-grant, device-code-phishing, consent, verification-page, restrict-device-flow, identity-protocols]
level: advanced
status: docs-checked
description: "Defend against device code phishing: user-facing context on the verification page, short codes lifetime, restricting the grant, and Conditional Access blocks."
sources:
  - https://www.rfc-editor.org/rfc/rfc8628
  - https://www.rfc-editor.org/rfc/rfc8252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device flow phishing and mitigations

Goal: stop attackers tricking users into approving their session.

Background: an attacker starts a device flow, sends the victim the user code with a pretext, and polls for tokens once the victim approves.

Method:
- The verification step should tell the user they are authorizing a device, display information about the device, and ask them to confirm the device is in their possession (RFC 8628 section 5.4).
- Keep the user code lifetime long enough to use but short enough to limit codes sent by email or text, and rate-limit code entry (section 5.1).
- Native apps that can open a browser can use authorization code with PKCE and a loopback redirect instead (RFC 8252 section 7.3).

Gotchas:
- `verification_uri_complete` removes the typing, so confirming the device is in the user's possession matters more; display the code and ask the user to check it matches the device (section 5.4).

Verify: open the verification page from a link and check that it asks the user to confirm the device.

## Checked

2026-11-02. Confirmed against RFC 8628 sections 3.3.1, 5.1 and 5.4 (device confirmation, `verification_uri_complete` risk, rate-limiting, user code lifetime) and RFC 8252 section 7.3 (loopback redirect, cited by RFC 9700). Removed: client name, logo and scope display requirements, the 5-10 minute figure, auto-fill advice, the Entra Conditional Access statement and the sign-in log audit.
Method: documentation only; no commands were run.
