---
id: computing-software.web-development.trpc.websocket-rpc-protocol
name: websocket-rpc-protocol
category: computing-software
field: web-development
product: trpc
tags: [trpc, websockets, json-rpc, protocol, subscription-stop]
level: sme
status: docs-checked
description: "The tRPC WebSocket message formats: query and mutation requests, subscription start and subscription.stop, result types, connectionParams message and reconnect."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/websockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The WebSocket transport uses JSON-RPC-style envelopes (see the envelope and codes files in the server package).

Query or mutation request: `{ id, jsonrpc?: '2.0', method: 'query' | 'mutation', params: { path, input? } }`, with the input serialized by the transformer. The response is `{ id, jsonrpc?, result: { type: 'data', data } }` or an error.

Subscription start: `{ id, method: 'subscription', params: { path, input? } }`. Cancel with `{ id, method: 'subscription.stop' }` where `id` is the id of the created subscription. Subscription responses are `result.type` of `data` (emitted data), `started` or `stopped`.

Connection params: if the connection is initialized with `?connectionParams=1`, the first message must be `{ method: 'connectionParams', data: Record<string, string> | null }`.

Errors follow the JSON-RPC error object (see the error formatting page).

Server to client notification: `{ id: null, type: 'reconnect' }` tells clients to reconnect before the server shuts down, triggered by `handler.broadcastReconnectNotification()`.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/websockets.md (read in full): "WebSockets RPC Specification" (query/mutation request and response, subscription start, subscription.stop, response shapes, connection params message), "Errors" and "Notifications from Server to Client". The linked envelopes.ts and codes.ts files were not opened.

Removed or corrected: the closing paragraph about non-TypeScript clients, load testing and a required `subscription.stop` (not on the page), and the invented Verify step.

Method: documentation only; no commands were run.
