---
id: computing-software.software-engineering.api-design.http-method-safety-and-idempotency
name: http-method-safety-and-idempotency
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, http-method-semantics, http-methods, safe-methods, idempotent-methods, rfc-9110, put-vs-post, head-options]
level: intro
status: docs-checked
description: "Choose HTTP methods by their RFC 9110 semantics: which are safe, which idempotent, when to use PUT, PATCH or POST, and what retries and caches assume."
sources: ["https://www.rfc-editor.org/rfc/rfc9110#section-9", "https://www.rfc-editor.org/rfc/rfc5789"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP method semantics (RFC 9110 section 9)

| Method | Safe | Idempotent | Cache semantics defined | Typical use |
|---|---|---|---|---|
| GET | yes | yes | yes | read a resource |
| HEAD | yes | yes | yes | headers only |
| OPTIONS | yes | yes | no | describe communication options |
| TRACE | yes | yes | no | loop-back test |
| PUT | no | yes | not cacheable | create or replace at a known URL |
| DELETE | no | yes | not cacheable | remove |
| POST | no | no | only with explicit freshness and a matching `Content-Location` | create, or resource-specific processing |
| PATCH | no | no (can be designed to be) | only with explicit freshness and a matching `Content-Location` | partial update (RFC 5789) |

- Safe means essentially read-only: the client does not request or expect any state change. Reasonable use must not cause harm or unusual burden. The point is that spiders and pre-fetchers can call safe methods without fear. If a resource uses query parameters to select an action (the spec's example is `page?do=delete`), the owner MUST disable that action when it is reached with a safe method.
- Idempotent means the intended effect of N identical requests is the same as one. It applies to what the client asked for; the server may still log each request or keep history. The response may differ between repeats.
- Idempotent methods may be retried automatically after a communication failure. A client SHOULD NOT automatically retry a non-idempotent request unless it knows the semantics are idempotent or can detect the original was never applied. A proxy MUST NOT automatically retry non-idempotent requests, and a client SHOULD NOT retry a failed automatic retry.
- PUT creates or replaces the target resource's state with the enclosed representation: 201 if it created one, 200 or 204 if it modified one. The client must know the target URI; a service that chooses the URI itself SHOULD use POST.
- PATCH (RFC 5789) is neither safe nor idempotent, but a request can be issued so that it is idempotent (for example by making it conditional), which also guards against collisions. A server that does not support the patch format should say so and advertise formats in `Accept-Patch`.
- POST that creates resources SHOULD return `201 Created` with a `Location` for the primary resource.
- Content in GET, HEAD and DELETE requests has no defined semantics and may be rejected as a request smuggling risk; a client SHOULD NOT send it unless the server has said it will support it. Sensitive data in a GET query string can leak in URIs; the spec points to POST for that case.
- A server that receives an unrecognized or unimplemented method SHOULD answer 501; a recognized method not allowed for the resource, 405. `Allow` lists the allowed methods.

## Gotchas
- Idempotent does not mean side-effect free: a DELETE that writes an audit log is still idempotent in intent.
- For a POST that must be retried, design a deduplication mechanism; the client cannot tell whether the first attempt was applied.

Verify: for each endpoint in the OpenAPI file, assert GET/HEAD handlers perform no writes (read-only DB role in test) and replay each PUT/DELETE twice, checking identical final state.

## Checked
2026-11-08. Confirmed against RFC 9110 section 9 (read through 9.3.6; OPTIONS, TRACE and the remaining method text not read in full) and RFC 5789 (searched for the safe/idempotent and Accept-Patch statements, not read in full). Removed: the "second DELETE returns 404" example, the Idempotency-Key and merge-patch advice, the QUERY method draft note, and the CORS preflight use of OPTIONS (not in the sources).
Method: documentation only; no commands were run.
