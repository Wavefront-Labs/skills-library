---
id: computing-software.database-administration.patroni.patroni-health-check-endpoints
name: patroni-health-check-endpoints
category: computing-software
field: database-administration
product: patroni
tags: [patroni, rest-api, health-check, haproxy, load-balancer]
level: practitioner
status: docs-checked
description: "Which Patroni REST GET endpoints return 200 for primary, replica, sync, quorum and async roles, for load balancers."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route traffic by role with HTTP checks.

All health GET requests return a JSON status document plus an HTTP code. Use HEAD or OPTIONS if the body is not needed.

Return 200 only for a primary holding the leader lock: `GET /`, `/primary`, `/read-write`.
- `/standby-leader`: leader of a standby cluster.
- `/leader`: node holds the leader lock, regardless of whether Postgres is primary or standby_leader.
- `/replica`: state running, role replica, and `noloadbalance` tag not set.
- `/read-only`: like `/replica` but also includes the primary.
- `/synchronous` or `/sync`: a synchronous standby; `/read-only-sync` also includes the primary.
- `/quorum`: node listed as quorum node in `synchronous_standby_names` on the primary; `/read-only-quorum` includes the primary.
- `/asynchronous` or `/async`: an asynchronous standby.
- `/health`: PostgreSQL is up and running.

Lag filter: `GET /replica?lag=<max-lag>` (and `/async?lag=`) also requires replication latency below the value, in bytes or human units such as `16kB`, `64MB`, `1GB`.

Tag filters: `GET /replica?tag_key1=value1&tag_key2=value2` checks user-defined tags; if the tag is undefined or the value differs, the response is 503. For leader and primary style endpoints (`/`, `/leader`, `/primary`, `/read-write`, `/standby-leader`) tags are ignored.

A node with `noloadbalance` set returns 503 on `GET /replica` and is excluded from load balancing.

## Checked

2026-11-08. Confirmed against the Patroni REST API page (health check endpoints list, lag and tag query parameters). Removed the claim that Patroni ships an HAProxy example configuration, which the page does not state, and clarified the `/read-only` wording.

Method: documentation only; no commands were run.
