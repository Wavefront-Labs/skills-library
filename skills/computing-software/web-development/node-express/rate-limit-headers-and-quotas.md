---
id: computing-software.web-development.node-express.rate-limit-headers-and-quotas
name: rate-limit-headers-and-quotas
category: computing-software
field: web-development
product: node-express
tags: [ratelimit-headers, api-quotas, retry-after, express-rate-limit, api-design]
level: practitioner
status: verified
description: "Communicating API rate limits: IETF RateLimit and RateLimit-Policy headers, legacy X-RateLimit headers, 429 with Retry-After, per-key quotas, and backoff."
sources:
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
  - https://www.rfc-editor.org/rfc/rfc6585#section-4
  - https://express-rate-limit.mintlify.app/reference/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limit headers and quotas

## 1. Headers
| Header | Meaning |
|---|---|
| `RateLimit-Policy: "default";q=100;w=60` | IETF draft: policy name, quota per window (seconds) |
| `RateLimit: "default";r=37;t=21` | remaining requests and seconds until reset |
| `X-RateLimit-Limit / -Remaining / -Reset` | widespread legacy convention (GitHub, Twitter); Reset is often an epoch timestamp - document which |
| `Retry-After: 21` | on 429 (and 503): seconds (or HTTP date) before retrying |

With express-rate-limit 8.7 the real output differs from the table in detail: `standardHeaders: "draft-8"` sends `RateLimit: "3-in-1min"; r=2; t=60` and `RateLimit-Policy: "3-in-1min"; q=3; w=60; pk=:...:` (the policy name defaults to `<limit>-in-<window>`, and a `pk` partition key is added; the name "default" in the table is only an example); `draft-7` sends `RateLimit: limit=2, remaining=1, reset=60` and `RateLimit-Policy: 2;w=60`; `draft-6` sends separate `RateLimit-Limit/-Remaining/-Reset`; `legacyHeaders: true` adds `X-RateLimit-*` with an epoch-seconds reset. The 429 response carries `Retry-After: 60`. Older drafts used separate `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` headers; many libraries still emit those. Pick one format, document it, and keep it stable.

## 2. Express
```js
import { rateLimit, ipKeyGenerator } from "express-rate-limit";
import { RedisStore } from "rate-limit-redis";
app.set("trust proxy", 1);                                  // correct client IPs behind one proxy
const apiLimiter = rateLimit({
  windowMs: 60_000,
  limit: (req) => req.apiKey?.plan === "pro" ? 1000 : 100,  // per-plan quotas
  keyGenerator: (req) => req.apiKey?.id ?? ipKeyGenerator(req.ip),   // per key, fallback per IP; v8 warns (ERR_ERL_KEY_GEN_IPV6) if raw req.ip is used
  standardHeaders: "draft-8",                               // RateLimit + RateLimit-Policy
  legacyHeaders: false,
  store: new RedisStore({ sendCommand: (...a) => redis.sendCommand(a) }),
  handler: (req, res, next, opts) => res.status(429).type("application/problem+json")
    .json({ type: "about:blank", title: "Too Many Requests", status: 429, detail: "Rate limit exceeded" }),
});
app.use("/api", apiLimiter);
```
- Shared store (Redis) for multiple instances; memory store is per process.
- Gateways (Kong, Envoy, API Gateway, Cloudflare) can enforce limits before traffic reaches Node.

## 3. Designing quotas
- Short window rate (burst control) plus longer quota (daily/monthly) for paid tiers; return the policy most likely to be hit.
- Token bucket or sliding window algorithms avoid the "double burst" at fixed-window boundaries.
- Separate, stricter limits for expensive endpoints (search, exports) and auth endpoints.
- Don't count requests rejected for auth failures against a customer's quota, but do rate-limit them per IP.

## 4. Client behaviour
Respect `Retry-After`; exponential backoff with jitter; read remaining counts to self-throttle. Document headers and limits in the OpenAPI spec (`429` responses with header schemas).

## Verify
- [ ] Responses carry rate limit headers; 429 includes Retry-After and a JSON body; limits consistent across instances; per-plan quotas enforced in tests.

## Checked
Run on Windows with Node 20.20.2, Express 4.22.3 and express-rate-limit 8.7.1 (in-memory store): a limit of 3 per minute returned 200, 200, 200, then 429 `application/problem+json` with `Retry-After` and the problem body from the custom handler; a per-plan `limit` function gave a pro key 1000; keyed limits per `x-key`; header output of draft-6 (with legacy), draft-7 and draft-8 as quoted above; without `trust proxy` a spoofed `X-Forwarded-For` shared the same bucket. Not run: `RedisStore`, multiple instances, gateways, sliding-window algorithms, client backoff, OpenAPI documentation. The library is pure JavaScript; not run on Linux.
