---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-processes
name: twelve-factor-processes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, twelve-factor-processes, stateless-processes, sticky-sessions, session-store, share-nothing, local-filesystem]
level: practitioner
status: docs-checked
description: "Apply factor VI: run the app as stateless share-nothing processes; move sessions, uploads and caches to backing services and remove sticky-session dependence."
sources: ["https://12factor.net/processes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor VI: Execute the app as stateless processes

**Rule:** processes are stateless and share nothing; any data that must persist is stored in a stateful backing
service, typically a database. Memory and local disk are a brief, single-transaction cache only (for example
downloading a large file, operating on it and storing the result in the database).

The app never assumes anything cached in memory or on disk will be there on a future request or job: with many
processes of each type, a later request is likely served by a different process, and even with one process a restart
(deploy, config change, relocation) usually wipes local memory and filesystem state.

## Audit for hidden state
- Server-side sessions in process memory that rely on sticky sessions at the load balancer. 12factor.net calls
  sticky sessions a violation that should never be used or relied upon.
- Uploaded files written to local disk then read by a later request.
- Compiled assets cached on the local filesystem at runtime: compile in the build stage instead.
- In-process caches treated as authoritative (acceptable as a cache, not as the source of truth).
- Scheduled jobs running in every instance (duplicated work) or only on one named instance (design guidance, not
  from the page).

## Fixes
| State | Move to |
|---|---|
| Session data | a datastore with time-expiration, such as Memcached or Redis (the page's suggestion) |
| Persistent data and uploads | a stateful backing service (database or object storage) |
| Compiled assets | the build stage |

## Verify
- [ ] Turn off LB stickiness: tests pass with 3+ replicas.
- [ ] Kill any instance at random during a user session: no logout, no lost upload.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.stateless-design

## Checked
2026-11-08. Confirmed against 12factor.net/processes: stateless share-nothing rule, persistence in a backing
service, memory/filesystem as single-transaction cache, restarts wiping local state, assets compiled at build,
sticky sessions as a violation, Memcached or Redis for expiring session state. Removed as not on that page: signed
cookie sessions, specific counters/locks/cron/websocket fan-out replacements, and the serverless `/tmp` remark.
Method: documentation only; no commands were run.
