---
id: computing-software.networking-hardware-and-wireless.envoy.grpc-web-and-json-transcoder-filters
name: grpc-web-and-json-transcoder-filters
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, grpc-web, grpc-json-transcoder, protoc, descriptor-set, rest-to-grpc, http-annotations]
level: practitioner
status: docs-checked
description: "Bridge gRPC-Web browsers and REST JSON clients to a gRPC backend with Envoy filters, including generating the proto descriptor set."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/grpc_web_filter.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/grpc_json_transcoder_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# grpc web and json transcoder filters
The `grpc_web` filter bridges a gRPC-Web client to a compliant gRPC server (per the gRPC-Web protocol spec). The `grpc_json_transcoder` filter lets a RESTful JSON client call a gRPC service; the HTTP mapping must be declared in the service via `google.api.http` annotations. Streaming requests/responses are arrays of messages in JSON.

Generate the descriptor set with googleapis on the include path (annotations.proto is needed):
```
git clone https://github.com/googleapis/googleapis
protoc -I$GOOGLEAPIS_DIR -I. --include_imports --include_source_info \
  --descriptor_set_out=proto.pb test/proto/bookstore.proto
```
Then configure the filter before the router:
```yaml
- name: envoy.filters.http.grpc_json_transcoder
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_json_transcoder.v3.GrpcJsonTranscoder
    proto_descriptor: protos/helloworld.pb
    services: [helloworld.Greeter]
    print_options: { add_whitespace: true, always_print_primitive_fields: true }
```
The router sees the gRPC path (for example `/helloworld.Greeter/SayHello`), so route prefixes must match that path, not the REST path. The docs' sample cluster uses `http2_protocol_options`.

Gotchas: forgetting `--include_imports` or `--include_source_info` yields a descriptor missing the HTTP rules and the filter fails at load; the upstream cluster needs `http2_protocol_options`. Verify with a REST request to the path in your annotations (the docs sample listens on port 51051 and proxies to a gRPC server on localhost:50051).

## Checked

2026-11-03. Confirmed against: grpc_web and grpc_json_transcoder filter pages and transcoder proto (proto_descriptor, services, print_options). Removed or corrected: the 60s route timeout, the guessed curl URL and the stats filter.

Method: documentation only; no commands were run.
