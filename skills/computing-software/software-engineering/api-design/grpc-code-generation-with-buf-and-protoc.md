---
id: computing-software.software-engineering.api-design.grpc-code-generation-with-buf-and-protoc
name: grpc-code-generation-with-buf-and-protoc
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, buf-generate, protoc, protobuf, code-generation, buf-lint]
level: practitioner
status: gated
description: "Generate gRPC stubs reproducibly with buf generate (or protoc with pinned plugins): buf.yaml, buf.gen.yaml, remote plugins, managed mode, lint and CI checks."
sources: ["https://buf.build/docs/generate/overview/", "https://buf.build/docs/configuration/v2/buf-gen-yaml/", "https://protobuf.dev/reference/go/go-generated/", "https://grpc.io/docs/protoc-installation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code generation with buf generate / protoc

Run here: buf 1.74.0 on Windows with the `buf.yaml` and `buf.gen.yaml` below (without the `deps` line, then with it): `buf dep update` wrote `buf.lock` for `buf.build/googleapis/googleapis` (it warns when a declared dep is unused), and `buf generate` fetched the three remote plugins (go v1.34.2, grpc/go v1.5.1, stephenh-ts-proto) with no login and produced `billing.pb.go`, `billing_grpc.pb.go` and `gen/ts/...`; managed mode with `go_package_prefix` gave `package billingv1` from `acme.billing.v1`. The protoc command was run in its Python form (`python -m grpc_tools.protoc ... --python_out --grpc_python_out --pyi_out`, producing `_pb2.py`, `_pb2.pyi`, `_pb2_grpc.py`); the Go protoc plugins, Gradle, `Grpc.Tools` and the CI drift check were not run (gated: unconfirmed, source is paywalled or blocked).

## buf (recommended)
`buf.yaml` (module + lint/breaking rules):
```yaml
version: v2
modules: [{path: proto}]
lint: {use: [STANDARD]}
breaking: {use: [FILE]}
deps: [buf.build/googleapis/googleapis]
```
`buf.gen.yaml`:
```yaml
version: v2
managed:
  enabled: true
  override:
    - {file_option: go_package_prefix, value: github.com/acme/api/gen/go}
plugins:
  - remote: buf.build/protocolbuffers/go:v1.34.2
    out: gen/go
    opt: paths=source_relative
  - remote: buf.build/grpc/go:v1.5.1
    out: gen/go
    opt: paths=source_relative
  - remote: buf.build/community/stephenh-ts-proto
    out: gen/ts
```
```
buf dep update && buf lint && buf breaking --against '.git#branch=main' && buf generate
```
Managed mode sets language options (`go_package`, `java_package`) so .proto files stay clean.
Pin plugin versions; unpinned remote plugins change output silently.

## protoc (when you must)
```
protoc -I proto -I third_party \
  --go_out=gen/go --go_opt=paths=source_relative \
  --go-grpc_out=gen/go --go-grpc_opt=paths=source_relative \
  proto/orders/v1/orders.proto
```
Pin `protoc` and each `protoc-gen-*` version (tools.go, a Makefile download, or a container image).
Python: `python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. --pyi_out=. ...`.
Java/Kotlin: protobuf Gradle plugin; .NET: `Grpc.Tools` with `<Protobuf Include=... />` in the csproj.

## Commit or generate?
- Inside one repo: generate in the build, or commit and have CI fail if `buf generate && git diff
  --exit-code` shows drift.
- For consumers in other repos: publish generated packages (BSR generated SDKs, npm/PyPI/Maven
  artifacts) versioned with the schema.

## Gotchas
Mismatched protobuf runtime vs generated code versions fail at import time; upgrade together.
