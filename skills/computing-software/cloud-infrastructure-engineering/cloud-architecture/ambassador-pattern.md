---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ambassador-pattern
name: ambassador-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, ambassador-pattern, out-of-process-proxy, client-connectivity, legacy-client, envoy, pgbouncer, cloud-sql-auth-proxy, egress-proxy]
level: practitioner
status: docs-checked
description: "Put an out-of-process proxy in front of an app's outbound calls to add retries, TLS, auth, routing or pooling without changing legacy code; when to use it and its costs."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/ambassador", "https://cloud.google.com/sql/docs/postgres/sql-proxy", "https://www.pgbouncer.org/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ambassador

A sidecar specialised for the **client side**: the app talks plain `localhost:port`; the ambassador
handles the remote connection's concerns.

## Typical uses
- Offload client connectivity (monitoring, logging, routing, TLS, resiliency) in a language-agnostic way, and
  extend legacy apps that are hard to modify.
- Legacy app that can't do IAM auth or secure transport itself: the Cloud SQL Auth Proxy handles
  authentication with Cloud SQL using IAM permissions, and listens on localhost by default for TCP (or a Unix socket).
- Connection pooling to a database for many short-lived processes: PgBouncer co-located. The Cloud SQL Auth Proxy
  itself does not pool connections but can be paired with a pooler.
- Retries, circuit breaking and routing for outbound calls in languages without good libraries.
- Deployment options: a sidecar with the app, or (for several processes on one host) a daemon or Windows service.

## Steps
1. Keep the ambassador on the same host as the app and bind it to localhost; point app config at it
   (env var, 12-factor config).
2. Give the ambassador the credentials (workload identity), not the app.
3. Configure timeouts and retries at the ambassador; remove duplicates in the app.
4. Health: app readiness should wait for the ambassador (startup ordering).
5. Export ambassador metrics; it sees all outbound traffic and can monitor latency and resource usage.

## Gotchas
- Adds a hop, some latency, and a failure point per instance; if latency is critical or only one language is
  involved, consider a client library, and prefer a service mesh if the platform already provides mTLS and policy.
- Transparent retries are unsafe unless operations are idempotent (for example POST); let the client pass
  context, such as headers to opt out of retry or cap retry count.
- Decide between one shared ambassador and one per client.
- PgBouncer transaction pooling: clients must not use session-based features, since each transaction can land on a
  different server connection. Named protocol-level prepared statements are tracked only when
  `max_prepared_statements` is non-zero; SQL-level `PREPARE`/`EXECUTE` are not tracked. Pick session vs
  transaction mode deliberately.

## Verify
- [ ] App works with only localhost egress allowed (ambassador does the rest).
- [ ] Rotating credentials needs no app restart.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center Ambassador pattern page (purpose, deployment as sidecar
or daemon, latency, idempotent-retry, context headers, shared vs per-client, service mesh alternative), the Cloud SQL
Auth Proxy page (IAM authentication, localhost default, no connection pooling; read through the cited sections) and
the PgBouncer config reference (transaction pooling, `max_prepared_statements`, SQL-level PREPARE not tracked; the
long page was searched for these settings rather than read end to end). Removed unsupported claims: AlloyDB Auth
Proxy, Envoy egress listener, twemproxy/ProxySQL sharding, the "before 1.21" version gate, advisory-lock and `SET`
specifics.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.sidecar-pattern
