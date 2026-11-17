---
id: computing-software.web-development.node-express.debugging-cors-errors
name: debugging-cors-errors
category: computing-software
field: web-development
product: node-express
tags: [cors, cors-errors, debugging, devtools, fetch]
level: practitioner
status: verified
description: "Diagnosing CORS errors from the browser console: reading the exact message, checking preflight and actual responses, opaque errors, proxies, and fixes that are not wildcards."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors
  - https://developer.chrome.com/docs/devtools/network/reference
  - https://fetch.spec.whatwg.org/#http-cors-protocol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging CORS errors

CORS errors are enforced by the browser on the **response**; the server usually received and processed the request. JS gets only `TypeError: Failed to fetch` - the reason is in the console.

## 1. Read the console message
Every message below was reproduced in Chrome (stable, via Playwright against local servers on `localhost` and `127.0.0.1`); wording is Chromium's and differs in other browsers.
| Message fragment | Cause | Fix |
|---|---|---|
| "No 'Access-Control-Allow-Origin' header is present" | server/proxy did not add ACAO, often on an **error** response (500/401 from middleware before CORS) | run CORS middleware first; add headers on error handlers too (ran: a bare 500 gives exactly this message) |
| "Response to preflight request doesn't pass access control check: It does not have HTTP ok status" | OPTIONS returned 401/404/405 with an ACAO header. If the failing OPTIONS response has no ACAO, Chrome reports "No 'Access-Control-Allow-Origin' header is present" instead | handle OPTIONS before auth, return 204 |
| "Request header field authorization is not allowed by Access-Control-Allow-Headers in preflight response" | missing in `Allow-Headers` | add it |
| "Method PUT is not allowed by Access-Control-Allow-Methods in preflight response" | missing in `Allow-Methods` | add it |
| "must not be the wildcard '*' when credentials mode is 'include'" | `*` with credentials | echo exact allowed origin |
| "Redirect is not allowed for a preflight request" | http->https or trailing-slash redirect | call the final URL |
| "has a value 'https://a' that is not equal to the supplied origin" | hardcoded/cached ACAO for another origin | dynamic allowlist + `Vary: Origin` |

## 2. Network panel
Find the OPTIONS request in the DevTools Network panel (the filter that shows it varies by browser version). Compare request `Origin` to response headers. Check the actual request too. Copy as cURL to replay with headers.

## 3. Not-actually-CORS problems
- Mixed content (https page -> http API) is blocked first.
- `net::ERR_BLOCKED_BY_CLIENT` = ad blocker.
- Private Network Access (public site -> `localhost`/LAN) needs extra handling in Chromium (preflight header or permission prompt depending on version); see the private-network-access-preflights skill.
- `mode: "no-cors"` makes errors disappear by returning an **opaque** response you cannot read (ran: `fetch` resolved with `status 0`) - never the fix.
- Server-to-server calls (curl, Node) never enforce CORS - "works in Postman" proves nothing.

## 4. Fix strategy
1. Prefer same-origin: dev-server proxy (`vite server.proxy`, Next.js rewrites) and production reverse proxy routing `/api` to the backend - no CORS at all.
2. Otherwise configure the server allowlist properly. Never use browser extensions that disable CORS or `Access-Control-Allow-Origin: *` with reflected credentials as the "fix".

## Verify
Replay with curl including `Origin` (and an OPTIONS for preflight) and check headers on both success and error responses.
