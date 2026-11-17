---
id: computing-software.database-administration.supabase.edge-function-cors
name: edge-function-cors
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, cors, preflight, withsupabase, corsheaders]
level: practitioner
status: docs-checked
description: "Handle CORS in Supabase Edge Functions with withSupabase or the SDK corsHeaders import, and the headers browser clients send."
sources:
  - https://supabase.com/docs/guides/functions/cors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let browsers call a function.

Browser invocation requires answering the CORS preflight (`OPTIONS`) request.

Automatic: `withSupabase` handles CORS and preflight, so no manual headers.

```ts
import { withSupabase } from 'npm:@supabase/server@^1'

export default {
  fetch: withSupabase({ auth: 'user' }, async (req, ctx) => {
    const { name } = await req.json()
    return Response.json({ message: `Hello ${name}!` })
  }),
}
```

Manual, if the function doesn't use `withSupabase` (supabase-js v2.95.0 and later): `import { corsHeaders } from 'npm:@supabase/supabase-js@^2/cors'`. This keeps your allow-list aligned with the headers client libraries send; redeploy after upgrading the SDK. From v2.112.3 the list includes trace headers (`traceparent`, `tracestate`, `baggage`), so older deployments need a redeploy before browsers can propagate traces. Trace headers are sent only when a client sets `tracePropagation: true` (off by default).

Headers the client sends: `authorization`, `apikey` and `x-client-info` on every request; `content-type` with a body; `x-retry-count` on automatic retries.

Before v2.95.0 hardcode them in `_shared/cors.ts`:

```ts
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers':
    'authorization, x-client-info, apikey, content-type, x-retry-count, traceparent, tracestate, baggage',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
}
```

Import it with `import { corsHeaders } from '../_shared/cors.ts'`.

## Checked

2026-11-04: Read the CORS guide in full. Confirmed the `withSupabase` behaviour, SDK import, version gates (2.95.0, 2.112.3), the header table, `tracePropagation: true` default off and the hardcoded headers file. Added the page's condition for manual handling.
Method: documentation only; no commands were run.
