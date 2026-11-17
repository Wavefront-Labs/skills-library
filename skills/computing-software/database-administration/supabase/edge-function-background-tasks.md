---
id: computing-software.database-administration.supabase.edge-function-background-tasks
name: edge-function-background-tasks
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, background-tasks, waituntil, beforeunload, per-worker]
level: practitioner
status: docs-checked
description: "Run background work in Supabase Edge Functions with EdgeRuntime.waitUntil, shutdown events and the per_worker policy for local testing."
sources:
  - https://supabase.com/docs/guides/functions/background-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: respond fast and finish work afterwards.

APIs:
- `EdgeRuntime.waitUntil(promise)` marks a background task.
- `addEventListener('beforeunload', ...)` fires before shutdown; the reason is at `ev.detail?.reason`.
- `addEventListener('unhandledrejection', ...)` catches promises without a rejection handler; call `ev.preventDefault()` inside.

Rules:
- Do not `await` the `waitUntil` call; awaiting blocks.
- Calling `waitUntil` inside the request handler does not block the response.
- The instance keeps running until the promise passed to `waitUntil` completes.
- Wrap the task in try/catch to handle errors.
- Duration is capped by the wall-clock, CPU and memory limits; the function shuts down on reaching any of them.

Local testing: by default the CLI terminates instances after each request, which can kill background tasks. Keep them alive with this in `supabase/config.toml`:

```toml
[edge_runtime]
policy = "per_worker"
```

The page's examples wrap handlers with `withSupabase({ auth: 'user' }, ...)` from `npm:@supabase/server@^1`.

## Checked

2026-11-04: Read the Background Tasks guide in full. Confirmed the APIs, rules, the wall-clock/CPU/memory cap, local-testing behaviour and the `per_worker` policy. Nothing removed.
Method: documentation only; no commands were run.
