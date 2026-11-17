---
id: computing-software.web-development.fastapi.custom-response-classes
name: custom-response-classes
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, response-class, htmlresponse, streamingresponse, fileresponse, redirectresponse, custom-response, default-response-class]
level: practitioner
status: docs-checked
description: "Choose FastAPI response classes: HTMLResponse, PlainTextResponse, RedirectResponse, StreamingResponse, FileResponse, custom classes, and the performance and docs trade-offs."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/custom-response.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom responses

## Rules
- Default is JSON. For best performance declare a response model/return type and no `response_class`; Pydantic then serializes directly.
- `response_class=` on the decorator wraps your returned content, sets the `Content-Type` media type and documents it in OpenAPI. With a JSON media type the data is still filtered by `response_model`, but converted with `jsonable_encoder` then the standard JSON library.
- A `Response` returned directly skips conversion and `response_model`, and its format is not documented in OpenAPI. To override in the function and still document, set `response_class` too and return a `Response`; `response_class` is then only for docs.
- A response class with no media type means FastAPI expects no content and documents no format.
- Classes come from `fastapi.responses` (Starlette's).

## Classes
- `Response(content, status_code, headers, media_type)`: base class; adds `Content-Length` and `Content-Type`.
- `HTMLResponse`, `PlainTextResponse`, `JSONResponse`.
- `RedirectResponse`: default status 307; usable in `response_class` so you can return the URL string; combine with `status_code`.
- `StreamingResponse`: takes a (async) generator. A generator without an `await` cannot be cancelled properly, so the docs add `await anyio.sleep(0)`. The docs prefer their Stream Data pages.
- `FileResponse(path, headers, media_type, filename)`: infers media type if unset, sets `Content-Length`, `Last-Modified`, `ETag`; with `response_class` return the path.

## Custom and default
- Subclass `Response` and implement `render(content)` returning `bytes` (docs example: orjson with `OPT_INDENT_2`). For speed, a response model already beats orjson.
- `default_response_class` on `FastAPI` or `APIRouter` sets the default; per-operation `response_class` still overrides.

## Verify
Check `Content-Type` and `/docs` for the media type.

## Checked

Read the full advanced/custom-response.md source page. Confirmed JSON default and performance advice, response_class behaviour, direct Response not documented, no-media-type note, the Response/FileResponse parameters, RedirectResponse 307 default, StreamingResponse cancellation note with anyio.sleep(0), FileResponse headers, custom render(content) returning bytes with orjson OPT_INDENT_2, and default_response_class. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
