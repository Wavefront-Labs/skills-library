---
id: computing-software.cloud-infrastructure-engineering.contour.contour-global-rate-limit-deployment-guide
name: contour-global-rate-limit-deployment-guide
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [global-rate-limit, envoyproxy-ratelimit, redis, extensionservice, h2c, ratelimit-config, defaultglobalratelimitpolicy]
level: advanced
status: docs-checked
description: "Deploying a global rate limit service with Contour: envoyproxy/ratelimit config, ExtensionService h2c, rateLimitService config, default global policy, opt-out, 429s."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/global-rate-limiting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global rate limiting: deploying an RLS

Guide demo (not production-ready): Envoy's `envoyproxy/ratelimit` backed by Redis.

1. RLS config (ConfigMap mounted at `/data/ratelimit/config`), with `domain` matching Contour's:

```yaml
domain: contour
descriptors:
- key: generic_key
  value: foo
  rate_limit: {unit: minute, requests_per_unit: 1}
- key: remote_address
  rate_limit: {unit: minute, requests_per_unit: 3}
```

2. RLS container env: `RUNTIME_ROOT=/data`, `RUNTIME_SUBDIRECTORY=ratelimit`, `RUNTIME_WATCH_ROOT=false`, `REDIS_SOCKET_TYPE=tcp`, `REDIS_URL=localhost:6379`, and `RUNTIME_IGNOREDOTFILES=true` (needed because of how Kubernetes mounts ConfigMaps). Service exposes gRPC 8081.
3. ExtensionService with `protocol: h2c` (plaintext) and a tight `timeoutPolicy.response: 100ms`.
4. Config file `rateLimitService` with `extensionService: projectcontour/ratelimit`, `domain`, `failOpen`; then `kubectl -n projectcontour rollout restart deploy/contour`.

Default policy for all vhosts (single-tenant convenience):

```yaml
rateLimitService:
  defaultGlobalRateLimitPolicy:
    descriptors:
    - entries:
      - requestHeader: {headerName: X-Custom-Header, descriptorKey: CustomHeader}
```

A vhost opts out with `rateLimitPolicy.global.disabled: true`; defining its own `global` descriptors replaces the default rather than adding to it.

Behaviour: every matching limit is applied per request, and rejected (429) requests still count against limits. With the demo config, a second request to `/foo` within a minute returns 429 (generic_key limit), and the fourth request from one IP returns 429 (remote_address limit).

## Checked

2026-11-04. Confirmed against the Contour global rate limiting guide (guides/global-rate-limiting.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
