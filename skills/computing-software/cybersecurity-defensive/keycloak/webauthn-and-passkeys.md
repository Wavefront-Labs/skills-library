---
id: computing-software.cybersecurity-defensive.keycloak.webauthn-and-passkeys
name: webauthn-and-passkeys
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, webauthn, passkeys, passwordless, fido2]
level: practitioner
status: docs-checked
description: "Enable WebAuthn as 2FA or passwordless passkeys in Keycloak, including required actions, policies, and the browser flow change."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/passkeys.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# webauthn and passkeys
WebAuthn as a second factor: check that the *Webauthn Register* required action is enabled (*Authentication* > *Required actions*); toggle *Default Action* on to require all new users to register a credential. In the *Browser* flow, change *WebAuthn Authenticator* inside the *Browser - Conditional 2FA* sub-flow from Disabled to Alternative; users can then choose OTP or WebAuthn, and the sub-flow only asks for a second factor when the user has registered one. To require WebAuthn for everyone, set *Browser - Conditional 2FA* to Required, *OTP Form* to Disabled and *WebAuthn Authenticator* to Required.

Passkeys are the passwordless variant of the same WebAuthn features. Enable the *WebAuthn Register Passwordless* required action, configure the *WebAuthn Passwordless Policy*, then turn on *Enable Passkeys* under *Realm Settings* > *Login* > *Login Screen Customization*. The default forms then offer conditional UI (browser autofill) and a modal *Sign in with Passkey* button. *Passkey Mediation* (in the passwordless policy) takes `conditional` (default: autofill only, no dialog on load), `none`, `optional`, `required` or `silent`; browser behaviour varies, so check your target browsers before relying on `required` or `silent`.

The default browser flow skips *Browser - Conditional 2FA* when a passkey was used. Synced and device-bound passkeys both work for same-device and cross-device authentication, but success depends on the user's environment.

Details:
- The WebAuthn `user.id` handle is an opaque byte sequence of at most 64 bytes.
- Administrators can assign the required action, view credential data such as the AAGUID, set a *User Label* and delete credentials.
- The *Relying Party ID* must be the origin's effective domain; if blank, Keycloak uses the host part of its base URL.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/webauthn.adoc and passkeys.adoc: required actions and flow settings, 64-byte `user.id`, admin credential management, Relying Party ID rule, passkey setup path, mediation values, 2FA skip. Removed: "changing the hostname invalidates credentials" (not stated), the invented Verify step and the exact menu path for the passwordless policy.
Method: documentation only; no commands were run.
