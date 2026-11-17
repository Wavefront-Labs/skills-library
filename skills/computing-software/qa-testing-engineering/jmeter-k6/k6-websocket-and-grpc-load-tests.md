---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-websocket-and-grpc-load-tests
name: k6-websocket-and-grpc-load-tests
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, k6-grpc, k6-websockets, k6-browser, grpc-load-testing, websocket-load-testing, protocols]
level: practitioner
status: verified
description: "Load test WebSocket and gRPC services with k6: k6/experimental/websockets or k6/ws, k6/net/grpc client with proto files or reflection, checks and metrics."
sources:
  - https://grafana.com/docs/k6/latest/javascript-api/k6-net-grpc/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-websockets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 WebSocket and gRPC load tests

**Goal:** load beyond plain HTTP with the same k6 workflow (checks, thresholds, scenarios).

## gRPC
```js
import grpc from 'k6/net/grpc'
import { check } from 'k6'
const client = new grpc.Client()
client.load(['./protos'], 'orders.proto')          // init context only

export default () => {
  client.connect('orders.internal:443', {})         // or { plaintext: true }; reflect: true to skip load()
  const res = client.invoke('shop.Orders/Get', { id: '42' }, { metadata: { authorization: `Bearer ${__ENV.TOKEN}` } })
  check(res, { 'status OK': r => r && r.status === grpc.StatusOK })
  client.close()
}
export const options = { thresholds: { grpc_req_duration: ['p(95)<200'] } }
```
Streaming: `new grpc.Stream(client, 'shop.Orders/Watch')` with `on('data')`, `on('end')`, `on('error')`, `write()`, `end()`. Do not call `client.close()` right after `stream.end()`: in a run the stream was cancelled (`canceled by client (k6)` warning) and no `data` event fired; closing the client inside the `on('end')` handler delivered `STREAM data {"id":"a-w"...}` then `end`.
Run against a local Python grpcio server (k6 2.3.0): `client.load(['./protos'], 'orders.proto')`, `connect(addr, { plaintext: true })`, `invoke('shop.Orders/Get', ...)` with `metadata.authorization` (the server saw `Bearer abc`), `r.status === grpc.StatusOK` (check passed), `grpc_req_duration` threshold evaluated (`p(95)=1.28ms`), and `connect(addr, { plaintext: true, reflect: true })` worked with no `load()` against a server with reflection enabled. `client.load()` inside VU code throws `load must be called in the init context`.

## WebSockets
```js
import { WebSocket } from 'k6/websockets'      // k6/experimental/websockets still works on k6 2.3.0 but logs a deprecation warning
export default () => {
  const ws = new WebSocket('wss://chat.example.com/ws')
  ws.onopen = () => ws.send(JSON.stringify({ type: 'join', room: 'r1' }))
  ws.onmessage = (e) => { if (JSON.parse(e.data).type === 'joined') ws.close() }
  ws.onerror = (e) => console.error(e.error)
}
```
Legacy `k6/ws` (`ws.connect(url, params, socket => {...})`) blocks the VU for the socket's life.
Metrics (all printed in a run against a local Python `websockets` echo server, for both `k6/websockets` and legacy `k6/ws`): `ws_connecting`, `ws_session_duration`, `ws_sessions`, `ws_msgs_sent`, `ws_msgs_received`; add custom Trends for message round-trip latency. Legacy `ws.connect` returned `status 101` (check passed).

## Load model notes
- Long-lived connections: model concurrent connections (constant-vus) more than request rate.
- Measure message latency end to end with timestamps in payloads.

## Gotchas
- Reconnecting the gRPC client every iteration measures connection setup; connect once per VU (`if (__ITER == 0)`) when that is the real behaviour.
- TLS and ALPN issues with gRPC behind load balancers: test against the same endpoint clients use.

## Verify
Thresholds on grpc_req_duration / custom WS latency trend evaluated; server-side connection counts match VUs.
