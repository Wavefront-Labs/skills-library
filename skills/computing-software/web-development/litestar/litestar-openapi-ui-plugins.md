---
id: computing-software.web-development.litestar.litestar-openapi-ui-plugins
name: litestar-openapi-ui-plugins
category: computing-software
field: web-development
product: litestar
tags: [litestar, openapi, openapi-ui, swagger, redoc, scalar, ui-plugin, render-plugins]
level: practitioner
status: docs-checked
description: "Serve Swagger UI, ReDoc, Scalar, Stoplight or YAML docs in Litestar through render_plugins, change the schema root path and write a custom OpenAPIRenderPlugin."
sources: [https://docs.litestar.dev/latest/usage/openapi/ui_plugins.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar OpenAPI UI plugins

Goal: choose and configure the OpenAPI documentation UIs (added in 2.8.0).

## Method

1. Import from `litestar.openapi.plugins`: `ScalarRenderPlugin`, `RedocRenderPlugin`, `StoplightRenderPlugin`, `SwaggerRenderPlugin`, `YamlRenderPlugin`.
2. Pass instances to `OpenAPIConfig(title=..., version=..., render_plugins=[ScalarRenderPlugin(), SwaggerRenderPlugin()])`. Any combination can be served together.
3. `YamlRenderPlugin` needs PyYAML, from the `litestar[yaml]` extra.
4. Options for all plugins: `path` (each has its own default, for example `/scalar`), `media_type` (typically `text/html`), `favicon` (a valid `<link>` tag string), `style` (a valid `<style>` tag string).
5. Most plugins also take `version` (bundle version, used to build an `unpkg` URL), `js_url` and `css_url`. `js_url`/`css_url` override `version`, so they let you serve from a CDN, an internal host or local files, for example `RedocRenderPlugin(version="latest", google_fonts=True, path="/redoc", js_url="https://cdn.company.internal/redoc/custom-redoc.js")`.
6. Root path: the OpenAPI endpoints default to `/schema`. Set `OpenAPIConfig(path="/docs")` to get `/docs/openapi.json`.
7. Swagger OAuth2: `SwaggerRenderPlugin(init_oauth={"clientId": "your-client-id", "appName": "your-app-name", "scopeSeparator": " ", "scopes": "openid profile", "usePkceWithAuthorizationCodeGrant": True})`.
8. Custom UI: subclass `OpenAPIRenderPlugin` and implement `render(self, request, openapi_schema: dict) -> bytes`. It receives the request and the schema dict and returns a complete HTML document as bytes (head with title from the schema, body with a link to the OpenAPI JSON and the JS bundle). Accept `version`, `js_url`, `css_url`, `path` and `**kwargs` in `__init__` and build the bundle URL when `js_url` is absent.
9. Router access: override `receive_router(self, router: Router) -> None` to get the `Router` that serves the OpenAPI endpoints, for example to add extra routes.

## Verify

With `path="/docs"` the page says endpoints are served at `/docs`, for example `/docs/openapi.json`.

## Checked

2026-11-07. Read the full cited page(s) (usage/openapi/ui_plugins.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
