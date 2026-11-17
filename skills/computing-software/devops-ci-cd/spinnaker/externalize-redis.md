---
id: computing-software.devops-ci-cd.spinnaker.externalize-redis
name: externalize-redis
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [redis, externalize, caching, spinnaker-yml, gate, keyspace-notifications]
level: advanced
status: docs-checked
description: "Move Spinnaker onto an external Redis, globally or per service via services.redis.baseUrl, and handle hosted Redis that blocks the CONFIG command with Gate keyspace notifications."
sources:
  - https://spinnaker.io/docs/setup/productionize/caching/externalize-redis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default Redis component is not configured to be production-ready, so the page calls an external or hosted Redis one of the easiest ways to improve reliability at scale. It also notes Spinnaker mostly uses SQL at this point.

**Spinnaker-wide Redis.** Determine the endpoint URL, for example `redis://some.redis.url:6379`, with credentials `redis://admin:passw0rd@some.redis.url:6379`, and with a database number `.../1` (database 1). Add it to the common configuration for all services (`spinnaker.yml` in the page's kustomize layout):

```yaml
services:
  redis:
    baseUrl: redis://some.redis.url:6379
    enabled: true
    host: 0.0.0.0
    port: 6379
```

**Per-service Redis** (if one node is overloaded): override `services.redis.baseUrl: $REDIS_ENDPOINT` in the individual service's configuration.

**Hosted Redis.** Gate needs keyspace notifications enabled and tries to configure them at startup. Some hosted services disable the `CONFIG` command. Then set `notify-keyspace-events` to `gxE` on your instance following the provider's documentation, and disable Gate's automatic configuration in `gate-local.yml`:

```yaml
redis:
  configuration:
    secure: true
```

## Checked

2026-11-04. Confirmed against the Externalize Redis page. Removed: the Halyard `service-settings/redis.yml` with `overrideBaseUrl` and `skipLifeCycleManagement`, `hal config generate` verification and `$DEPLOYMENT` notes (the page now edits spinnaker.yml directly).

Method: documentation only; no commands were run.
