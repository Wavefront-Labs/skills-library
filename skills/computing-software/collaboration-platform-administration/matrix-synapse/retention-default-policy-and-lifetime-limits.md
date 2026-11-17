---
id: computing-software.collaboration-platform-administration.matrix-synapse.retention-default-policy-and-lifetime-limits
name: retention-default-policy-and-lifetime-limits
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, retention, message-retention, max-lifetime, default-policy, allowed-lifetime, m-room-retention, msc1763]
level: practitioner
status: docs-checked
description: "Enable Synapse message retention: default_policy max_lifetime, allowed_lifetime_min and max clamping, the experimental m.room.retention event, and what retention does not cover."
sources:
  - https://element-hq.github.io/synapse/latest/message_retention_policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Message retention policies follow MSC1763 and set how long messages stay in the homeserver database. The key parameter is `max_lifetime`. A room with no policy and no server default never has messages purged on that server. `min_lifetime` is only registered, not otherwise supported. Retention does not apply to state events. The feature is off by default; set `enabled: true` under the `retention` option. Per-room policies via `m.room.retention` are experimental, while the server default policy is considered stable.

A default policy applies to every room lacking its own, so messages are not kept forever:

```yaml
default_policy:
  min_lifetime: 1d
  max_lifetime: 1y
```

Durations use `s`, `m`, `h`, `d`, `w` and `y`, or a number of milliseconds.

Lifetime limits clamp the effective `max_lifetime` (inclusive) when purge jobs run, including for the default policy:

```yaml
allowed_lifetime_min: 1d
allowed_lifetime_max: 1y
```

With these values Synapse never deletes events under a day old and always deletes events over a year old. Either limit can be omitted.

A room admin or moderator sets a per-room policy by sending a state event of type `m.room.retention`, with `max_lifetime` in milliseconds:

```json
{
    "max_lifetime": ...
}
```

Behaviour at expiry: Synapse immediately stops serving the event to clients, and the next purge job removes it from the database, so it can remain on disk longer than the lifetime. Events received from other servers that should already have expired are stored until purged but hidden. Synapse never deletes the last message in a room, only hides it. In a federated room only servers with retention support enabled remove events. See the purge jobs skill for scheduling.

## Checked

2026-11-04. Confirmed against the Synapse Message retention policies page: MSC1763, max_lifetime and min_lifetime support, state events, default_policy, duration units, lifetime limits, m.room.retention, expiry behaviour. Nothing removed.
Method: documentation only; no commands were run.
