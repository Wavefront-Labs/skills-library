---
id: computing-software.web-development.bun.redis-client
name: redis-client
category: computing-software
field: web-development
product: bun
tags: [bun-redis, redis-pubsub, auto-pipelining, valkey]
level: practitioner
status: docs-checked
description: "Use Bun's built-in Redis client: connection URLs and env vars, auto-pipelining, pub/sub with a duplicate client, reconnect options and unsupported features."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/redis.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { redis, RedisClient } from "bun";
const client = new RedisClient("redis://user:pass@host:6379/0", { tls: false });
await client.set("k", "v");
await client.expire("k", 3600);
const results = await Promise.all([client.get("a"), client.get("b")]); // auto-pipelined
await client.send("MULTI", []);                                       // raw commands, transactions

const sub = await client.duplicate();
await sub.subscribe("news", (message, channel) => {});
await client.publish("news", "hi");
```

- Default URL: `REDIS_URL`, then `VALKEY_URL`, then `redis://localhost:6379`. `rediss://` or `redis+tls://` for TLS; `redis+unix:///path/to/socket` for sockets.
- No connection opens until the first command (or `connect()`). Supports Redis 7.2+.
- Options (defaults): `connectionTimeout` 10000 ms, `idleTimeout` 0, `autoReconnect` true, `maxRetries` 20, `enableOfflineQueue` true, `enableAutoPipelining` true. Backoff starts at 50 ms, cap 2000 ms.

Gotchas:
- A subscribed client accepts only subscription methods, `pubsub()` and `ping()`; use `duplicate()` for other commands. Pub/sub is experimental.
- Idle-timeout closes do not auto-reconnect; call `connect()` again.
- Sentinel and Cluster are unsupported; transactions need `send()`.
- AUTH, INFO, MULTI, EXEC, WATCH, SELECT bypass pipelining.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/redis: REDIS_URL then VALKEY_URL then localhost default, URL schemes for TLS and unix sockets, lazy connection and connect(), Redis 7.2+, option defaults (connectionTimeout 10000, idleTimeout 0, autoReconnect, maxRetries 20, enableOfflineQueue, enableAutoPipelining), backoff 50 ms to 2000 ms, duplicate() for subscriber clients and the allowed subscription-mode methods, experimental pub/sub, idle timeout not reconnecting, raw send() for MULTI, the list of commands that skip pipelining, and Sentinel and Cluster being unsupported. Nothing removed.
Method: documentation only; no commands were run.
