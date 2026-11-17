---
id: computing-software.database-administration.supabase.edge-function-postgres
name: edge-function-postgres
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, postgres, withsupabase, drizzle, ssl]
level: practitioner
status: docs-checked
description: "Query Postgres from Supabase Edge Functions: ctx.supabase vs supabaseAdmin, direct drivers, SSL certificates locally and Drizzle dependencies."
sources:
  - https://supabase.com/docs/guides/functions/connect-to-postgres
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write the database from a function with the right privilege level.

Use `withSupabase` for most apps. It gives `ctx.supabase`, a supabase-js client scoped to the caller's RLS policies. `ctx.supabaseAdmin` bypasses RLS; use it only for privileged work. The wrapper also handles JSON formatting and consistent errors.

```ts
import { withSupabase } from 'npm:@supabase/server@^1'
export default {
  fetch: withSupabase({ auth: 'user' }, async (_req, ctx) => {
    const { data, error } = await ctx.supabase.from('countries').select('*')
    if (error) return new Response(error.message, { status: 500 })
    return Response.json({ data })
  }),
}
```

Direct connections: functions run server-side, so connecting straight to Postgres with Deno Postgres or Drizzle with Postgres.js is safe. For Drizzle, declare dependencies in a `deno.json` inside the function directory. The page's Deno Postgres example reads `SUPABASE_DB_URL`; its Drizzle example creates `postgres(connectionString, { prepare: false })` (the page's comment: prefetch is not supported for Transaction pool mode).

SSL: deployed functions are preconfigured for SSL to the Supabase database. Locally, download the certificate from Database Settings and add to your `.env`:

```bash
SSL_CERT_FILE=/path/to/cert.crt
DENO_TLS_CA_STORE=mozilla,system
```

Restart with `supabase functions serve your-function` after changing `.env`.

## Checked

2026-11-04: Read the Integrating with Supabase Database (Postgres) page in full. Confirmed `withSupabase`, `ctx.supabase` and `ctx.supabaseAdmin`, direct-client safety, the Drizzle `deno.json` advice and the SSL steps. The sample above is shortened from the page's (which wraps the body in try/catch).
Method: documentation only; no commands were run.
