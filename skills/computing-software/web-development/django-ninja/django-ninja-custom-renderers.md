---
id: computing-software.web-development.django-ninja.django-ninja-custom-renderers
name: django-ninja-custom-renderers
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, renderers, baserenderer, jsonrenderer, orjson, xml, csv]
level: practitioner
status: docs-checked
description: "Swap the Django Ninja response renderer with a BaseRenderer subclass (orjson, XML, CSV) or tweak JSONRenderer encoder_class and json_dumps_params."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/renderers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom renderers

One renderer per `NinjaAPI` instance serializes every response, including Ninja's own error responses. There is no per-router or per-operation override.

```python
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer

class TextRenderer(BaseRenderer):
    media_type = "text/plain"

    def render(self, request, data, *, response_status):
        return str(data)

api = NinjaAPI(renderer=TextRenderer())
```

## BaseRenderer contract

- `media_type`: used in `Content-Type`.
- `charset`: defaults to `"utf-8"`.
- `render(self, request, data, *, response_status)`: gets the request, the (already validated) view result and the int status; return `str` or `bytes`.

## Default JSONRenderer

Uses stdlib `json`. Override `encoder_class` (default `ninja.responses.NinjaJSONEncoder`, extending `DjangoJSONEncoder`, which also handles Pydantic models, URLs, IP types and Enums) or `json_dumps_params` (kwargs for `json.dumps`):

```python
from ninja.renderers import JSONRenderer

class PrettyJSONRenderer(JSONRenderer):
    json_dumps_params = {"indent": 2}

api = NinjaAPI(renderer=PrettyJSONRenderer())
```

## orjson

```python
import orjson

class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)
```

`orjson.dumps` returns bytes, which Django's `HttpResponse` accepts.

## CSV (single known shape)

```python
class CSVRenderer(BaseRenderer):
    media_type = "text/csv"

    def render(self, request, data, *, response_status):
        rows = [",".join(data[0].keys())]
        rows += [",".join(map(str, item.values())) for item in data]
        return "\n".join(rows)
```

The docs also show an XML renderer built on `SimplerXMLGenerator` (from `django.utils.xmlutils`) that recurses over lists and dicts.

## Gotchas

- Error payloads are plain dicts and go through your renderer too, so make it defensive; the CSV and XML examples only suit their intended shapes.
- Keep the renderer stateless; one instance serves all requests.
- `get_content_type()` always appends `; charset=...`. `charset = ""` leaves a trailing `charset=`; override `get_content_type()` on a `NinjaAPI` subclass for a bare media type.
- Renderers (output) are independent of request parsers (input).

## Checked

2026-11-07: Confirmed against guide/renderers.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
