---
id: computing-software.qa-testing-engineering.test-automation.grpc-api-testing
name: grpc-api-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [grpc-testing, grpcurl, ghz, protobuf, grpc-status-codes]
level: practitioner
status: verified
description: "Test gRPC services: grpcurl exploration with reflection or protos, status code and metadata assertions, deadlines, streaming tests in code, and ghz load tests."
sources:
  - https://github.com/fullstorydev/grpcurl
  - https://grpc.io/docs/guides/status-codes/
  - https://ghz.sh/docs/usage
  - https://grpc.io/docs/guides/deadlines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC API testing (grpcurl, ghz)

## Explore with grpcurl
```bash
grpcurl -plaintext localhost:50051 list                         # needs server reflection
grpcurl -plaintext localhost:50051 describe orders.v1.OrderService
grpcurl -plaintext -d '{"id":"ord_1"}' localhost:50051 orders.v1.OrderService/GetOrder
grpcurl -import-path ./proto -proto orders/v1/orders.proto \
  -H "authorization: Bearer $TOKEN" -d @ api.test:443 orders.v1.OrderService/CreateOrder < order.json
```
TLS by default (a plaintext server gives `tls: first record does not look like a TLS handshake`); flags must come before the host:port; `-plaintext` for local, `-insecure` to skip verification, `-cacert/-cert/-key` for mTLS.

## Automated tests (Python example)
```python
import grpc, pytest
from orders.v1 import orders_pb2 as pb, orders_pb2_grpc as rpc

@pytest.fixture
def stub():
    with grpc.insecure_channel("localhost:50051") as ch:
        yield rpc.OrderServiceStub(ch)

def test_not_found(stub):
    with pytest.raises(grpc.RpcError) as e:
        stub.GetOrder(pb.GetOrderRequest(id="missing"), timeout=2)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND

def test_stream_lists_all(stub):
    items = list(stub.ListOrders(pb.ListOrdersRequest(page_size=10), timeout=5))
    assert all(i.id for i in items)
```
The three tests above passed against a `grpcio` 1.84 server (reflection enabled via `grpcio-reflection`, `NOT_FOUND` via `context.abort`, a slow handler for `DEADLINE_EXCEEDED`). Use an in-process server (`grpc.server` with the real servicer and fakes) for fast component tests; real network tests for integration.

## What to cover
- Status codes per error (INVALID_ARGUMENT vs FAILED_PRECONDITION vs NOT_FOUND), rich error details (`google.rpc.Status` details) if used.
- Deadlines: client timeout honoured, server cancels work on `DEADLINE_EXCEEDED`/`CANCELLED`.
- Metadata: auth headers required, response trailers.
- Streaming: server stream completion, client stream half-close, bidi ordering, backpressure.
- Backward compatibility of protos: `buf breaking --against '.git#branch=main'` in CI (buf 1.75 with `breaking: use: [FILE]`: deleting a field printed `Previously present field "2" ... was deleted` and exited 100; adding a field exited 0).

## Load with ghz
```bash
ghz --insecure --proto ./proto/orders/v1/orders.proto --call orders.v1.OrderService/GetOrder \
  -d '{"id":"ord_{{.RequestNumber}}"}' --rps 500 --duration 60s --connections 10 localhost:50051
```
Reports latency histogram and status code distribution (ghz v0.121.0: both `pkg.Service/Method` and `pkg.Service.Method` accepted by `--call`; 997 OK responses at 200 rps for 5 s). k6 `k6/net/grpc` for scripted scenarios (module name confirmed in the k6 source; not run here).

## Gotchas
- One HTTP/2 connection multiplexes streams; load tests with a single connection hit per-connection limits: set `--connections`.
- Reflection is often disabled in production; keep protos available to test tooling.

## Verify
`buf breaking` passes on compatible changes and fails on a removed field; status code tests cover each documented error.
