---
id: computing-software.cybersecurity-defensive.network-defence.rate-limiting-for-dos-protection
name: rate-limiting-for-dos-protection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-mitigation, rate-limiting, nginx-limit-req, waf-rate-rules, api-gateway-throttling, token-bucket, application-layer-ddos, credential-stuffing]
level: practitioner
status: draft
description: "Apply rate limiting at the edge, load balancer and application to absorb layer-7 floods and abuse: algorithms, keys, limits, responses and bypass for trusted clients."
sources: ["CompTIA Security+ SY0-701 objective 2.4 (DDoS)", "NGINX documentation - Limiting access to proxied HTTP resources (limit_req)", "AWS WAF rate-based rules documentation", "OWASP API Security Top 10 API4:2023 Unrestricted Resource Consumption"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rate limiting for DoS protection

**Goal:** a flood of requests from a few sources, or expensive requests from anyone, cannot
exhaust your application, while normal users never notice.

## Layers
1. **CDN/WAF edge** (Cloudflare, AWS WAF, Azure Front Door, Akamai): rate-based rules per IP or per header/cookie; cheapest place to drop traffic.
2. **Load balancer / reverse proxy** (NGINX, HAProxy, Envoy): per-IP and per-route limits.
3. **API gateway**: per API key/client quotas and burst limits.
4. **Application**: per user/account for sensitive actions (login, password reset, OTP, search, export).

## NGINX example
```
limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
server {
  location / { limit_req zone=perip burst=20 nodelay; }
  location = /login { limit_req zone=login burst=5; limit_req_status 429; }
}
```
Token-bucket style: `rate` is the sustained rate, `burst` absorbs short spikes.

## AWS WAF rate-based rule
Limit 2,000 requests per 5 minutes per IP (the evaluation window is configurable), scope-down
statement to `/login` with a much lower limit; action Block or CAPTCHA/Challenge.

## Choosing keys and limits
- Per IP is easy but weak against botnets and unfair for NAT/CGNAT users; add per-session, per-account or per-API-key limits.
- Set limits from observed p99 traffic per key, with headroom; start in count/log mode.
- Return `429 Too Many Requests` with `Retry-After`.
- Exempt health checks and known partners by authenticated identity, not by IP alone.

## Gotchas
- Rate limits keyed on `X-Forwarded-For` are spoofable unless the header is set by your own trusted proxy.
- Distributed limits across many instances need a shared store (Redis) or edge enforcement, otherwise each node allows the full rate.
- Expensive endpoints (search, report generation) need concurrency limits, not just request rates.

## Verify
- [ ] Load test from one source exceeds the limit and receives 429s; normal traffic unaffected.
- [ ] Rate-limit hits logged and visible on a dashboard during incidents.
