---
id: computing-software.it-support-helpdesk.apple-device-management.platform-sso-methods
name: platform-sso-methods
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, platform-sso, platform-sso-methods, secure-enclave]
level: practitioner
status: docs-checked
description: "Choose Platform SSO authentication methods (password, web-based, smart card, Secure Enclave key, access key) and plan registration and login policy on macOS."
sources:
  - "https://support.apple.com/guide/deployment/dep7bbb05313/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# platform-sso-methods

Goal: let users sign in to the Mac and apps with their IdP identity.

- Needs macOS 13 or later, a management service that supports the Extensible Single Sign-on configuration (which includes Platform SSO settings), and an app containing a Platform SSO extension compatible with the IdP. One domain uses only one SSO extension; if combined with Kerberos SSO, set `syncLocalPassword` to FALSE.
- Methods: Password (also WS-Trust for federated IdPs), Web-based (multi-step, QR code), Smart card (register with the IdP and configure attribute mapping on the Mac), Secure Enclave-backed key (IdP sets it up at user registration; user logs in with the local password), Access key (Apple Wallet pass). Support depends on the IdP and extension.
- Minimum OS for features: login policies macOS 15; on-demand account creation, group management and network authorisation, and Platform SSO in System Settings macOS 14; UPN prefix as local account name and device-identifier attestation macOS 15.4; Tap to Login, Authenticated Guest Mode and Platform SSO during ADE macOS 26; Require Touch ID, web-based authentication and QR code macOS 27.
- Shared device keys are required for Platform SSO during ADE, Require Touch ID, web-based authentication, Authenticated Guest Mode, on-demand account creation and network authorisation.
- Registration: device first (registration token from the extensible SSO configuration, or attestation), then user. Unenrolling the Mac from management also unregisters it from the IdP.
- Token handling: expired or older-than-four-hours tokens are refreshed; full login every 18 hours by default (configurable, minimum one hour).
- Login policies (FileVault, Lock Screen, login window): attempt or require IdP authentication, with an optional offline grace period in days.
- Users see registration state and can repair it in System Settings > Users & Groups.

Gotcha: web-based authentication, Authenticated Guest Mode and login policy need the Mac to reach the IdP before FileVault unlock, with no VPN, network relay or 802.1X in the way. Passkeys cannot be used at FileVault unlock.

Recovery: at FileVault unlock, Option-Shift-Return with the Personal Recovery Key reaches the login window. In recoveryOS, `security platformsso bypass-login-policy` removes the IdP requirement for 12 hours or until the next successful IdP authentication.

Verify:
- System Settings shows the account registered with a working token refresh.
- A test login at each prompt (FileVault, Lock Screen, login window) follows the login policy, including offline.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Platform Single Sign-on for macOS" (the page is marked partly pre-release, so OS minimums may change). Removed as unconfirmed: the payload and key names (`com.apple.extensiblesso`, `AuthenticationMethod` values, `UseSharedDeviceKeys`, `LoginFrequency`), Microsoft and Okta behaviour, the Jamf Connect gotcha, `app-sso platform -s` and the Microsoft Learn source. Authentication method names follow the Apple page's wording.
Method: documentation only; no commands were run.
