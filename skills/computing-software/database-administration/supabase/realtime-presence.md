---
id: computing-software.database-administration.supabase.realtime-presence
name: realtime-presence
category: computing-software
field: database-administration
product: supabase
tags: [realtime, presence, track, presence-state, sync]
level: practitioner
status: docs-checked
description: "Supabase Realtime Presence: track and untrack, sync join and leave events, presence keys, and when to use Broadcast instead."
sources:
  - https://supabase.com/docs/guides/realtime/presence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share who is online and slow-changing state.

JavaScript calls:
- `supabase.channel('room_01')`, optionally with `config: { presence: { key } }`.
- `channel.on('presence', { event: 'sync' | 'join' | 'leave' }, handler)`.
- `channel.subscribe()`, then `channel.track(payload)` and `channel.untrack()`.
- `channel.presenceState()` reads the merged state: an object keyed by presence key, each value an array of payloads such as `[{ "userId": 1, "typing": false }]`.
- Call `track()` inside the `subscribe` callback once the status is `SUBSCRIBED`.

Events: `sync` means the full presence state updated; `join` means a client started tracking; `leave` means a client stopped.

Behaviour:
- Each client's payload is stored under a unique presence key and Supabase keeps a merged view of all clients.
- Without a custom key the server generates a UUIDv1. A custom key must be unique among clients.
- A `sync` event may arrive alongside `join` and `leave`; that is state reconciliation, not real user activity.
- `untrack()` triggers the `sync` and `leave` handlers.
- Clients receive state from other subscribers on the same topic, and their own `sync` and `join` handlers fire too.

Use presence for online status, the active document or the current page. Do not call `track()` at high frequency, such as on every mouse move; use Broadcast for that.

Other SDKs: Dart `onPresenceSync`, `onPresenceJoin`, `onPresenceLeave`; Swift `presenceChange()`; Kotlin `presenceChangeFlow()`; Python `on_presence_sync`; C# `Register<T>(key)` and `AddPresenceEventHandler`.

The `anon` and `service_role` keys are being deprecated by the end of 2026; use publishable (`sb_publishable_...`) and secret (`sb_secret_...`) keys.

## Checked

2026-11-04: Read the Presence guide in full; the non-JavaScript SDK names were confirmed against the Markdown source on GitHub (the rendered text shows JavaScript only). Confirmed the three events, state shape, key behaviour, `untrack()` handlers, the high-frequency warning and the key deprecation notice. Added the state shape and the `SUBSCRIBED` timing from the page's example.
Method: documentation only; no commands were run.
