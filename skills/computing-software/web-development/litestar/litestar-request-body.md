---
id: computing-software.web-development.litestar.litestar-request-body
name: litestar-request-body
category: computing-software
field: web-development
product: litestar
tags: [litestar, request, body, jsonbody, msgpack, custom-request, request-class, openapi]
level: practitioner
status: docs-checked
description: "Receive and validate Litestar request bodies with JSONBody, MsgPackBody and Body, and set a custom Request class on any layer."
sources: [https://docs.litestar.dev/latest/usage/requests.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar request body

Goal: read a typed request body in a handler, with validation and OpenAPI metadata.

## Method

Use the special `data` parameter, declared with a body marker from `litestar.params`. For JSON:

```python
from litestar import Litestar, post
from litestar.params import JSONBody

@post(path="/")
async def index(data: JSONBody[dict[str, str]]) -> dict[str, str]:
    return data
```

`data` can be a stdlib type, a `TypedDict`, a dataclass, or a type supported via plugins: msgspec `Struct`, Pydantic models, attrs classes.

Validation and OpenAPI customization: use the `Body` class in the `Annotated` form:

```python
data: Annotated[User, Body(title="Create User", description="Create a new user.")]
```

Content type: Litestar parses the body as JSON by default. Pass a `RequestEncodingType` to `Body` to choose another one (this also sets the OpenAPI media type). Shorthands:
- `URLEncodedBody[T]` = `Annotated[T, Body(media_type=RequestEncodingType.URL_ENCODED)]`
- `MultipartBody[T]` = `Annotated[T, Body(media_type=RequestEncodingType.MULTI_PART)]`
- `MsgPackBody[T]` = `Annotated[T, Body(media_type=RequestEncodingType.MESSAGEPACK)]`; per the example comment it parses MessagePack regardless of `Content-Type`.

Use the `Annotated` form when you need extra OpenAPI metadata or constraints.

Custom request class (added in 2.7.0): subclass `Request`, then set `request_class=CustomRequest` on `Litestar(...)`. Handlers then declare `request: CustomRequest`. It can be set on any layer; the layer closest to the handler wins.

```python
class CustomRequest(Request):
    __slots__ = ("kitten_name",)
    def __init__(self, scope, receive=empty_receive, send=empty_send) -> None:
        super().__init__(scope=scope, receive=receive, send=send)
        self.kitten_name = "Mittens"
```

## Gotchas

- URL-encoded data cannot handle complex dictionaries or deeply nested data; keep it to simple structures.
- `request_max_body_size` can be set on any layer and defaults to 10MB; a larger body gets a `413 - Request Entity Too Large` response. Setting it to `None` disables the limit and is strongly discouraged (DoS risk).

## Verify

For the `@get(path="/kitten-name")` example returning `request.kitten_name`, a GET returns the name the class sets for that method (`"Whiskers"` for GET in the page's map).

## Checked

2026-11-07. Read the full cited page(s) (usage/requests.html) and the example files they include, and confirmed the claims in this skill against that text. Replaced a pointer to a nonexistent form/upload skill with the request_max_body_size default (10MB), 413 response and the discouraged None setting.

Method: documentation only; no commands were run.
