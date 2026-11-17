---
id: computing-software.database-administration.supabase.realtime-authorization
name: realtime-authorization
category: computing-software
field: database-administration
product: supabase
tags: [realtime, authorization, realtime-messages, private-channels, rls]
level: advanced
status: docs-checked
description: "Secure Supabase Realtime Broadcast and Presence with RLS on realtime.messages: private channels, extension column, topic helper and revocation lag."
sources:
  - https://supabase.com/docs/guides/realtime/authorization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict who can join, send and listen on Realtime channels.

Setup: control Broadcast and Presence with RLS policies on `realtime.messages`. For private channels, turn off "Allow public access" in Realtime Settings, and create the channel with `config: { private: true }` in JavaScript.

Do not run `ALTER TABLE` to enable RLS on `realtime.messages`: it is already on, and the statement fails with `42501`, aborting the rest of the migration. Check status via `relrowsecurity` in `pg_class`. Creating tables or functions in the `realtime` schema is expected to fail with "permission denied for schema realtime", whether through SQL or the Dashboard; managing RLS policies on `realtime.messages` is allowed. The page's policy examples use `for select` with `using` and `for insert` with `with check`.

Evaluation: permissions are calculated when a client connects and joins a topic, from the policies, JWT, request headers and topic. Realtime does not store messages in `realtime.messages`. In policies use `realtime.topic()` for the requested topic, `current_setting('request.jwt.claims')` for claims, and the `extension` column (`broadcast` or `presence`).

Rules by feature:
- Broadcast join: at least one read or write permission on the topic.
- Broadcast send: an `insert` policy with `extension` = `broadcast`.
- Presence listen: a `select` policy with `extension` = `presence`.
- Presence track: an `insert` policy with `extension` = `presence`.
- One policy can cover both by listing both values.

Postgres Changes are delivered only to clients whose table RLS allows reading; private and public channels can both subscribe.

Caching: access is cached for the life of the connection and refreshed on connect, subscribe, or a new JWT via the `access_token` message. Revocation is therefore delayed until the JWT expires or is replaced, so keep JWT expiry short. If a new JWT is never received on the channel, the client is disconnected when the JWT expires. Complex policies increase connection latency and reduce join rates.

## Checked

2026-11-04: Read the Realtime Authorization guide in full. Confirmed the setup steps, the 42501 behaviour, the evaluation inputs, `realtime.topic()`, JWT claims access, the extension values, per-feature policy rules, Postgres Changes interaction and the caching and revocation text. Added the policy-management allowance and the disconnect-on-expiry behaviour.
Method: documentation only; no commands were run.
