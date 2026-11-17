---
id: computing-software.database-administration.supabase.realtime-broadcast
name: realtime-broadcast
category: computing-software
field: database-administration
product: supabase
tags: [realtime, broadcast, send, replay, broadcast-changes]
level: practitioner
status: docs-checked
description: "Supabase Realtime Broadcast: client send and httpSend, realtime.send and broadcast_changes from SQL, REST endpoints, replay and billing tips."
sources:
  - https://supabase.com/docs/guides/realtime/broadcast
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: push low-latency messages between clients and from the database.

Client: `supabase.channel('test-channel')`, `.on('broadcast', { event: 'shout' }, callback)` (`event` may be `"*"`), `.subscribe()`. `channel.send({ type: 'broadcast', event, payload })` uses HTTP before subscribing and WebSockets after. `channel.httpSend(event, payload)` sends over REST without subscribing (supabase-js 2.76.0+; binary needs 2.107.0+). Config: `broadcast: { self: true, ack: true }` echoes to the sender and makes `send` resolve on server confirmation. `private: true` requires authenticated subscribers. Binary payloads (`ArrayBuffer` or `ArrayBufferView`) over WebSocket need supabase-js 2.91.0+ or supabase-swift 2.44.0+; older receivers silently drop them, and the Dart, Kotlin and Python clients do not support binary yet.

From the database:
- `realtime.send(payload => jsonb_build_object(...), event => 'event', topic => 'topic', private => true)`; `private` defaults to true (clients must authenticate), `false` makes a public broadcast.
- `realtime.send_binary(payload => '\x012345'::bytea, ...)`
- `realtime.broadcast_changes(topic, TG_OP, TG_OP, TG_TABLE_NAME, TG_TABLE_SCHEMA, NEW, OLD)` inside a trigger function; the page's example is `SECURITY DEFINER SET search_path = ''`, returns `NULL`, and is attached with an `AFTER INSERT OR UPDATE OR DELETE ... FOR EACH ROW` trigger. The client calls `await supabase.realtime.setAuth()` first, then listens on the topic for events `INSERT`, `UPDATE` and `DELETE`.
- Receiving needs a policy such as `CREATE POLICY "authenticated can receive broadcasts" ON "realtime"."messages" FOR SELECT TO authenticated USING ( true );`.

REST: `POST /realtime/v1/api/broadcast/{topic}/events/{event}` (JSON or `application/octet-stream`; `?private=true` for private channels). Batch: `POST /realtime/v1/api/broadcast` with a `messages` array (JSON only).

Replay (supabase-js 2.74.0+): `private: true` plus `broadcast: { replay: { since, limit } }`; `since` is epoch milliseconds (required), `limit` at most 25. Only database-sent messages replay, retained 72 hours to 4 days.

Rules: send and channel privacy must match or messages are not delivered. Database messages in `realtime.messages` are deleted after 3 days. Connect a client before broadcasting from the database, or the insert fails with `WarnSendingBroadcastMessage`. Subscribing only to send raises billing; use `httpSend` or REST. Self-sent messages are billed as received messages; use acknowledgements to confirm delivery instead.

## Checked

2026-11-04: Read the Broadcast guide in full from its Markdown source on GitHub (the rendered text lost the top). Confirmed client calls, version numbers, `httpSend`, the SQL functions, REST endpoints, replay options, retention and the private/public matching rule. Added the `private` default, the binary WebSocket versions and the `broadcast_changes` example details.
Method: documentation only; no commands were run.
