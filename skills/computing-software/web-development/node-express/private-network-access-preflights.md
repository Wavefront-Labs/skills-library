---
id: computing-software.web-development.node-express.private-network-access-preflights
name: private-network-access-preflights
category: computing-software
field: web-development
product: node-express
tags: [private-network-access, local-network-access, cors-preflight, localhost-security, intranet-devices]
level: advanced
status: docs-checked
description: "Requests from public websites to localhost and private-IP devices: Chrome's Private/Local Network Access rules, required preflight headers or permission, and safe device APIs."
sources:
  - https://developer.chrome.com/blog/private-network-access-preflight
  - https://wicg.github.io/private-network-access/
  - https://developer.chrome.com/blog/local-network-access
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private Network Access preflights

Public websites calling `http://192.168.1.1`, `http://localhost:8080` or `*.local` devices enabled drive-by attacks on routers, printers and local dev servers. Chromium restricts these requests.

## 1. What changed
- **Private Network Access (PNA)**: a request from a less-private context (public internet) to a more-private one (private IP, loopback) gets a CORS preflight carrying `Access-Control-Request-Private-Network: true`. The target must answer:
```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Private-Network: true
```
- The preflight is sent for every private network request regardless of method or request mode (cors, no-cors and others), and also for same-origin requests whose target is more private than the initiator, which guards against DNS rebinding. For a request in `cors` mode, CORS headers must also be on the final response.
- PNA was put on hold, and Chrome's **Local Network Access** (LNA) replaces it: a user permission prompt when a public site contacts local network or loopback addresses, restricted to secure contexts. The prompt launched in Chrome 142 (update dated 29 Sept 2025); it applies to `fetch()`, subresource loading and subframe navigation. Check current Chrome status for your version.
- LNA gaps listed at the time of the post: WebSockets, WebTransport and WebRTC were not yet gated, and service or shared workers need the permission granted earlier by a document of the same origin.
- Secure-context requirement: only secure contexts may make private network requests (enforced from Chrome 96) and request the LNA permission.
- Mixed content: under LNA, permission-gated local network requests are exempt from mixed content checks when Chrome knows beforehand they go to the local network: a private IP literal host, a `.local` hostname, or `fetch()` with `targetAddressSpace: "local"`. A public hostname that merely resolves to a local address is not exempt.

## 2. If you ship a local agent or device web UI
- Under the PNA preflight model, answer the preflight with `Access-Control-Allow-Private-Network: true` plus a CORS `Access-Control-Allow-Origin` naming only your known web origins.
- Never rely on "it's only reachable on the LAN"; these rules exist because public pages can be used for CSRF against routers and other private-network devices.

## Verify
- [ ] From a public HTTPS test page, DevTools shows the PNA preflight or LNA permission prompt and the device's response headers.

## Checked

The preflight headers, request scope, secure-context rule, DNS rebinding rationale, LNA prompt, Chrome 142 launch, known gaps and mixed content exemptions were confirmed on the two Chrome blog posts. Removed as unconfirmed: the iframe `allow` delegation claim, the Vite allowedHosts claim, Host header validation, pairing secrets, and the WebRTC relay advice. The WICG spec page was only searched for header names, not read in full.

Method: docs-checked 2026-11-09 against developer.chrome.com private-network-access-preflight (introduction and what-is-PNA sections) and local-network-access (read from the intro through Chrome 139 plans), plus a header-name search of wicg.github.io/private-network-access.
