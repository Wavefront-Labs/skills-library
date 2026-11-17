---
id: computing-software.cybersecurity-defensive.authelia.session-redis-provider
name: session-redis-provider
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, redis, session-provider, stateless, high-availability, tls, session-storage]
level: practitioner
status: docs-checked
description: "Move Authelia sessions from the default in-memory provider to Redis: address, ACL user, pool sizes, TLS and why it matters for high availability."
sources:
  - https://www.authelia.com/configuration/session/redis/
  - https://www.authelia.com/configuration/session/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia keeps sessions in memory by default, which leaves it stateful. Memory sessions are lost on restart and cannot be shared between replicas, so the documentation recommends Redis for production and for any high availability or Kubernetes deployment.

```yaml
session:
  secret: '<SESSION_SECRET>'
  redis:
    host: '127.0.0.1'
    port: 6379
    timeout: '5s'
    max_retries: 0
    username: 'authelia'
    password: '<REDIS_PASSWORD>'
    database_index: 0
    maximum_active_connections: 8
    minimum_idle_connections: 0
    tls:
      server_name: 'redis.example.com'
      minimum_version: 'TLS1.2'
```

Options:

- `host` is an address or unix socket path. IPv6 literals need square brackets and quotes.
- `username` is only for Redis 6.0+ ACLs; password-only auth remains compatible.
- `database_index` is the same number you would pass to `SELECT`.
- `max_retries: 0` disables command retries.
- `minimum_idle_connections` keeps connections warm when connecting is slow; it cannot exceed the maximum.
- A `tls` block turns on TLS using the system trust store, extendable with the global `certificates_directory`.

The documentation strongly recommends a random alphanumeric password of 64 or more characters (set the Redis user's password to that value) and defining `password` and `session.secret` as secrets rather than inline, especially in containers. `session.secret` is the key used to encrypt session data in Redis. Defaults: `port` 6379, `timeout` 5 seconds, `max_retries` 0, `database_index` 0, `maximum_active_connections` 8, `minimum_idle_connections` 0. Sentinel is configured under `redis.high_availability` and has its own skill.

Check: restart Authelia, reload a protected page and confirm you stay signed in.

## Checked

2026-11-08. Read in full: configuration/session/redis, configuration/session/introduction. Fixed secrets guidance (page recommends secrets, not _FILE specifically), added documented defaults.

Method: documentation only; no commands were run.
