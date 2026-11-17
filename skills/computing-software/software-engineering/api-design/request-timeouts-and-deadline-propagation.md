---
id: computing-software.software-engineering.api-design.request-timeouts-and-deadline-propagation
name: request-timeouts-and-deadline-propagation
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, request-timeouts, http-timeout-budget, deadline-propagation, grpc-deadlines, retries]
level: advanced
status: docs-checked
description: "Set explicit deadlines on every call, propagate the remaining time downstream, and stop work once the caller has given up, following the gRPC deadlines guide."
sources: ["https://grpc.io/docs/guides/deadlines/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request timeouts and deadline propagation

## Always set a deadline
- A deadline is the point in time past which a client will not wait; a timeout is a maximum duration. A timeout
  becomes a deadline by adding it to the current time when the call starts.
- By default gRPC sets no deadline, so a client can wait effectively forever. Always set a realistic one:
  start from an educated guess (network latency, server processing time) and validate with load testing.
- When the deadline passes the client fails the RPC with `DEADLINE_EXCEEDED`.

## Server side
- A gRPC server automatically cancels a call (status `CANCELLED`) once the client's deadline has passed, which
  protects it from requests with unrealistically short deadlines.
- The server application must stop any activity it spawned for the RPC; for long-running work, periodically
  check whether the RPC was cancelled and stop.

## Propagate the deadline
- When your server calls another server, honour the original client's deadline. Some gRPC implementations
  propagate it automatically (on by default in Java and Go, needs enabling in C++), which avoids hand-copying
  deadlines onto each outgoing call.
- Because clocks differ between servers, gRPC converts the deadline to a timeout with elapsed time already
  deducted, so clock skew does not matter. In the guide's example a 2 s budget with 0.5 s used leaves a
  1.5 s timeout for the next hop.

## Checked
Date: 2026-11-01. Confirmed on the gRPC Deadlines guide (all points above). Removed: HTTP header conventions,
connect and read timeout values, language library defaults, cancellation APIs of other stacks, retry,
status-code and fault-injection advice, which that page does not state.
Method: documentation only; no commands were run.
