---
id: computing-software.collaboration-platform-administration.mattermost.rate-limiting-settings
name: rate-limiting-settings
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [rate-limiting, api-throttling, reverse-proxy, config-settings]
level: practitioner
status: docs-checked
description: "Mattermost rate limiting settings: enable flag, queries per second, burst, memory store, vary-by options and proxy headers with defaults."
sources: ["https://docs.mattermost.com/administration-guide/configure/rate-limiting-configuration-settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rate limiting settings

Rate limiting throttles API access on self-hosted servers to protect against overload and abusive third-party clients. It is meant for small deployments of up to a few hundred users, not Enterprise scale. Configure it in System Console > Environment > Rate Limiting or in config.json under RateLimitSettings; changes need a server restart.

Settings and defaults:
- Enable rate limiting (RateLimitSettings.Enable, MM_RATELIMITSETTINGS_ENABLE): false by default, so no throttling.
- Maximum queries per second (PerSec): 10. Raise to accept more requests per second, lower to allow fewer.
- Maximum burst size (MaxBurst): 100 requests allowed beyond the per-second limit.
- Memory store size (MemoryStoreSize): 10000 sessions. Set it near the expected number of users; higher wastes resources, lower makes sessions or tokens expire too often.
- Vary rate limit by remote address (VaryByRemoteAddr): true by default; limits by IP and is recommended behind a proxy.
- Vary rate limit by user (VaryByUser): false by default; true limits by authentication token.
- Vary rate limit by HTTP header (VaryByHeader): empty by default; names the header that identifies the client when behind a proxy. For NGINX use X-Real-IP; for Amazon ELB use X-Forwarded-For.

Each setting also has a MM_RATELIMITSETTINGS_* environment variable (for example MM_RATELIMITSETTINGS_VARYBYHEADER).

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/configure/rate-limiting-configuration-settings (defaults, env vars, NGINX and ELB headers). Removed the unsupported shared-bucket explanation.

Method: documentation only; no commands were run.
