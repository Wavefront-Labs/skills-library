---
id: computing-software.database-administration.supabase.database-webhooks
name: database-webhooks
category: computing-software
field: database-administration
product: supabase
tags: [webhooks, pg-net, http-request, triggers, payload]
level: practitioner
status: docs-checked
description: "Send HTTP requests from Supabase table changes with Database Webhooks: events, payload fields, Edge Function auth, secret handling and local URLs."
sources:
  - https://supabase.com/docs/guides/database/webhooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: notify an external service or Edge Function when rows change.

Webhooks wrap triggers and use the `pg_net` extension, which is asynchronous, so long network calls do not block database changes. Events are INSERT, UPDATE and DELETE, all fired after the row changes. Requests are POST or GET with a JSON payload.

Payload fields:
- `type`: INSERT, UPDATE or DELETE.
- `table` and `schema`: strings.
- `record`: the row; null for DELETE.
- `old_record`: null for INSERT; prior row for UPDATE and DELETE.

In SQL, create an `after insert ... for each row` trigger that runs `"supabase_functions"."http_request"`. The page's example passes five string arguments: the URL, `'POST'`, a headers JSON, `'{}'` and `'1000'` (it does not label them).

Calling an Edge Function: send the project's secret key, accept it in the function with `auth: 'secret'` and `verify_jwt = false`. To keep the key out of migrations, store the project URL and secret key in Vault once per project (`vault.create_secret`), outside the migrations, and have a trigger function read them and call `net.http_post`. That function is `security definer` with `set search_path = ''`, because roles such as `authenticated` cannot read Vault and their inserts would otherwise fail with a permission error.

Security warnings:
- A key typed in the Dashboard is saved in the trigger definition, so it shows up wherever the trigger SQL does, such as a database dump.
- Any login-capable role can read the secret key while the request waits, because pg_net writes the decrypted key to `net.http_request_queue` until it sends.

Monitoring: call history is logged in the `net` schema.

Local: `localhost` or `127.0.0.1` in the URL refers to the container itself. Use `host.docker.internal`, or your machine's local IP if that fails (for example `http://host.docker.internal:54321/functions/v1/my-function-name`).

## Checked

2026-11-04: Read the Database Webhooks guide in full. Confirmed events, pg_net behaviour, payload shapes, Edge Function auth, Vault pattern, security warnings, monitoring and local-development advice. Replaced the invented labels for the `http_request` arguments with what the example shows, and scoped the `security definer` statement to the Vault pattern.
Method: documentation only; no commands were run.
