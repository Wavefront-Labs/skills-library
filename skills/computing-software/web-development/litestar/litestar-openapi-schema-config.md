---
id: computing-software.web-development.litestar.litestar-openapi-schema-config
name: litestar-openapi-schema-config
category: computing-software
field: web-development
product: litestar
tags: [litestar, openapi, schema, openapi-config, operation, responsespec, examples, pydantic]
level: practitioner
status: docs-checked
description: "Configure Litestar OpenAPI generation with OpenAPIConfig, per-handler schema kwargs, ResponseSpec, custom Operation classes, schema names and generated examples."
sources: [https://docs.litestar.dev/latest/usage/openapi/schema_generation.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar OpenAPI schema configuration

Goal: control the generated OpenAPI schema at app, handler and model level.

## Method

- Schema generation is on by default. Configure it: `Litestar(route_handlers=[...], openapi_config=OpenAPIConfig(title="My API", version="1.0.0"))` (`from litestar.openapi import OpenAPIConfig`).
- Disable it and drop the schema endpoints with `openapi_config=None`.
- Omit one handler: `@get(path="/some-path", include_in_schema=False)`.
- Per-handler kwargs: `tags`, `security`, `summary`, `description`, `response_description`, `operation_class` (an `Operation` subclass), `operation_id` (string or callable returning a string), `deprecated` (default `False`), `raises` and `responses`.
- `raises`: list of `HttpException` subclasses. `ValidationException` is added automatically when parameters are validated. Custom exceptions should define a `detail` class property; without it, a generic message is used when the status code matches a stdlib status code.
- `responses`: extra status codes, for example `responses={404: ResponseSpec(data_container=ItemNotFound, description="Item was removed or not found")}` (`from litestar.openapi.datastructures import ResponseSpec`).
- `operation_id` is prefixed with the method name when a handler has multiple `http_method`s, and with Router and Controller path strings, to keep it unique.
- `security` and `tags` can also be set on a controller, router or the app. `security=[{}]` marks optional security. Define schemes in `OpenAPIConfig(security=[{"BearerToken": []}], components=Components(security_schemes={"BearerToken": SecurityScheme(type="http", scheme="bearer")}), tags=[Tag(name="public", description="...")])` (from `litestar.openapi.spec`).
- Read the schema in code: `request.app.openapi_schema`, then `.to_schema()`. It is built during app init.
- Pydantic model component names: set `__schema_name__ = "IdContainer"` on the model. Two models sharing a name need distinct `__schema_name__` values, otherwise components are ambiguous.
- Custom `Operation` subclass: useful when you parse request data manually. Vendor extension fields must start with `x-`; Litestar honours an `alias` in the dataclass `field` metadata for that name.
- Generated examples: install `polyfactory` (extras `litestar[polyfactory]` or `litestar[full]`) and turn the feature on through the OpenAPI config (the page shows no option name).

## Verify

Per the page, the `__schema_name__ = "IdContainer"` example produces `"$ref": "#/components/schemas/IdContainer"` in the returned schema.

## Checked

2026-11-07. Read the full cited page(s) (usage/openapi/schema_generation.html) and the example files they include, and confirmed the claims in this skill against that text. Removed the create_examples option name, which the cited page never shows.

Method: documentation only; no commands were run.
