---
id: computing-software.cybersecurity-defensive.application-security.grpc-security
name: grpc-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [grpc-security, grpc, protobuf, tls, call-credentials, protovalidate, api-security]
level: practitioner
status: docs-checked
description: "Secure gRPC services: TLS and ALTS channel credentials, per-call OAuth token credentials checked in a server interceptor, protovalidate message rules."
sources: ["https://grpc.io/docs/guides/auth/", "https://raw.githubusercontent.com/bufbuild/protovalidate/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC security

## Transport
- gRPC has SSL/TLS integration and promotes its use to authenticate the server and encrypt all
  data exchanged. Optional mechanisms let clients provide certificates for mutual
  authentication.
- ALTS is supported as a transport security mechanism when the application runs on Compute
  Engine or Google Kubernetes Engine.
- The language examples each include an insecure base case (for example
  `grpc.credentials.createInsecure()` in Node.js, `:this_channel_is_insecure` in Ruby). These
  carry no encryption or authentication; treat them as test-only.
- Non-POSIX systems such as Windows must give root certificates in `SslCredentialsOptions`,
  because defaults are configured only for POSIX filesystems.

## Credentials
- Channel credentials attach to a channel (for example SSL credentials). Call credentials
  attach to a call. A composite of the two sends the call credentials with every call on the
  channel.
- Token-based auth is generally used as well as SSL/TLS on the channel, and most gRPC language
  implementations will not let you send credentials on an unencrypted channel.
- OAuth token flow: the client gets a token, creates per-call credentials from it, and the
  token is normally sent in the HTTP Authorization header. The server verifies the token; in
  most implementations the validation is done in a server-side interceptor.
- Google credentials should only be used to connect to Google services. Sending a
  Google-issued OAuth2 token to a non-Google service could let the token be stolen and used to
  impersonate the client.
- Custom schemes plug in through the credentials plugin API (`MetadataCredentialsPlugin`).

## Input validation
- Protovalidate is a semantic validation library for Protobuf, the next generation of
  protoc-gen-validate. Annotate fields with standard rules and write custom rules in CEL.
  README examples: `string id = 1 [(buf.validate.field).string.uuid = true];`,
  `uint32 age = 2 [(buf.validate.field).uint32.lte = 150];`,
  `string email = 3 [(buf.validate.field).string.email = true];`,
  `string first_name = 4 [(buf.validate.field).string.max_len = 64];`.
- Implementations exist for Go, Java, Python, C++ and TypeScript/JavaScript.

## Verify
- [ ] Production channels use TLS or ALTS credentials, not an insecure channel.
- [ ] Token validation runs in a server interceptor rather than inside each handler.
- [ ] Messages carry protovalidate rules on externally supplied fields.

## Checked
Confirmed 2026-11-09 against the gRPC Authentication guide (read in full) and the protovalidate README.
Removed as unconfirmed: the Go mTLS server snippet, the method-to-scope permission map, stream re-check advice, message size, concurrent stream and keepalive limits, unknown-field handling, server reflection, gateway and channelz exposure, status code guidance, the grpcurl checks, and the grpc.io security-policy source, which returned 404.
Method: docs-checked 2026-11-09 against grpc.io guides auth and bufbuild/protovalidate README
