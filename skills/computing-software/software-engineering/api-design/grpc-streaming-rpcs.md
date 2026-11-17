---
id: computing-software.software-engineering.api-design.grpc-streaming-rpcs
name: grpc-streaming-rpcs
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-streaming, server-streaming, client-streaming, bidirectional-streaming, flow-control, keepalive, long-lived-streams]
level: advanced
status: docs-checked
description: "Decide when to use server, client or bidirectional gRPC streaming, handle flow control, keepalives, reconnection and load balancing of long-lived streams."
sources: ["https://grpc.io/docs/what-is-grpc/core-concepts/#rpc-life-cycle", "https://grpc.io/docs/guides/flow-control/", "https://grpc.io/docs/guides/keepalive/", "https://grpc.io/docs/guides/performance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC streaming RPCs

**Goal:** use streaming where it genuinely beats unary calls, and keep long-lived
streams healthy in production.

## The four shapes
```proto
rpc Get(Req) returns (Resp);                          // unary
rpc Watch(WatchReq) returns (stream Event);           // server streaming: feeds, large result sets, progress
rpc Upload(stream Chunk) returns (UploadResult);      // client streaming: uploads, telemetry batches
rpc Chat(stream Msg) returns (stream Msg);            // bidi: interactive protocols
```
The performance guide says streams suit a long-lived logical flow of data and avoid repeated RPC
initiation, but they cannot be load balanced once started, are harder to debug, and can reduce
scalability, so use them only when they give substantial performance or simplicity benefit.
Prefer unary + pagination for ordinary list APIs.

## Flow control and backpressure
Flow control stops a fast sender overwhelming a receiver; it applies to streaming RPCs, not unary.
By default gRPC handles it for you. If both sides do synchronous reads or manual flow control and
both write heavily without reading, they can deadlock. Don't buffer unboundedly in your own
queues behind a slow receiver.

## Lifetimes, deadlines, keepalive
- Keepalive pings keep HTTP/2 connections alive through idle periods. Settings: `KEEPALIVE_TIME`
  (interval between pings) and `KEEPALIVE_TIMEOUT` (ack timeout, after which the connection closes).
- Servers decide whether they accept keepalives: `PERMIT_KEEPALIVE_TIME` is the minimum time between
  pings a server allows. If the server does not support keepalive, it eventually sends a GOAWAY with
  debug data `too_many_pings`. Agree client settings with the service owner.
- Server `MAX_CONNECTION_AGE` (with `MAX_CONNECTION_AGE_GRACE`) limits how long a channel exists,
  forcing reconnection. Clients must reconnect and resume (send a cursor / last event id).
- A channel uses HTTP/2 connections with a concurrent-stream limit; beyond it new RPCs queue in the
  client. Workarounds from the guide: a separate channel per high-load area, or a channel pool.

## Errors mid-stream
A stream ends with a status. Partial results may have been delivered: design messages
so clients can resume (sequence numbers, resume tokens) instead of restarting from scratch.

## Verify
- [ ] Client reconnect test: kill a server replica; client resumes without data loss/duplication beyond the documented semantics.
- [ ] Slow-consumer test: server memory stays bounded.

## Checked

Date: 2026-11-01. Confirmed against the gRPC flow control, keepalive and performance guides.
Removed unconfirmed claims about L4 load balancers, `round_robin`, Envoy, Go option names and
`keepalive_time` naming.
Method: documentation only; no commands were run.
