---
id: computing-software.software-engineering.software-architecture.rate-limiting-algorithms
name: rate-limiting-algorithms
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, resilience, rate-limiting, token-bucket, sliding-window, leaky-bucket, redis]
level: practitioner
status: verified
description: "Choose and implement rate limiting algorithms (token bucket, leaky bucket, fixed and sliding window) locally or in Redis, with burst handling and distributed accuracy trade-offs."
sources: ["https://en.wikipedia.org/wiki/Token_bucket", "https://blog.cloudflare.com/counting-things-a-lot-of-different-things/", "https://redis.io/glossary/rate-limiting/", "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limiting algorithms

| Algorithm | Behaviour | Memory | Notes |
|---|---|---|---|
| **Token bucket** | refill r tokens/s up to capacity b; each request takes 1 | 2 numbers/key | allows bursts up to b, average r. Default choice. |
| Leaky bucket (queue) | requests drain at fixed rate; overflow dropped | queue | smooths output; adds latency |
| Fixed window counter | count per calendar window | 1 counter | 2x burst at window edges |
| Sliding window log | timestamps of each request | O(requests) | exact, expensive |
| Sliding window counter | weighted current + previous window | 2 counters | ~exact, cheap (Cloudflare) |
| GCRA | token bucket as "theoretical arrival time" | 1 timestamp | implemented by the redis-cell Redis module (`CL.THROTTLE key max_burst count period [quantity]`) |

## Token bucket (lazy refill, no timer)
```python
def allow(state, now, rate, cap, cost=1):
    tokens = min(cap, state.tokens + (now - state.ts) * rate)
    if tokens < cost: return False, state._replace(tokens=tokens, ts=now)
    return True, state._replace(tokens=tokens - cost, ts=now)
```

## Sliding window counter
`estimate = prev_count * (1 - elapsed/window) + curr_count` (Cloudflare's example: 42 requests in the previous minute, 18 so far, 15 s into the minute: `42 * 0.75 + 18 = 49.5` against a limit of 50). Reject once the estimate would exceed the limit. Cloudflare measured 0.003% of 400M requests wrongly allowed or limited, mean rate error 6%.

## Distributed
- Redis with a Lua script so read-modify-write is atomic (or `INCR` + `EXPIRE` for fixed window; the redis.io INCR page wraps them in `MULTI`/`EXEC` because INCR without EXPIRE can leak the key, and shows a Lua `EVAL` variant).
  One extra network hop per request; batch or use local pre-checks for hot paths.
- Local per-instance limits (limit / instance count) are cheap but drift with autoscaling.
- Envoy global rate limit (an external gRPC rate limit service called per request/connection) usually paired with a local token-bucket limit as the coarse first stage; NGINX `limit_req` uses the leaky bucket method and rejects with 503 by default (set `limit_req_status 429`); it does not document sending `Retry-After`, so add it yourself.
- API gateways (Kong), cloud WAF rules.
- Accept slight over-admission under concurrency rather than serialising every request.

## Design choices
- Key: API key/tenant (fair), user, IP (crude: NAT, IPv6 ranges), endpoint.
- Cost-based: expensive endpoints consume more tokens.
- Respond 429 with `Retry-After` (redis-cell's 4th reply element is the seconds until retry, -1 if allowed); log and meter rejections.
- Rate limit (protect from bursts) is different from quota (commercial allocation over days).
