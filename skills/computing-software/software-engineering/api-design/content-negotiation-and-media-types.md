---
id: computing-software.software-engineering.api-design.content-negotiation-and-media-types
name: content-negotiation-and-media-types
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, content-negotiation, media-types, accept-header, http-406, vary-header]
level: practitioner
status: docs-checked
description: "Serve one resource in several representations with Accept / Content-Type, 406 and 415 handling, structured +json suffixes and correct Vary headers so caches keep variants apart."
sources: ["https://www.rfc-editor.org/rfc/rfc9110#section-12", "https://www.rfc-editor.org/rfc/rfc6838", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content negotiation and media types

**Goal:** a client says what it can read (`Accept`) and what it is sending (`Content-Type`); the
server picks a representation or fails loudly, and caches store each variant separately.

## Request side
- Send `Content-Type` on any request with a body. A server may refuse an unsupported request representation
  with **415 (Unsupported Media Type)** (RFC 9110, section 15.5.16 reference in section 12 text).
- `Accept-Patch` (RFC 5789, referenced by RFC 9110 section 12) is the response header that tells clients which
  content types a resource accepts in PATCH requests; use it to make 415 actionable.
- Document the one body type per endpoint instead of sniffing bodies.

## Response side
- Proactive negotiation: the client sends `Accept` (and `Accept-Language`, `Accept-Encoding`) with quality
  values, `weight = OWS ";" OWS "q=" qvalue`; the server chooses. Both RFC 9110 and MDN describe this.
- If none of the available representations is acceptable, the server may either send **406 (Not Acceptable)**
  or disregard the header and send a default representation. Pick one policy and document it. Clients cannot
  rely on preferences being honoured, so they must handle a different type.
- A client can send `Accept: */*;q=0` to explicitly ask for 406 when its preferred format is unavailable.
- `Vary` in a response lists the request fields that might have influenced the choice of representation, so
  caches key on them: send `Vary: Accept` when the body depends on `Accept` (and `Accept-Encoding`,
  `Accept-Language` likewise).

## Media type naming
- RFC 6838 defines media type registration and the structured syntax suffix (`+json` is one of the suffixes it
  discusses), so a vendor type such as `application/vnd.example.invoice.v2+json` signals JSON syntax.
- Vendor types allow per-resource versioning but are harder for tooling; weigh that against versioning in the
  path.

## Checked
Date: 2026-11-01. Confirmed in RFC 9110 section 12 (Accept q-value syntax, 406 or ignore, 415, Accept-Patch, Vary
definition, `*/*;q=0`), RFC 6838 (structured syntax suffix, `+json` named) and MDN Content negotiation (406, 415, q-factors).
Removed: framework helper names, problem+json, merge-patch, ndjson and SSE rows, Content-Disposition, format-in-URL
advice, JSON charset note and curl examples, which the cited pages do not state.
Method: documentation only; no commands were run.
