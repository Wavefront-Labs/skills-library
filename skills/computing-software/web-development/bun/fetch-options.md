---
id: computing-software.web-development.bun.fetch-options
name: fetch-options
category: computing-software
field: web-development
product: bun
tags: [bun-fetch, fetch-proxy, fetch-unix-socket, fetch-session]
level: advanced
status: docs-checked
description: "Use Bun-specific fetch options: proxy and NO_PROXY, unix sockets, tls and checkServerIdentity, streaming bodies, connection limits, preconnect and FetchSession."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/networking/fetch.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
await fetch(url, { signal: AbortSignal.timeout(1000) });
await fetch("https://example.com", {
  proxy: { url: "http://proxy.com", headers: { "Proxy-Authorization": "Bearer t" } },
  decompress: true, keepalive: false,
});
await fetch("https://hostname/a/path", { unix: "/var/run/app.sock", method: "POST", body: "{}" });
const session = new Bun.FetchSession({ keepAlive: { idleTimeout: 30, maxIdleSockets: 8 } });
await session.fetch("https://example.com"); session.close();
await Bun.write("out.txt", await fetch(url));
```

- Without `proxy`, Bun reads `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`; `NO_PROXY` bypasses hosts, IPs, CIDRs or ports. `proxy: false` connects directly; `respectNoProxy: false` forces the proxy. A non-2xx CONNECT answer rejects with `ERR_PROXY_TUNNEL`.
- `verbose: true` or `"curl"` logs headers. `file://`, `data:`, `blob:` and `s3://` URLs work.
- Default cap is 256 simultaneous requests; raise with `BUN_CONFIG_MAX_HTTP_REQUESTS` (max 65,535).
- `fetch.preconnect(url)` / `--fetch-preconnect` only helps if there is a gap before the real request.

Gotchas: a body on GET or HEAD throws; `proxy` plus `unix` throws; URL credentials become a Basic header; `checkServerIdentity` must be a function and returns `undefined` to approve (async approves nothing); connecting by IP with a `Host` header needs `proxy: false`, `redirect: "manual"` and `tls.serverName`.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/networking/fetch: proxy as string or object with headers, HTTP_PROXY/HTTPS_PROXY/ALL_PROXY and NO_PROXY handling with respectNoProxy and proxy:false, ERR_PROXY_TUNNEL on non-2xx CONNECT, unix option, proxy plus unix throwing, body on GET/HEAD throwing, URL credentials becoming a Basic header, checkServerIdentity semantics (undefined approves, async function approves nothing, must be a function), decompress/keepalive/verbose options, file/data/blob/s3 URL support, 256 request cap and BUN_CONFIG_MAX_HTTP_REQUESTS max 65,535, preconnect advice, FetchSession keepAlive options, and the connect-by-address requirements (proxy:false, redirect manual, tls.serverName). Nothing removed.
Method: documentation only; no commands were run.
