---
id: computing-software.web-development.litestar.litestar-response-media-types
name: litestar-response-media-types
category: computing-software
field: web-development
product: litestar
tags: [litestar, response, media-type, json, msgpack, plaintext, html, content-negotiation]
level: practitioner
status: docs-checked
description: "Choose Litestar response media types (JSON, MessagePack, text, HTML, +json suffix) and negotiate content with Request.accept."
sources: [https://docs.litestar.dev/latest/usage/responses.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar response media types

Goal: return the right serialization and `Content-Type` from a handler.

## Method

Returning a value is the base pattern. A returned pydantic model gives status 200 and `application/json` by default; JSON is the default `media_type`.

Set `media_type` on the decorator with `MediaType` (from `litestar`). It affects both serialization and the OpenAPI docs:
- `MediaType.JSON`: `application/json`
- `MediaType.MESSAGEPACK`: `application/x-msgpack` (same supported types as JSON)
- `MediaType.TEXT`: `text/plain`; return `str` or `bytes`
- `MediaType.HTML`: `text/html`; return `str` or `bytes` containing HTML

```python
@get(path="/health-check", media_type=MediaType.MESSAGEPACK)
def health_check() -> Dict[str, str]:
    return {"hello": "world"}
```

JSON serializes dataclasses, pydantic dataclasses and models (and libraries extending them), UUIDs, datetime objects, `msgspec.Struct`, and dict/list containers of those. A `+json` suffix media type per RFC 6839 (for example `application/vnd.example.resource+json`) serializes as JSON with the right content-type and OpenAPI entry.

Any IANA media type string is allowed; OpenAPI is still correct, but serialization needs a custom response class with a serializer or serializing inside the handler. For anything beyond defaults, use a template engine for complex HTML rather than inline strings.

Content negotiation: use `request.accept.best_match(...)`:

```python
@get("/resource")
def retrieve_resource(request: Request[Any, Any, Any]) -> Response[bytes | None]:
    provided_types = [MediaType.TEXT, MediaType.HTML, "application/xml"]
    preferred_type = request.accept.best_match(provided_types, default=MediaType.TEXT)
    ...
    return Response(content=content, media_type=preferred_type)
```

Custom response classes (`response_class`) are layered; the layer closest to the handler wins.

## Gotchas

- Type the `Response` generic argument (use `None` for empty bodies); otherwise it defaults to `Any` and the OpenAPI docs are imprecise.
- For `Template`, `File`, `Stream` and `Redirect` use the response containers from `litestar.response`, or OpenAPI is generated incorrectly.

## Verify

The page's example is called with `/resource`, `/resource -H "Accept: text/html"` and `/resource -H "Accept: application/xml"`; each should return the body matching the preferred type.

## Checked

2026-11-07. Read the full cited page(s) (usage/responses.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
