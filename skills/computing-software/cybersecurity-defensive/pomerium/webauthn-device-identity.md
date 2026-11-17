---
id: computing-software.cybersecurity-defensive.pomerium.webauthn-device-identity
name: webauthn-device-identity
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [webauthn, device-identity, device-enrollment, device-not-authorized, secure-enclave]
level: practitioner
status: docs-checked
description: "Require registered WebAuthn devices in Pomerium policy, enroll devices as a user or admin, and handle the 450 device not authorized error."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/integrations/device-context/webauthn.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium uses WebAuthn for clientless device identity (TPM, Secure Enclave, YubiKey): no agent needed, from Pomerium v0.16.0. Limits: it is more browser identity than OS identity, hides hardware details, so deep OS posture checks may need a complementary solution.

**Core**: user-initiated enrollment only; registered devices work immediately with no approval.
**Enterprise**: adds admin pre-approved links, device management (view, approve, delete) and approval of user-initiated devices (they stay pending). Deleting a device revokes it and invalidates its link. Registration is trust on first use.

User steps: visit a route that requires device identity and register, or open the `.pomerium` endpoint, Device Credentials, **Register New Device**.

Admin steps (Enterprise, needs directory sync): Devices, **NEW ENROLLMENT**; choose the user, route, optional redirect URL and enrollment type (**Any**, or **Secure Enclave Only**); SUBMIT and share the link.

Policy: restrict routes with the `device` matcher (see ppl-device-and-record-matchers).

Error: a `450 device not authorized` after registering usually means the policy requires a specific device ID. Users copy their device ID from the `.pomerium` endpoint and send it to an admin, and can remove devices there.

## Checked

2026-11-04. Confirmed against the WebAuthn device identity page: v0.16.0, Core vs Enterprise features, TOFU, delete revokes, admin steps and field names, user steps, 450 error and device ID. Softened the posture-check limitation to the page's wording.

Method: documentation only; no commands were run.
