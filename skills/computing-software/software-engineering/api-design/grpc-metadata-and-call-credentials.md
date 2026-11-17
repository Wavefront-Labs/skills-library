---
id: computing-software.software-engineering.api-design.grpc-metadata-and-call-credentials
name: grpc-metadata-and-call-credentials
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-metadata, call-credentials, authorization-header, trailers, channel-credentials, mtls]
level: practitioner
status: docs-checked
description: "Use gRPC metadata and credentials correctly: header and trailer rules, binary -bin keys, per-call tokens versus TLS channel credentials, and reading metadata in servers."
sources: ["https://grpc.io/docs/guides/metadata/", "https://grpc.io/docs/guides/auth/", "https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md", "https://github.com/grpc/grpc-go/blob/master/Documentation/grpc-metadata.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC metadata and call credentials

Metadata is a list of key-value pairs sent as HTTP/2 headers (client to server, and server initial headers) and trailers (server, when it closes the call).

## Rules
- Keys are case insensitive and, on the wire, use only lowercase letters, digits, `_`, `-` and `.`; keys ending in `-bin` carry binary values (base64 on the wire, applied by the library); other values are space and printable ASCII.
- Do not use keys starting with `grpc-` (reserved for gRPC). Servers may limit request header size; 8 KiB is the suggested default, and clients may limit response headers and trailers the same way. Keep metadata small.
- Metadata is for cross-cutting data (auth token, tracing information, request id, tenant); business data belongs in the message.
- Header order is not preserved except among values with the same name; duplicate names may be joined with `,`.

## Go example
```go
// client: attach per call
ctx := metadata.AppendToOutgoingContext(ctx, "x-request-id", id)
// server: read
md, _ := metadata.FromIncomingContext(ctx)
vals := md.Get("x-request-id")
// server (unary): send headers and trailers
grpc.SetHeader(ctx, metadata.Pairs("x-served-by", "node-3"))
grpc.SetTrailer(ctx, metadata.Pairs("x-cost-units", "12"))
```
Go lowercases keys in `metadata.New` and `metadata.Pairs`. On the client, read a unary call's headers and trailers with the `grpc.Header(&md)` and `grpc.Trailer(&md)` call options. Never use `FromOutgoingContext` on a server to write response metadata; it is client-side only.

## Credentials layers
- Channel credentials: attached to the channel, such as SSL/TLS (server authentication and encryption; client certificates are an option for mutual authentication).
- Call credentials: attached to a call; an OAuth token is always per-call credentials and normally goes in the `authorization` HTTP header (`Bearer <token>`).
- Composite credentials combine a channel credential with call credentials, so every call on the channel sends the token. Most implementations validate tokens in a server interceptor (see grpc-interceptors).
- Most gRPC language implementations will not let you send credentials over an unencrypted channel.
- Google-issued tokens are for Google services only; sending one to another service risks theft and impersonation.

## Gotchas
- A Trailers-Only response (used for calls that produce an immediate error) carries the status in a single header block, so client code that looks for trailers must handle both shapes.
- Some deployments send non-200 HTTP statuses or omit `grpc-status`; clients must synthesize a status.
- Test custom metadata and trailers through every proxy and gateway you deploy.

Verify: call a method with a bad token and with a valid one through the real path, and confirm the first fails with an authentication error and the second succeeds with your response headers and trailers visible.

## Checked
2026-11-08. Confirmed against grpc.io Metadata and Authentication guides, PROTOCOL-HTTP2.md (header grammar, `-bin`, 8 KiB, Trailers-Only, `grpc-` prefix) and the grpc-go metadata doc (AppendToOutgoingContext, SetHeader, SetTrailer, Header/Trailer call options, lowercasing). Removed: the `credentials.NewTLS` call, the grpc-web trailer-dropping claim, `SendHeader`, and the `grpcurl` verify line (none in the sources).
Method: documentation only; no commands were run.
