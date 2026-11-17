---
id: computing-software.collaboration-platform-administration.nextcloud.memory-cache-choice-by-deployment
name: memory-cache-choice-by-deployment
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [memcache, apcu, redis, memcached, file-locking]
level: practitioner
status: docs-checked
description: "Pick Nextcloud memcache.local, memcache.distributed and memcache.locking backends for a home server, single server or cluster, and keep shared caches pointed at one server."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set the three cache keys that match your deployment.

Opcache (compiled PHP) comes bundled; the data cache is yours to configure. A memcache is not required, and the warning may be ignored. Enabling only a distributed cache without a local one still shows the warning.

Backends: APCu (local), Redis (local, distributed and locking; Valkey and KeyDB are expected to work), Memcached (distributed).

Small or home server, APCu only:

```
'memcache.local' => '\OC\Memcache\APCu',
```

Single server organisation, Redis for everything except local:

```
'memcache.local' => '\OC\Memcache\APCu',
'memcache.distributed' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => [ 'host' => 'localhost', 'port' => 6379 ],
```

Cluster: APCu local, plus either `redis.cluster` with `seeds` listing some servers and the port, or Memcached with `memcached_servers` for distributed and locking.

With several web servers, the distributed and locking settings must point at the very same cache server or cluster, never `localhost` or a unix socket.

APCu is faster than Redis locally. With enough memory use APCu for caching and Redis for file locking; when short on memory use Redis for both.

Check: after enabling the cache and restarting the web server, view `phpinfo` to confirm the module is active and refresh the admin page to see the warning clear.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
