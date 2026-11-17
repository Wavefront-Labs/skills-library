---
id: computing-software.database-administration.redis.redis-rate-limiter-patterns
name: redis-rate-limiter-patterns
category: computing-software
field: database-administration
product: redis
tags: [redis, rate-limiter, token-bucket, sliding-window, fixed-window, lua]
level: practitioner
status: docs-checked
description: "Implement rate limiting in Redis with fixed window, sliding window (sorted set) and token bucket (Lua) patterns, including atomicity and key expiry."
sources: ["https://redis.io/docs/latest/commands/", "https://redis.io/docs/latest/develop/programmability/eval-intro/", "https://github.com/brandur/redis-cell"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis rate limiter patterns

**Goal:** limit actions per key (user, IP, API token) correctly under concurrency.

## Fixed window (cheapest)
```
SET rl:u42:202611020914 0 EX 60 NX
INCR rl:u42:202611020914
```
Allow when the INCR result is at most the limit. Setting the expiry with `NX` before INCR (or one Lua script) avoids the classic bug of INCR then crash before EXPIRE leaving an immortal key. Weakness: bursts at the window boundary can reach 2x the limit.

## Sliding window log (exact, more memory)
Atomic via Lua (`EVAL`):
```lua
local now = tonumber(ARGV[1]); local win = tonumber(ARGV[2]); local lim = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, now - win)
if redis.call('ZCARD', KEYS[1]) < lim then
  redis.call('ZADD', KEYS[1], now, ARGV[4]); redis.call('PEXPIRE', KEYS[1], win); return 1
end
return 0
```
Pass a unique member (`ARGV[4]`, such as a request id) so concurrent requests do not collapse. Memory is O(limit) per key.

## Token bucket (smooth bursts)
Store `tokens` and `ts` in a hash. In Lua: refill `tokens = min(cap, tokens + (now-ts)*rate)`, deduct 1 if at least 1 available, write back with `PEXPIRE` to the time to refill. Take `now` from `redis.call('TIME')` inside the script for a consistent clock across app servers. The redis-cell module offers `CL.THROTTLE` for this where modules are allowed.

## Operating
- All read-modify-write logic goes in Lua or a transaction; client-side GET/SET races.
- In Redis Cluster all keys of a script must share a hash slot (`{user42}` tag).
- Decide fail-open vs fail-closed when Redis is down.
- Return `429` with `Retry-After`; log limit hits.

## Verify
Load test with concurrent clients: allowed count never exceeds limit per window; keys disappear after expiry (`TTL`).

## Checked
2026-11-09. Confirmed in the Redis command and scripting docs: SET with EX and NX options, scripts atomically combine commands across keys, scripts must receive all key names as KEYS (same hash slot in Cluster), TIME is usable inside scripts. Confirmed in the redis-cell README: module providing the CL.THROTTLE command. Nothing was removed; the window and token-bucket designs are patterns, not documented figures.
Method: documentation only; no commands were run.
