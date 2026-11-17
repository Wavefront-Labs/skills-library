---
id: computing-software.qa-testing-engineering.playwright.websocket-inspection-and-mocking
name: websocket-inspection-and-mocking
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [websocket-mocking, routewebsocket, playwright-network, websockets, real-time-testing]
level: practitioner
status: docs-checked
description: "Inspect and mock WebSockets in Playwright: page.on('websocket') frame events, routeWebSocket to fake or modify a server, and asserting real-time UI updates."
sources:
  - https://playwright.dev/docs/network#websockets
  - https://playwright.dev/docs/api/class-websocketroute
  - https://playwright.dev/docs/api/class-websocket
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting and mocking WebSockets (Playwright)

**Goal:** test real-time features (chat, live prices, notifications) deterministically.

## Observe traffic
Every time a WebSocket is created, `page.on('websocket')` fires with a `WebSocket` instance.
```ts
page.on('websocket', ws => {
  console.log('WS open', ws.url());
  ws.on('framesent', e => console.log('>>', e.payload));
  ws.on('framereceived', e => console.log('<<', e.payload));
  ws.on('close', () => console.log('WS closed'));
});
```
`WebSocket` events: `close`, `framereceived`, `framesent`, `socketerror`; frame payload is `string | Buffer`.
`ws.waitForEvent('framereceived', { predicate: e => String(e.payload).includes('"type":"price"') })`
resolves when the predicate is truthy and throws if the socket closes first. Its default timeout is 0 (none).
The WebSocket page itself says to use `WebSocketRoute` to intercept or modify frames.

## Mock the server entirely (routeWebSocket, added in Playwright 1.48)
```ts
await page.routeWebSocket('wss://example.test/prices', ws => {
  ws.onMessage(message => {
    if (message === 'subscribe:BEANS') ws.send(JSON.stringify({ sku: 'BEANS', price: 12.5 }));
  });
});
await page.goto('/prices');
await expect(page.getByTestId('price-BEANS')).toHaveText('£12.50');
```
By default a routed WebSocket does not connect to the server. If the handler never calls `connectToServer()`,
Playwright assumes the socket is mocked and opens it inside the page automatically. `browserContext.routeWebSocket()`
exists too.

## Proxy and modify
```ts
await page.routeWebSocket('/ws', ws => {
  const server = ws.connectToServer();
  ws.onMessage(m => server.send(m));                                 // page -> server
  server.onMessage(m => ws.send(String(m).replace('"stock":5', '"stock":0')));   // server -> page, altered
});
```
After `connectToServer()` every message is forwarded both ways by default. Calling `onMessage()` on the page-side
route stops page-to-server forwarding (the handler must forward); calling it on the server-side route stops
server-to-page forwarding. Calling `onMessage()` again replaces the handler.

Closing: `ws.close({ code, reason })` closes one side (both options are optional). By default closing one side
closes the other; setting `onClose(handler)` disables that default forwarding. `ws.protocols()` returns the
subprotocols the page requested (added in v1.60), and `ws.url()` the socket URL.

## Test ideas
- Message ordering and duplicates.
- Reconnect after a drop; state resync after reconnect.
- Malformed frames do not crash the UI.

## Verify
UI assertions pass against the mocked socket with no backend, and a drop-and-reconnect scenario is covered.

## Checked
Date 2026-11-09. Read in full as fetched text: the WebSockets section of the Network guide, the WebSocketRoute
class page and the WebSocket class page. Confirmed: `page.on('websocket')` and the frame events, `routeWebSocket`
(added v1.48), default no-connect mocking, `connectToServer` and forwarding rules, `onMessage`, `onClose`, `close`
options, `waitForEvent` predicate and default timeout.
Removed as unconfirmed: `page.waitForEvent('websocket')`, regex URL matching for `routeWebSocket`, the specific 1006
close code, the "register the route before the page opens the socket" note and the Socket.IO framing note.
Method: documentation only; no commands were run.
