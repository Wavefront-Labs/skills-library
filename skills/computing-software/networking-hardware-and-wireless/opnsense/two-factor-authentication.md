---
id: computing-software.networking-hardware-and-wireless.opnsense.two-factor-authentication
name: two-factor-authentication
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [two-factor, totp, authentication, access-servers]
level: practitioner
status: docs-checked
description: "Where OPNsense 2FA applies (GUI, captive portal, OpenVPN, IPsec, proxy) and what TOTP tokens it supports."
sources: ["https://docs.opnsense.org/manual/two_factor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Two-factor authentication

OPNsense (since 16.1.14) supports two-factor authentication across the system, except console and SSH access. Covered services: the web GUI, Captive Portal, VPN (OpenVPN and IPsec) and the caching proxy.

The method is TOTP per RFC 6238: a one-time password computed from a shared secret and the current time. Google Authenticator works fully, as does any TOTP token; seeds may need conversion to base32 for the token to accept them.

Authentication servers are added under System > Access > Servers; that page supports local users as well as users synchronised from LDAP. The step-by-step setup lives in the Two-factor how-to (Configure 2FA TOTP and Google Authenticator). Console and SSH access are the one exception to system-wide 2FA.

The per-user token seed is held in the OTP seed field of the user entry in the local user manager, so each person needs their own seed before the token can be verified.

## Checked

2026-11-03. Read the Two-factor authentication manual page (two_factor.html) and the Users manual page (users.html) on docs.opnsense.org and confirmed the claims above against them. Removed: the unsupported OTP-option and secret-generation steps, and the keys-and-restricted-access advice for console and SSH.
Method: documentation only; no commands were run.
