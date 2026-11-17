---
id: computing-software.web-development.web-performance.http2-and-http3-delivery
name: http2-and-http3-delivery
category: computing-software
field: web-development
product: web-performance
tags: [http-caching, http2, http3, quic, multiplexing, performance]
level: practitioner
status: docs-checked
description: "Delivering assets over HTTP/2 and HTTP/3: multiplexing implications for bundling and domain sharding, prioritisation, 103 Early Hints, enabling QUIC with Alt-Svc, and verifying."
sources:
  - https://developer.mozilla.org/en-US/docs/Glossary/HTTP_2
  - https://developer.mozilla.org/en-US/docs/Glossary/HTTP_3
  - https://www.rfc-editor.org/rfc/rfc9114
  - https://developer.chrome.com/docs/web-platform/early-hints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP/2 and HTTP/3 delivery

## 1. What changed from HTTP/1.1
- **Multiplexing**: many requests over one connection, so bundling everything or domain sharding is less necessary.
- **Header compression** (HPACK/QPACK).
- **HTTP/3** runs over QUIC (UDP), specified in RFC 9114.

## 2. Practice changes
- **Stop domain sharding** (`static1.`, `static2.`) - it costs extra connections. Consolidate on the main origin or one CDN host.
- **Bundling**: still bundle (compression ratio, fewer module waterfalls), but finer-grained chunks and route-level splitting are cheap now. Unbundled ESM with deep import chains still suffers request waterfalls - use `modulepreload`.
- **Inlining** small assets matters less; caching separately often wins.
- **HTTP/2 Server Push** has been removed from most major browser engines (MDN); use `<link rel="preload">` and **103 Early Hints**.
- The `fetchpriority` attribute hints relative priority to the browser (web.dev Fetch Priority); some servers/CDNs ignore priorities - test.

## 3. Enable
- HTTP/3: an origin advertises an HTTP/3 endpoint with the `Alt-Svc` response header (or the HTTP/2 ALTSVC frame) using the `h3` ALPN token (RFC 9114); allow UDP traffic to that port. Most CDNs offer a toggle - check yours.

## 4. Pitfalls
- Test both the h2 and h3 paths, since clients may use either.

## Verify
DevTools Network "Protocol" column shows `h2`/`h3`; WebPageTest waterfall shows one connection per origin.

## Checked

2026-10-28. Confirmed from RFC 9114 (HTTP/3 over QUIC; `Alt-Svc` header or ALTSVC frame with the `h3` ALPN token), MDN HTTP/2 glossary (Server Push removed from most major browser engines; replaced by preload and 103 Early Hints) and web.dev Fetch Priority. Removed (not found): the 6-connections figure, Chrome 106 removal, RFC 9218 claim, nginx directives and versions, TLS/OCSP/HSTS advice, 0-RTT and migration claims, UDP-blocking and coalescing pitfalls, the `curl --http3` check.

Method: documentation only; no commands were run.
