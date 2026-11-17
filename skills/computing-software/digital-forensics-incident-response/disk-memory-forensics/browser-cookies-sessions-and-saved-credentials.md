---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.browser-cookies-sessions-and-saved-credentials
name: browser-cookies-sessions-and-saved-credentials
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [browser-cookies, session-tokens, saved-credentials, dpapi, infostealer, browser-forensics, dfir]
level: advanced
status: draft
description: "Examine browser cookies, session tokens and saved credentials: Chromium encryption with DPAPI and app-bound keys, Firefox key4.db, and infostealer theft scoping."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://security.googleblog.com/2024/07/improving-security-of-chrome-cookies-on.html", "https://attack.mitre.org/techniques/T1539/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser cookies, sessions and saved credentials

**Goal:** determine which sessions and credentials a browser held (for example after an
infostealer infection) so they can be revoked, and use cookies as evidence of site access.

## Chromium
- Cookies: `<Profile>\Network\Cookies` (SQLite `cookies` table: `host_key`, `name`,
  `creation_utc`, `last_access_utc`, `expires_utc`, `encrypted_value`).
- Passwords: `Login Data` (`logins` table: `origin_url`, `username_value`,
  `password_value` encrypted, `date_created`, `date_last_used`).
- Encryption: values encrypted with AES-GCM using a key stored in `Local State`
  (`os_crypt.encrypted_key`), itself protected by **DPAPI** (user context). Since Chrome
  127 (2024) on Windows, **app-bound encryption** (`v20` prefix, `app_bound_encrypted_key`)
  ties decryption to the Chrome service, raising the bar for offline decryption.
- Metadata (host, name, times) is plaintext: enough to list which sites had sessions.

## Firefox
`cookies.sqlite` stores values in **plaintext**; passwords in `logins.json` encrypted with
keys in `key4.db` (NSS), protected by the primary password if set.

## Infostealer scoping
1. Identify the stealer execution time (EDR, Prefetch, Amcache).
2. List cookies and saved logins existing at that time (creation < infection) per profile;
   include all browsers and profiles on the host.
3. Treat all those sessions and passwords as **stolen**: revoke sessions (IdP, SaaS),
   reset passwords, re-register MFA where tokens were present.
4. Check for session-cookie replay in SaaS sign-in logs (same session ID from new IP/ASN).

## Gotchas
- Decrypting user secrets needs authorisation and the user's DPAPI master key (password or
  domain backup key); usually unnecessary for scoping.
- Sync can propagate credentials to other devices of the same account.

## Verify
Every site with a pre-infection session cookie or saved login appears in the revocation list
with completion status.
