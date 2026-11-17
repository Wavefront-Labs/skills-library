---
id: computing-software.software-engineering.go.draining-and-closing-response-bodies
name: draining-and-closing-response-bodies
category: computing-software
field: software-engineering
product: go
tags: [go, go-http-client, go-http-body-drain, response-body, connection-reuse, keep-alive]
level: practitioner
status: docs-checked
description: "Close and drain Go http.Response bodies so keep-alive connections can be reused."
sources:
  - https://pkg.go.dev/net/http#Client.Do
  - https://pkg.go.dev/net/http#Transport
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Draining and closing response bodies

**Goal:** keep-alive connections get reused, descriptors do not leak.

If the error from `Client.Do` is nil, the `Response` has a non-nil `Body` that the caller is expected to close. If the body is not both **read to EOF** and **closed**, the transport may not be able to reuse the persistent TCP connection for a later keep-alive request. The `Transport` automatically tries to read a body to EOF asynchronously, up to a conservative limit, when it is closed.

```go
resp, err := client.Do(req)
if err != nil { return err }   // resp is not usable on error
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body) // reads to EOF
```

If a `CheckRedirect` hook returns `http.ErrUseLastResponse`, the most recent response is returned with its body unclosed, so you must close it.

## Gotchas
- A body left unread and unclosed can stop the connection being reused; close on every path, including non-2xx responses.
- `Transport.MaxIdleConnsPerHost` defaults to `DefaultMaxIdleConnsPerHost` (2); raise it for services calling one host heavily.
- A `Client`'s `Transport` holds cached TCP connections, so reuse one `Client` rather than creating one per request; clients are safe for concurrent use.

## Verify
Under a loop of many requests the number of established connections to the host stays small instead of growing.

## Checked
2026-11-03. Confirmed on pkg.go.dev/net/http (Client.Do body rules, async read up to a conservative limit, `ErrUseLastResponse`, `DefaultMaxIdleConnsPerHost = 2`, Client reuse). Removed: `io.LimitReader` bounded drain, json.Decoder trailing-data claim, HTTP/2 stream reset claim, goroutine dump signature, `ss`/`httptrace` verification.
Method: documentation only; no commands were run.
