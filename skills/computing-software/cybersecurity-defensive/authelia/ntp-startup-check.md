---
id: computing-software.cybersecurity-defensive.authelia.ntp-startup-check
name: ntp-startup-check
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, ntp, time-sync, totp, startup-check, max-desync]
level: practitioner
status: docs-checked
description: "Configure Authelia's NTP startup check, including address schemes, version, max_desync, and why disabling it is unsupported for TOTP correctness."
sources:
  - https://www.authelia.com/configuration/miscellaneous/ntp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Time drift breaks TOTP and other time-based security features, so Authelia checks its clock against an NTP server at startup.

```yaml
ntp:
  address: 'udp://time.cloudflare.com:123'
  version: 3
  max_desync: '3s'
  disable_startup_check: false
  disable_failure: false
```

- `address` is a connector URL with scheme `udp`, `udp4` or `udp6`, for example `udp6://[fd00:1111:2222:3333::1]:123`.
- `version` is 3 or 4 (the documented default is 4; the example uses 3).
- `max_desync` (default 3 seconds) tunes the acceptable desync from the time the NTP server reports.
- `disable_startup_check: true` skips the check entirely.
- `disable_failure: true` lets Authelia start and only logs an error when the desync exceeds `max_desync`. By default, if it reaches the server and the time is further out than `max_desync`, Authelia logs a fatal error and exits.

Both disabling options are discouraged. The page states they are not supported configurations, and that any failure of a time-reliant feature caused by a wrong clock is unlikely to be fixed or accepted upstream. The docs urge fixing the underlying time issue instead.

The check runs only at startup. It protects session cookie expiry times, OpenID Connect JWT issued-at, not-before and expiry times, and TOTP code validity.

Check: start Authelia with a deliberately wrong `address` and confirm it logs the failure, then restore.

## Checked

2026-11-08. Read the full Authelia NTP page. Confirmed address schemes, version values and default, max_desync default, both disable options, the startup-only check and why it matters. Removed unsourced operational advice (NTP client on the node, internal NTP server for blocked UDP).

Method: documentation only; no commands were run.
