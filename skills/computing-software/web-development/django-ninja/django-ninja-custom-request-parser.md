---
id: computing-software.web-development.django-ninja.django-ninja-custom-request-parser
name: django-ninja-custom-request-parser
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, request-parsers, parser, yaml, orjson, querydict]
level: advanced
status: docs-checked
description: "Replace the Django Ninja request Parser to accept YAML or orjson bodies or change how query, form and file lists are read."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/parsers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom request parsers in Django Ninja

Goal: change how the request body or query data is parsed, API-wide.

The default `ninja.parser.Parser` parses `Body` with the `json` module and reads `Query`, `Form`, `File` from Django's `QueryDict`. Pass your own instance:

```python
from ninja import NinjaAPI
from ninja.parser import Parser

api = NinjaAPI(parser=Parser())
```

The parser is set once per `NinjaAPI`; there is no per-router or per-operation override.

## Override points
- `parse_body(self, request)`: returns the dict-like data for `Body` parameters.
- `parse_querydict(self, data, list_fields, request)`: for `Query`, `Form`, `File`; `data` is a QueryDict, `list_fields` the names declared with a list type. Default returns single values and `.getlist(...)` for list fields.

Overriding one keeps the default for the other.

## YAML

```python
import yaml

class MyYamlParser(Parser):
    def parse_body(self, request):
        return yaml.safe_load(request.body)

api = NinjaAPI(parser=MyYamlParser())
```

Content-Type is not inspected; raw bytes go to `parse_body`.

## orjson

```python
import orjson

class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)
```

## Comma-separated lists

```python
class CommaSeparatedListParser(Parser):
    def parse_querydict(self, data, list_fields, request):
        result = {}
        for key in data.keys():
            if key in list_fields:
                result[key] = data[key].split(",")
            else:
                result[key] = data[key]
        return result
```

`?tags=red,green,blue` then gives `["red","green","blue"]` for every list in `Query`/`Form`/`File`, replacing repeated keys.

## Gotchas
- Errors from `parse_body` become an HTTP 400 ("Cannot parse request body", with the exception message appended when `DEBUG=True`). Errors from `parse_querydict` are not caught the same way, so be defensive.
- Parsers affect only incoming data; responses use the renderer.

## Checked

2026-11-07: Confirmed against guide/parsers.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
