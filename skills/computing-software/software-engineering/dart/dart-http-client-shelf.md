---
id: computing-software.software-engineering.dart.dart-http-client-shelf
name: dart-http-client-shelf
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-http, http-client-shelf]
level: practitioner
status: docs-checked
description: "Make HTTP requests with status checks, a reused Client and RetryClient, and build small servers with shelf."
sources: ["https://dart.dev/server/fetch-data", "https://pub.dev/packages/http", "https://pub.dev/packages/shelf", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# package:http client and shelf servers
- Build URLs with `Uri.parse(...)` or `Uri.https('host', '/path', {'q': 'x y'})` (the `http`/`https` constructors take a query-parameter map and encode it). Check `response.statusCode != 200` yourself and raise a typed exception, as the Dart fetch-data tutorial does.
- Create one `http.Client()` for repeated requests, and `close()` it in a `finally` block. Inject the client (`client ?? http.Client()`) so tests can pass a `MockClient`.
- `RetryClient(http.Client())` retries 503 responses up to three times by default, waiting 500 ms before the first retry and increasing the delay by 1.5x each time; both are configurable.
- Under the Dart SDK, `runWithClient` selects the client when you cannot pass it explicitly, and must be called again in each spawned isolate (isolates do not inherit the calling zone).
- shelf: `const Pipeline().addMiddleware(logRequests()).addHandler(handler)` and `shelf_io.serve(handler, 'localhost', 8080)`. Middleware wraps a handler to add behaviour; `shelf_router` and `shelf_static` are packages built on shelf.
- Do not trust request input; validate it and set size limits (judgement, not from these pages).

Verify: with `MockClient`, return a 404 and confirm your code raises its typed exception.

## Checked

Checked 2026-11-08 against https://dart.dev/server/fetch-data (status-code, Client and RetryClient sections), the pub.dev pages of http and shelf, and the Uri section of https://dart.dev/libraries/dart-core. Removed (not confirmed): the `.timeout(Duration(seconds: 10))` example, the claim that package:http never throws on 4xx/5xx, the `shelf_router` Router wiring and the direct `handler(Request(...))` test recipe.

Method: documentation only; no commands were run.
