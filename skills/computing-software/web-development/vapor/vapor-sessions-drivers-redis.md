---
id: computing-software.web-development.vapor.vapor-sessions-drivers-redis
name: vapor-sessions-drivers-redis
category: computing-software
field: web-development
product: vapor
tags: [vapor,sessions,sessionsmiddleware,redis,valkey,fluent,cookies,swift]
level: practitioner
status: docs-checked
description: "Add SessionsMiddleware to Vapor, pick a session driver (memory, Fluent, Redis, Valkey), and customise Redis storage with RedisSessionsDelegate."
sources:
  - https://docs.vapor.codes/advanced/sessions/
  - https://docs.vapor.codes/valkey/sessions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: persist per-user data across requests with a session cookie.

Sessions suit HTML front ends; for APIs the docs recommend stateless token authentication.

**Middleware.** Requests must pass `SessionsMiddleware`. Configure the driver first, because `Sessions` is a value type and must be set before the middleware is used.

```swift
app.middleware.use(app.sessions.middleware)
// or only for a subset:
let sessions = app.grouped(app.sessions.middleware)
```

Cookie config: `app.sessions.configuration.cookieName = "foo"` (default name `vapor_session`) and `cookieFactory = { sessionID in .init(string: sessionID.string, isSecure: true) }`.

**Drivers** (custom ones conform to `SessionDriver`; configure before adding the middleware):

- `app.sessions.use(.memory)`: default, zero config, lost on restart.
- Fluent: `app.sessions.use(.fluent)` or `.fluent(.sqlite)`, then `app.migrations.add(SessionRecord.migration)` and run migrations (table `_fluent_sessions`).
- Redis: `import Redis`, `app.sessions.use(.redis)`.
- Valkey: set `app.valkey = ValkeyClient(.hostname("localhost"), eventLoopGroup: app.eventLoopGroup, logger: app.logger)`, then `app.sessions.use(.valkey())` (imports Valkey, Vapor, VaporValkey).

**Using data.** Writing to `req.session.data` creates the session and sets the cookie:

```swift
req.session.data["name"] = req.parameters.get("value")
req.session.data["name"] ?? "n/a"
req.session.destroy()   // deletes data, invalidates cookie
```

**Redis defaults.** Session IDs: 32 random bytes, base64-encoded. Data: JSON string via `Codable`, under key `vrs-` + session ID.

**Custom Redis storage.** Implement `RedisSessionsDelegate`; required methods are `redis(_:store:with:)` and `redis(_:fetchDataFor:)` (reading and writing must match). Optional overrides: `makeNewID()`, `makeRedisKey(for:)`. Register with `app.sessions.use(.redis(delegate: CustomRedisSessionsDelegate()))`. The docs' hash example stores with `client.hmset(data.snapshot, in: key)` and reads with `client.hgetall(from: key)`.

## Checked

2026-11-08: read in full the Sessions page at docs.vapor.codes/advanced/sessions/ and the Sessions with Valkey/Redis page at docs.vapor.codes/valkey/sessions/ (middleware, cookie defaults, drivers, Redis defaults, RedisSessionsDelegate). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
