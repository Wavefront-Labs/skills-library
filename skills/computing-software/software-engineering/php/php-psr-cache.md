---
id: computing-software.software-engineering.php.php-psr-cache
name: php-psr-cache
category: computing-software
field: software-engineering
product: php
tags: [php, psr-cache, caching]
level: practitioner
status: docs-checked
description: "Use PSR-6 CacheItemPool and PSR-16 SimpleCache: TTLs, key rules, null handling, deferred saves and failure behaviour."
sources: ["https://www.php-fig.org/psr/psr-6/", "https://www.php-fig.org/psr/psr-16/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSR-6 and PSR-16 caching

PSR-16 (`Psr\SimpleCache\CacheInterface`) is the small API: `get`, `set`, `delete`, `clear`, `getMultiple`, `setMultiple`, `deleteMultiple`, `has`. PSR-6 (`Psr\Cache\CacheItemPoolInterface`) hands out `CacheItemInterface` objects via `getItem()`, with `save()`, `saveDeferred()` and `commit()`.

```php
// PSR-16
$user = $cache->get("user.$id");
if ($user === null) {
    $user = $repo->find($id);
    $cache->set("user.$id", $user, new DateInterval('PT10M'));   // ttl: null|int seconds|DateInterval
}
$cache->deleteMultiple(["user.$id", "user.$id.perms"]);

// PSR-6
$item = $pool->getItem("report.$day");
if (!$item->isHit()) {
    $item->set(buildReport($day))->expiresAfter(3600);
    $pool->save($item);
}
$report = $item->get();
```

## Rules from the specs
- Keys: every implementation MUST support `A-Z a-z 0-9 _ .` (UTF-8) up to 64 characters. `{}()/\@:` are reserved and MUST NOT be supported. Hash long or user-provided keys into that alphabet.
- TTL: whole-second granularity is the minimum. With no TTL an implementation may use a configured default, otherwise it caches as long as it can. PSR-16: a zero or negative TTL deletes the item.
- PSR-16 `get($key, $default)` returns the default on a miss; a stored `null` cannot be told apart from a miss. PSR-6 `getItem()` never returns null; use `isHit()` to tell a cached `null` from a miss.
- `has()` is race-prone (PSR-16 recommends it only for cache warming); prefer `get` with a default.
- A value that cannot be returned exactly as saved must become a miss, not corrupted data.
- Deleting a missing key or clearing an empty pool is not an error.
- A cache error should not fail the application: implementations must not throw other than the interface exceptions and should trap backend errors. Keep caching optional in your code too.
- `saveDeferred()` may delay the write; `commit()` persists all deferred items, and a request for a deferred item returns it.

## Gotchas
- Never cache per-user data under a shared key; include tenant and user in the key.
- Serialised objects tie the cache to class definitions; version keys on deploy when shapes change.
- Stampede protection, tagging and backends are implementation features (not in either PSR); check your library's documentation.

Verify: stub the backend as down and confirm requests still succeed.

## Checked

Date: 2026-11-08. Read in full from the php-fig/fig-standards markdown: PSR-6 and PSR-16 (keys, TTL, null/miss, deferred saves, error handling, interfaces). Removed the Symfony Cache callback example, `TagAwareAdapter`, backend list and stampede/probabilistic-expiry statements, and the unread Symfony page source, because those pages were not read.

Method: documentation only; no commands were run.
