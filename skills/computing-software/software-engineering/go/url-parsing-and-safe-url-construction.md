---
id: computing-software.software-engineering.go.url-parsing-and-safe-url-construction
name: url-parsing-and-safe-url-construction
category: computing-software
field: software-engineering
product: go
tags: [go, go-http-client, go-url-parsing, net-url, url-parse, query-escape]
level: practitioner
status: docs-checked
description: "Parse and build URLs in Go with net/url: Parse vs ParseRequestURI, query encoding, path escaping, JoinPath and allow-list validation."
sources:
  - https://pkg.go.dev/net/url
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# net/url parsing and safe construction

**Goal:** no string concatenation for URLs, and no surprises from lenient parsing.

```go
u, err := url.Parse("https://api.example.com/v1/items?n=1")
q := u.Query()          // url.Values parsed from RawQuery
q.Set("q", "go & rust")
u.RawQuery = q.Encode() // "URL encoded" form, sorted by key
base, _ := url.Parse("https://api.example.com/v1/")
next := base.JoinPath("items", url.PathEscape(userID)) // Go 1.19; elements must already be escaped
esc := url.PathEscape("a/b c")                         // escapes "/" too, giving a%2Fb%20c
```

`url.Parse` accepts relative or absolute URLs; parsing a hostname and path without a scheme is invalid but may not return an error. `ParseRequestURI` assumes the string came from an HTTP request, so it accepts only an absolute URI or an absolute path and no `#fragment`. After parsing, check `u.Scheme` and `u.Host` yourself. `u.Hostname()` returns the host with any valid port stripped. `JoinPath` cleans `./` and `../` elements and collapses repeated `/`. `Path` and `Fragment` are stored decoded; use `EscapedPath` / `EscapedFragment` for the original encoding.

For server-side fetches of user-supplied URLs (webhooks, image proxies), validate scheme and host against an allow-list before fetching; `net/url` only parses and does not check where a URL points.

## Gotchas
- `Query()` silently discards malformed value pairs; `url.ParseQuery` returns the first decoding error.
- Because `Path` is decoded, `%2f` and `/` cannot be told apart in it; use `EscapedPath` when that matters.
- `JoinPath` does not escape its arguments: pass user-controlled segments through `url.PathEscape` first.

## Verify
Table-test hostile inputs such as `//evil.com` and `http://a@b` through your validator and assert its decisions.

## Checked
2026-11-03. Confirmed on pkg.go.dev/net/url: `Parse` and `ParseRequestURI` semantics, `Query`, `ParseQuery`, `Values.Encode` ordering, `JoinPath` (go1.19, requires escaped elements), `PathEscape`, `Hostname`, decoded `Path` and `Fragment`. Corrected: JoinPath does not escape. Removed: `net.Dialer.Control` SSRF recipe, redirect re-check, control-character-since-Go-1.12 claim, `u.String()` re-encoding advice, "User and Fragment never sent" claim, the `127.0.0.1:80@evil.com` test case.
Method: documentation only; no commands were run.
