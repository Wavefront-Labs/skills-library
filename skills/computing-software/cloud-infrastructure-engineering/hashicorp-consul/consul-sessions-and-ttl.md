---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-sessions-and-ttl
name: consul-sessions-and-ttl
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-sessions, session-ttl, lock-delay]
level: practitioner
status: docs-checked
description: "Use Consul sessions with TTL, behavior release or delete, and lock-delay for leader election built on KV."
sources: ["https://developer.hashicorp.com/consul/commands/lock", "https://developer.hashicorp.com/consul/commands/kv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sessions bind locks and ephemeral keys to a liveness signal. A session is invalidated when its TTL expires, its health checks go critical, or it is destroyed.

```sh
curl -s -X PUT -d '{"Name":"leader-web","TTL":"30s","Behavior":"release","LockDelay":"15s"}' localhost:8500/v1/session/create
curl -s -X PUT -d 'node-1' 'localhost:8500/v1/kv/service/web/leader?acquire=<session-id>'
curl -s -X PUT localhost:8500/v1/session/renew/<session-id>
```

`Behavior` is `release` (the default; held locks are released) or `delete` (the keys of held locks are deleted). `LockDelay` (default 15s, between 0 and 60 seconds in the sessions overview) stops previously held locks being re-acquired for that interval after invalidation, giving a possibly still-live holder time to stop.

Gotchas: `TTL` must be between 10s and 86400s. The TTL is a lower bound, so renew in advance to allow for network delay and clock skew; forcibly expired sessions may not be reaped for up to double the TTL, so avoid TTLs over 1 hour. By default a session uses the gossip-based `serfHealth` node check, so a node failure releases the lock, and false positives are possible. The locking is advisory only: nothing forces clients to take the lock before reading or writing a key.

Verify: `curl localhost:8500/v1/kv/service/web/leader` shows a `Session` field while the lock is held; once the session is invalidated or destroyed, the lock is released (Session cleared) or the key deleted, depending on `Behavior`.

## Checked

2026-11-03. Confirmed against the Session HTTP API page (LockDelay default, TTL range, Behavior values, renew, double-TTL reaping note) and the sessions and distributed locks overview (invalidation rules, serfHealth default, lock-delay 0 to 60 seconds, TTL lower bound, advisory locks, KV acquire and release) and the KV API page. Removed: the renew-at-one-third rule, the lock-delay-zero split-brain claim and the advice to avoid hand-rolled code.

Method: documentation only; no commands were run.
