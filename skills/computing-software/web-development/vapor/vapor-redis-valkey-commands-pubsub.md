---
id: computing-software.web-development.vapor.vapor-redis-valkey-commands-pubsub
name: vapor-redis-valkey-commands-pubsub
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-redis, redis, valkey, pubsub, redistack, valkey-swift, cache]
level: practitioner
status: docs-checked
description: "Configure Redis (RediStack) or Valkey in Vapor, tune the connection pool, send commands, and subscribe to pub/sub channels."
sources:
  - https://docs.vapor.codes/valkey/redis/
  - https://docs.vapor.codes/valkey/valkey/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: connect a Vapor app to Redis or Valkey, run commands, and use pub/sub.

## Redis (RediStack)
Package:

```swift
.package(url: "https://github.com/vapor/redis.git", from: "4.0.0")
// target: .product(name: "Redis", package: "redis")
```

Configure (minimum is a host or URL):

```swift
app.redis.configuration = try RedisConfiguration(hostname: "localhost")
```

- Several endpoints (e.g. a cluster): pass a `[SocketAddress]` built with `.makeAddressResolvingHost(_:port:)`. For one endpoint use `.init(url:pool)` or `.init(hostname:port:password:database:pool:)`.
- `password`: each new connection authenticates with it.
- `database`: selected when each connection is created, so you need not send SELECT. The selection is not maintained, so be careful sending SELECT yourself.
- Pool options (`RedisConfiguration.PoolOptions`): `minimumConnectionCount` is how many connections each pool keeps; with 0, lost connections are only recreated when needed (a "cold start" with some overhead). `maximumConnectionCount` controls the maximum, see `RedisConnectionPoolSize`.

Commands via `.redis` on `Application` or `Request`:

```swift
let value = try await app.redis.get("my_key", as: String.self)   // Optional("my_value")
```

(Blocking `.wait()` and future styles also exist.) Commands without an extension method can be sent raw, each value after the command being a positional argument:

```swift
let res = try await app.redis.send(command: "PING", with: ["hello"])   // "hello"
```

Pub/sub lifecycle: subscribe (once at start), message (0+ times), unsubscribe (once at end, by request or lost connection). You must supply a `messageReceiver`; `onSubscribe` and `onUnsubscribe` handlers are optional. `app.redis.subscribe` takes `to:` channel names, `messageReceiver: { channel, message in ... }` and optionally `onUnsubscribe: { channel, subscriptionCount in ... }`.

## Valkey
Valkey is a Redis v7.2.4 fork; the `VaporValkey` integration (driver: valkey-swift) also talks to Redis up to 7.2.4.

```swift
.package(url: "https://github.com/vapor/valkey.git", from: "1.2.0"),
.package(url: "https://github.com/valkey-io/valkey-swift.git", from: "1.0.0"),
// target: .product(name: "VaporValkey", package: "VaporValkey"), .product(name: "Valkey", package: "valkey-swift")
```

```swift
import Valkey; import Vapor; import VaporValkey
app.valkey = ValkeyClient(.hostname("localhost"), eventLoopGroup: app.eventLoopGroup, logger: app.logger)
```

Assigning `app.valkey` makes the Application own the client: it runs the client and pool and cancels them at shutdown. It accepts `ValkeyClient` or `ValkeyClusterClient`.

```swift
try await app.valkey.set("mykey", value: "myvalue")
let value: RESPBulkString? = try await app.valkey.get("my_key")
```

Pub/sub as an `AsyncSequence`; leaving the closure sends UNSUBSCRIBE:

```swift
try await app.valkey.publish(channel: "channel", message: "Hello, World!")
try await app.valkey.subscribe(to: ["channel"]) { subscription in
    for try await item in subscription {
        print(item.channel); print(String(item.message))
    }
}
```

## Checked

2026-11-08: read in full the Redis and Valkey pages at docs.vapor.codes/valkey/redis/ and /valkey/valkey/ (package snippets, RedisConfiguration options, pool options, send(command:with:), pub/sub lifecycle, ValkeyClient setup, subscribe(to:)). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
