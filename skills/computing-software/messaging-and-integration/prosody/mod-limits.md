---
id: computing-software.messaging-and-integration.prosody.mod-limits
name: mod-limits
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, rate-limiting, limits, bandwidth, c2s, s2s]
level: practitioner
status: docs-checked
description: "mod_limits in Prosody: per-session bandwidth rate and burst for c2s, s2sin, s2sout and component, limits_resolution, and unlimited_jids exemptions."
sources:
  - https://prosody.im/doc/modules/mod_limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_limits

Rate-limits sessions to cap bandwidth. Add `"limits"` to `modules_enabled`. Connection types: `c2s`, `s2sin`, `s2sout`, `component`.

```lua
limits = {
  c2s = {
    rate = "3kb/s";
    burst = "2s";
  };
  s2sin = {
    rate = "10kb/s";
    burst = "5s";
  };
}
```

Units are bytes (kb = 1000 bytes). Limits go in the global section only, not per host.

| Option | Default |
|---|---|
| `limits` | `{}` |
| `limits_resolution` | `1` (how long an over-limit session is suspended) |
| `unlimited_jids` | `{}` (0.12.0+; global and VirtualHost lists merge) |

Verify: a client sending faster than the rate is throttled while its JID in `unlimited_jids` is not.

## Checked

2026-11-04. Read the mod_limits page: connection types, the global-only rule, byte units (kb = 1000 bytes), the three options with defaults, unlimited_jids since 0.12.0 and the global/VirtualHost merge all match. Nothing removed.

Method: documentation only; no commands were run.
