---
id: computing-software.messaging-and-integration.temporal.codec-server-protocol
name: codec-server-protocol
category: computing-software
field: messaging-and-integration
product: temporal
tags: [codec-server, encode, decode, external-storage, cors, x-namespace, jwt, payload-codec]
level: advanced
status: docs-checked
description: "Run a Temporal Codec Server: /encode and /decode endpoints, external storage /download, preserveStorageRefs, authentication options, X-Namespace authorization."
sources:
  - https://docs.temporal.io/codec-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Codec Server is an HTTP(S) service you host that runs your Payload Codec for the Web UI and CLI. It is independent of the Temporal Service and keys never leave your environment. Without it the UI and CLI show raw encoded payloads. It also lets the UI or CLI encode input when you start or signal a workflow, so the Service never sees plaintext (use HTTPS beyond loopback).

Protocol: two POST endpoints, `/encode` (plaintext to encoded) and `/decode` (encoded to decoded), each taking and returning JSON with a `payloads` array.

External Storage: payloads over a threshold are replaced in history with reference tokens. Build the handler with `NewPayloadHTTPHandler` and `PayloadHTTPHandlerOptions` (storage drivers, pre-storage codecs, post-storage proxy codecs). It adds `/download` (fetch and decode a stored payload; the UI uses it when you expand a reference); `/decode` follows references unless called with `?preserveStorageRefs=true`; `/encode` encodes then uploads oversized payloads. Do not point a Worker's remote codec at this handler; use `NewPayloadCodecHTTPHandler` for that, with identical codecs.

Security: anyone who can call it effectively can decrypt. Options:
- Bind to `localhost` (the UI can reach it) or place behind a VPN.
- Authentication, recommended: enable Include cross-origin credentials so the server uses its own cookies and login.
- Or Pass access token: the UI forwards its JWT in `Authorization`; validate against the OIDC provider's JWKS endpoint (Cloud: the Temporal Cloud JWKS endpoint; the optional audience check is `https://saas-api.tmprl.cloud`).
- Namespace authorization: each request carries `X-Namespace`; you must check the user may decode that Namespace.

## Checked

2026-11-08. Read in full: the Codec Server page (docs.temporal.io/codec-server). Every remaining claim matches those pages. Removed: the literal JWKS URL, which the page does not state.

Method: documentation only; no commands were run.
