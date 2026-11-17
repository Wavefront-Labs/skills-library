---
id: computing-software.systems-network-administration.pi-hole.api-two-factor-and-app-passwords
name: api-two-factor-and-app-passwords
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-2fa, totp, app-password]
level: advanced
status: docs-checked
description: "Enable TOTP two-factor authentication and use application passwords and app_sudo for scripts calling the Pi-hole API."
sources: ["https://docs.pi-hole.net/api/auth/", "https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# 2FA and application passwords

**TOTP.** Setting `webserver.api.totp_secret` to a non-empty value enforces two-factor authentication for the API and web interface. The secret is a 20-byte Base32 value and is write-only; the CLI shows `"********"` once configured. The login reply includes a `totp` flag. Log in with both fields:

```bash
curl -k -X POST "https://pi.hole/api/auth" --data '{"password":"your-password", "totp":123456}'
```

**Application password.** Scripts that cannot use TOTP, or that should not hold your real password, can use an app password. It is a long random password used instead of password plus token. Generate it on the settings page of the web interface; it is shown only once and can be revoked and regenerated at any time (config key `webserver.api.app_pwhash`).

**app_sudo.** `webserver.api.app_sudo` (default `false`) controls whether sessions made with the app password may change configuration such as upstream DNS, DHCP or passwords. Enable it only if you trust the application.

**CLI sessions.** The temporary CLI password (`webserver.api.cli_pw`, default `true`) cannot change configuration either.

**Checklist**

1. Enable TOTP by setting `webserver.api.totp_secret`.
2. Create an app password for each integration.
3. Keep `app_sudo` off unless an integration must write settings.
4. Revoke app passwords no longer used.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: API Authentication (api/auth); FTL Configuration Reference (ftldns/configfile). Replaced the unconfirmed checklist step "Enable TOTP in the web interface" with the documented config key. The page says the app password can be generated on the web settings page (auth page) or through the API (config reference).
Method: documentation only; no commands were run.
