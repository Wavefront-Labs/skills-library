---
id: computing-software.database-administration.supabase.edge-function-limits
name: edge-function-limits
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, limits, cpu-time, memory, secrets-limit]
level: practitioner
status: docs-checked
description: "Supabase Edge Function runtime and platform limits: memory, wall clock, CPU time, bundle size, function counts, secrets and blocked ports."
sources:
  - https://supabase.com/docs/guides/functions/limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know the ceilings before designing a function.

Runtime:
- Memory 256MB.
- Wall clock (worker lifetime): 150s on Free, 400s on paid plans.
- CPU time: 2s per request, counting only CPU, not async I/O.
- Request idle timeout 150s; with no response the caller gets a 504 Gateway Timeout.

Platform:
- Function size: 20MB bundled locally via the CLI, 5MB bundled server-side (Management API or Dashboard).
- Functions per project: Free 100, Pro 1000, Team 2000, Enterprise unlimited.
- Log message length 10,000 characters; 100 log events per 10 seconds.
- Recursive or nested calls: 30 requests per trace within 60 seconds.

Secrets: at most 100 per project, names up to 256 characters, value up to 48 KiB (24,576 characters), no `SUPABASE_` prefix. To exceed 100, bundle values into one JSON secret.

Restrictions:
- Outgoing connections to ports 25 and 587 are blocked.
- HTML is served only through custom domains; otherwise `text/html` GET responses are rewritten to `text/plain`.
- The Web Worker API and Node's vm API are unavailable.
- Static files cannot be deployed with the API flag; build with Docker via the CLI.
- Node libraries needing multithreading (libvips, sharp) are not supported.

## Checked

2026-11-04: Read the Edge Functions limits page in full and compared every figure. All confirmed; nothing removed. Limits can change; re-read the page before relying on them.
Method: documentation only; no commands were run.
