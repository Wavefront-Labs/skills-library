---
id: computing-software.web-development.web-performance.streaming-html-and-early-flush
name: streaming-html-and-early-flush
category: computing-software
field: web-development
product: web-performance
tags: [html-streaming, early-flush, chunked-transfer, ttfb, streaming-ssr]
level: advanced
status: docs-checked
description: "Streaming HTML and flushing the head early: chunked responses, sending head and critical links before slow data, streaming SSR, proxy buffering pitfalls and verifying in DevTools."
sources:
  - https://web.dev/articles/optimize-ttfb#use_streaming
  - https://react.dev/reference/react-dom/server/renderToPipeableStream
  - https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming HTML and flushing the head early

Browsers parse HTML incrementally. If the server sends `<head>` (CSS, preloads, fonts) immediately and the slow body later, the browser downloads critical resources during server think time.

## 1. Early flush
```js
// Node/Express
app.get("/product/:id", async (req, res) => {
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.write(`<!doctype html><html><head><link rel="stylesheet" href="/app.css">
    <link rel="preload" as="image" href="/hero.avif" fetchpriority="high"></head><body>${header}`);
  const product = await db.product(req.params.id);       // slow part
  res.end(renderProduct(product) + "</body></html>");
});
```
Commit the status code and headers before flushing: once bytes are sent you can't change to a 404/redirect. Decide status first (cheap existence check), or render errors in-page.

## 2. Streaming SSR in frameworks
- React: `renderToPipeableStream` / `renderToReadableStream` with `<Suspense>` boundaries; shell flushes first, boundaries stream in with inline scripts. `onShellReady` to start piping for users, `onAllReady` for crawlers if needed.

## 3. Things that silently buffer
| Layer | Fix |
|---|---|
| nginx `proxy_buffering on` | `X-Accel-Buffering: no` header or `proxy_buffering off` for the route |

## 4. Verify the stream
In the DevTools waterfall the CSS request should start before the HTML finishes downloading.

## Verify
- [ ] Head with critical resources arrives before the slow data; CSS and LCP image requests start before HTML completes; no proxy buffering on streamed routes.

## Checked

2026-10-28. Confirmed from the React `renderToPipeableStream` page (`renderToReadableStream` for web-stream runtimes, `onShellReady`, `onAllReady`) and the nginx `proxy_buffering` docs (`X-Accel-Buffering` header turns buffering on or off per response). Removed (not found in the pages): framework streaming claims, Rails/Django/PHP snippets, compression, CDN, serverless and rewriter rows, the curl command and the 100-200 ms figure.

Method: documentation only; no commands were run.
