---
id: computing-software.messaging-and-integration.prosody.mod-register-limits
name: mod-register-limits
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, registration, rate-limiting, blacklist, whitelist]
level: practitioner
status: docs-checked
description: "mod_register_limits in Prosody: throttle account creation by IP with min_seconds_between_registrations, registration_whitelist and blacklist, and throttle cache size."
sources:
  - https://prosody.im/doc/modules/mod_register_limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_register_limits

Limits account creation by rate and IP, including registrations through third-party web forms.

```lua
modules_enabled = { "register"; "register_limits"; }
registration_whitelist = { "127.0.0.1", "::1" }
registration_blacklist = { "192.0.2.0" }
min_seconds_between_registrations = 60
```

| Option | Default |
|---|---|
| `registration_blacklist` | `{ }` |
| `registration_whitelist` | `{ }` (bypass all limits) |
| `whitelist_registration_only` | false |
| `min_seconds_between_registrations` | nil |
| `registration_throttle_max` | 1 if the min option is set |
| `registration_throttle_period` | value of the min option |
| `registration_throttle_cache_size` | 100 IPs |
| `blacklist_on_registration_throttle_overload` | false |

Verify: a second registration from one IP within 60 seconds is refused.

## Checked

2026-11-04. Read the mod_register_limits page: every option, default and the example (whitelist, blacklist, min_seconds_between_registrations = 60) match, as does the note that it covers third-party registration methods. Nothing removed.

Method: documentation only; no commands were run.
