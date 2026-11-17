---
id: computing-software.ai-ml-engineering.seldon-core-2.inference-ingress-routing-options
name: inference-ingress-routing-options
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference, ingress, virtual-hosts, subdomains, authority, grpc-paths, routing-headers]
level: advanced
status: docs-checked
description: "Choose how an ingress routes to Seldon Core 2: virtual hosts, subdomains, custom headers or paths, and why custom path prefixes do not work with gRPC."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ingress routing for inference

With an ingress controller you must set routing rules yourself. Custom path prefixes do not work with gRPC, because gRPC determines the path from the Protobuf definition and not every implementation lets you change it. To expose REST and gRPC consistently use virtual hosts, subdomains or headers. Using only paths means you cannot tell apart different Seldon installs, or Seldon traffic from other inference endpoints on the same ingress. A mixture is allowed.

## Virtual hosts
The `Host` header (HTTP/1) or `:authority` pseudo-header (HTTP/2) names the logical service.
- `seldon` CLI: the `--authority` flag, for REST and gRPC.
- `curl`: set `Host` as a normal header.
- `grpcurl`: the `-authority` flag.
- Go `http.Request`: use the `Host` field, because header values for Host are ignored.
- Python `requests`: pass host as a normal header.

## Subdomains
Put the subdomain in the URI, for example namespaces `seldon-1` and `seldon-2` become `https://seldon-1.example.com/v2/models/iris/infer`. With the CLI use `--inference-host`. Istio and Nginx support this.

## Headers
Use any header that does not clash with those Seldon relies on. `seldon` accepts repeated `--header`, `curl` uses `-H`, `grpcurl` uses `-H`.

## Paths
Match well-known v2 prefixes. For gRPC the method is `/inference.GRPCInferenceService/ModelInfer`, so an exact match or a regex that matches the word inference works.

## Checked

Confirmed against the Inference page (Ingress Routes section): gRPC path limitation, virtual hosts via Host and :authority with the per-tool handling, subdomain example and --inference-host, header routing flags, and the gRPC method path.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb inference.md page (raw markdown).
