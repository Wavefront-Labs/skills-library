---
id: computing-software.software-engineering.api-design.grpc-http-json-transcoding
name: grpc-http-json-transcoding
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-gateway, http-transcoding, google-api-http, rest-mapping, openapi-generation, envoy-transcoder, connect-rpc]
level: practitioner
status: docs-checked
description: "Expose gRPC services as REST/JSON with google.api.http annotations via grpc-gateway, Cloud Endpoints or Connect: paths, bodies, OpenAPI output."
sources: ["https://google.aip.dev/127", "https://github.com/grpc-ecosystem/grpc-gateway", "https://cloud.google.com/endpoints/docs/grpc/transcoding", "https://connectrpc.com/docs/introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP/JSON transcoding for gRPC

**Goal:** one API definition serving gRPC clients and browser/curl/third-party REST
clients, without hand-writing a second API layer.

## Annotate the proto (AIP-127)
```proto
import "google/api/annotations.proto";

service InvoiceService {
  rpc GetInvoice(GetInvoiceRequest) returns (Invoice) {
    option (google.api.http) = { get: "/v1/{name=invoices/*}" };
  }
  rpc CreateInvoice(CreateInvoiceRequest) returns (Invoice) {
    option (google.api.http) = { post: "/v1/invoices" body: "invoice" };
  }
  rpc UpdateInvoice(UpdateInvoiceRequest) returns (Invoice) {
    option (google.api.http) = { patch: "/v1/{invoice.name=invoices/*}" body: "invoice" };
  }
}
```
Mapping rules (AIP-127): the first key is the HTTP method (`get`, `post`, `patch`, `delete`; avoid `put` and `custom`).
Path variables use `{field=pattern}` and populate request fields; when extracting a resource name the
variable must cover the whole name, not just the ID. `*` matches one segment (no `/`), `**` may end a
path. `body: "*"` makes the whole request the JSON body; `body: "invoice"` names one top-level field
(never nested, repeated, or the same as a URI parameter); no `body` on `get` or `delete`. Fields bound to neither
path nor body become query parameters, with camelCase names. `additional_bindings` add more URIs (one level
only; the `body` must be identical in each). Avoid `json_name` unless needed for backwards compatibility.

## Implementation options
| Option | How |
|---|---|
| grpc-gateway (Go) | `protoc-gen-grpc-gateway` generates a reverse-proxy server from the `google.api.http` annotations; entrypoint uses `runtime.NewServeMux()`. `protoc-gen-openapiv2` emits OpenAPI (Swagger 2.0); `protoc-gen-openapiv3` is a separate, alpha generator for OpenAPI 3.1. |
| Google Cloud Endpoints | The Extensible Service Proxy (ESP) transcodes HTTP/JSON to gRPC using proto annotations (recommended) or YAML service configuration. |
| Connect (connectrpc) | Different approach: the same handlers serve gRPC, gRPC-Web and Connect's own HTTP protocol (works over HTTP/1.1, HTTP/2, HTTP/3; JSON or binary Protobuf) with no annotations. |

Other proxies and frameworks offer transcoding too; check their own documentation.

## Gotchas
- Bi-directional streaming cannot be natively supported over HTTP/1.1: AIP-127 says bidi RPCs should carry no `google.api.http` annotation and the service should offer a non-streaming alternative. grpc-gateway maps streaming APIs to newline-delimited JSON streams and does not support true bi-directional streaming.
- Request bodies use protobuf's canonical JSON encoding; consult it for int64, timestamp, enum and bytes representation.
- Keep annotations in sync with AIP resource names so REST URLs look natural.

## Verify
- [ ] `curl` against each annotated route returns the same data as the gRPC call.
- [ ] Generated OpenAPI published and lint-clean.

## Checked
2026-11-08. Confirmed by reading AIP-127 and the Connect introduction in full, and by targeted search of the grpc-gateway README and the Cloud Endpoints transcoding page: annotation rules, bindings, plugin names, `runtime.NewServeMux`, OpenAPI generators, ESP, streaming limits and Connect protocols. Removed (not in the sources): the Envoy `grpc_json_transcoder` and ASP.NET Core `AddJsonTranscoding` rows, API Gateway/ESPv2 naming, the lowerCamelCase/int64/error-code mapping details, "path templates must not overlap" and the "POST per method" description of Connect.
Method: documentation only; no commands were run.
