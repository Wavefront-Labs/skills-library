---
id: computing-software.email-administration.mailcow.mailcow-two-factor-authentication
name: mailcow-two-factor-authentication
category: computing-software
field: email-administration
product: mailcow
tags: [two-factor-authentication, totp, webauthn, yubi-otp, app-passwords, fido-key]
level: practitioner
status: docs-checked
description: "Enable WebAuthn, Yubi OTP or TOTP two-factor login in mailcow and understand the app-password requirement for mail clients."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-tfa/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Two-factor authentication in mailcow

Three methods are implemented: WebAuthn (which replaced U2F in February 2022), Yubi OTP and TOTP.
- WebAuthn works with any FIDO security key but only over HTTPS.
- Yubi OTP needs internet access and a personal Yubico API ID and key; the key ID (first 12 characters, modhex), API ID and key are stored as the secret in the MySQL table, and the credentials are checked against the Yubico cloud API.
- TOTP uses authenticator apps after scanning a QR code or entering the secret manually.
WebAuthn and Yubi OTP support several keys per user; the key used for login is shown in green.

Important: mailbox users with two-factor authentication enabled must create app passwords for external applications such as mail clients, since those cannot do a second factor.

Yubi OTP setup: in YubiKey Manager choose Applications, OTP, Configure, credential type Yubico OTP; tick Use serial, generate a private ID and secret key, tick Upload and finish. The upload to the Yubico server yields a Client ID and secret key. In the mailcow UI open Access, Two-factor authentication, choose Yubico OTP, name the key, enter the Client ID and secret, confirm with the account password and touch the key.

An administrator can temporarily disable a domain administrator's two-factor login until they next log in successfully. Removing two-factor authentication is covered in the reset-password troubleshooting page.

## Checked

2026-11-09. Confirmed on the two-factor page: three methods, WebAuthn replacing U2F in February 2022, HTTPS requirement, Yubi OTP internet and API ID requirement and modhex storage, multiple keys, green key, TOTP QR setup, app-password warning, the full YubiKey Manager steps, domain admin temporary disable and the pointer to the reset page. No changes needed.

Method: docs-checked 2026-11-09 against the full two-factor page (u_e-mailcow_ui-tfa.en.md in mailcow-dockerized-docs).
