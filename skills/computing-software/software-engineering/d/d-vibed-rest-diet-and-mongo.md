---
id: computing-software.software-engineering.d.d-vibed-rest-diet-and-mongo
name: d-vibed-rest-diet-and-mongo
category: computing-software
field: software-engineering
product: d
tags: [d-vibed-rest-diet-and-mongo, ecosystem-vibed, vibe-d-rest, diet-templates, registerrestinterface, websocket, session, mongodb, redis, ddbc, mysql-native, vibe-web, d]
level: advanced
status: draft
description: "Generate REST APIs from D interfaces (@path, @method), render Diet (.dt) templates, use sessions and WebSockets, and talk to Mongo, Redis, SQL (ddbc, mysql-native) from vibe.d."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vibe.d REST interfaces, Diet templates, sessions and database access

Goal: structure a larger vibe.d app.

- REST: `@path("/api") interface IApi { @method(HTTPMethod.GET) string[] getItems(); @path("items/:id") Item getItem(int _id); }` implement as a class, `router.registerRestInterface(new Api);`; `vibe.web.rest` also builds typed clients (`new RestInterfaceClient!IApi("http://...")`) and generates OpenAPI JSON.
- Web interface: `vibe.web.web` `registerWebInterface(router, new Web)` maps methods to routes; `@auth`, `@before`, `@errorDisplay` attributes; `render!("index.dt", user)` Diet template (indentation syntax, `#{expr}` interpolation, `include`/`extends`/`block`).
- Sessions: `res.startSession()`, `req.session.set("k", v)`; store `MemorySessionStore` or `RedisSessionStore`.
- WebSockets: `handleWebSockets((scope ws) { while (ws.waitForData()) ws.send(ws.receiveText); })`.
- Data: `vibe.db.mongo`, `vibe.db.redis`; SQL: `ddbc`, `mysql-native`, `postgresql-d` through dub; use `vibe.core.connectionpool` for pooling.
- Serialisation: `vibe.data.json` (`serializeToJson`, `deserializeJson!T`) and `vibe.data.serialization` with `@name`, `@optional` attributes.
- Logging: `logInfo`, `setLogLevel(LogLevel.diagnostic)`.

Gotchas:
- Mixed blocking DB drivers need `runWorkerTask`.
- Diet templates compile into the binary; template errors appear as long compile errors.

Verify: integration test with `curl` and `dub test` using vibe's `listenHTTP` on a random port.
