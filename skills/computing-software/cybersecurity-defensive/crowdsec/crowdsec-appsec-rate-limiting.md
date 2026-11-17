---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-appsec-rate-limiting
name: crowdsec-appsec-rate-limiting
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [appsec-rate-limit, ratelimit-helper, pre-eval, token-bucket, http-429]
level: advanced
status: docs-checked
description: "Rate limit endpoints inside the CrowdSec WAF with the RateLimit helper in pre_eval hooks."
sources: ["https://docs.crowdsec.net/docs/appsec/rate_limiting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`RateLimit(key, limit, source?)` is available in `pre_eval` hooks and runs before any rule is evaluated.

```yaml
name: custom/my-appsec-config
inband:
  pre_eval:
    - filter: req.URL.Path == "/login" && req.Method == "POST"
      apply:
        - RateLimit("login", "5/m")
```

The first five requests per minute per client pass (and then go through normal rules); extra requests are blocked with HTTP **429**.

## Arguments

- `key`: a string literal naming the limiter. It must be unique: one `RateLimit()` call per key across the top level, `inband` and `outofband`. Each key has an independent budget per client. To share a budget across endpoints use one call with a broader filter, for example paths in a list.
- `limit`: `<count>/<unit>` with unit `s`, `m` or `h`; a positive integer count and a single unit (`1/5m` and `10/d` are invalid). Also a literal.
- `source` (optional): what to count on. Default is the client IP; IPv4 per address, IPv6 per `/64`. Pass something else such as `req.Header.Get("X-Api-Key")` for a budget per API key. If the value is empty the IP is used. Only use a value the client cannot freely change, because each distinct value consumes memory until it expires.

An invalid limit, non-literal argument or duplicate key stops the AppSec datasource from starting with an explicit error.

## Behaviour

It is a token bucket: `3/m` allows 3 at once, the fourth is blocked, and a token returns every 20 seconds. Over the limit, rule evaluation stops, the bouncer is told to apply `ban`, and the user always sees 429 regardless of `user_blocked_http_code`. Limiters are in memory only and reset on restart or reload. Rate limiting applies to the in-band phase only: declare `RateLimit()` under `inband.pre_eval`, because calls reached out-of-band do nothing.

## Checked

2026-11-03. Confirmed against the AppSec Rate Limiting page: helper signature, 5/m example and 429, key and limit rules, source default (IP, IPv6 /64) and empty-value fallback, token bucket 3/m example, 429 regardless of user_blocked_http_code, in-memory limiters, startup errors. Added: the in-band-only rule from the page.

Method: documentation only; no commands were run.
