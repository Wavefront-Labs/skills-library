---
id: computing-software.collaboration-platform-administration.nextcloud.transactional-file-locking-with-redis
name: transactional-file-locking-with-redis
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [file-locking, memcache-locking, keyvaluecache, phpredis, valkey]
level: advanced
status: docs-checked
description: "Move Nextcloud transactional file locking off the database onto Valkey or Redis through KeyValueCache or phpredis, and know what locking does not do."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/files_locking_transactional.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop file locking from loading your database.

What it does: works above the filesystem (so it needs no filesystem locking support), locks parent directories against rename, releases locks after interrupted transactions such as a sync client losing connection mid-upload, and handles shared files, external storage mounts and encrypted files correctly.

What it is not: it does not stop several users editing the same document or warn them. It only prevents simultaneous saving.

By default locking uses the database backend, which places significant load on it. Setting `memcache.locking` relieves that. Heavy workloads should install a memcache backed by a key-value server such as Valkey or Redis.

Option 1, the `keyvalue` cache. Built on a bundled library, so no PHP module is needed, only a running Valkey or Redis compatible server:

```
'memcache.locking' => '\OC\Memcache\KeyValueCache',
'memcache.kvstore' => [
    'server' => [ 'host' => 'localhost', 'port' => 6379, 'password' => '' ],
],
```

The password is optional. Unix sockets, TLS, Sentinel and cluster setups are covered in the caching page.

Option 2, the `Redis` cache, which needs the phpredis PHP module:

```
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => [ 'host' => 'localhost', 'port' => 6379, 'timeout' => 0.0, 'password' => '' ],
```

Configure the server to require a password if it is reachable beyond the host.

Check: with a cluster, all web servers point at the same key-value server (see memory-cache-choice-by-deployment).

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/files_locking_transactional.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
