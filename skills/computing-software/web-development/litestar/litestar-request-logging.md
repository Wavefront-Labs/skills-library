---
id: computing-software.web-development.litestar.litestar-request-logging
name: litestar-request-logging
category: computing-software
field: web-development
product: litestar
tags: [litestar, logging, request-logging, loggingmiddleware, structlog, obfuscation, structured-logging, middleware]
level: practitioner
status: docs-checked
description: "Log Litestar requests and responses with LoggingMiddleware, choose logged fields, obfuscate headers and cookies, handle compressed bodies and use structlog."
sources: [https://docs.litestar.dev/latest/usage/logging.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar request logging

Goal: log requests and responses through `LoggingMiddleware` with any compatible logger.

## Method

1. Add the middleware with a `logging.Logger`-compatible object (or a callable returning one):

```python
from litestar.middleware.logging import LoggingMiddleware

app = Litestar(
    route_handlers=[my_handler],
    middleware=[
        LoggingMiddleware(
            logging.getLogger("my.app"),
            request_log_fields=("query", "body"),  # only log query and body fields
        )
    ],
)
```

2. Default request properties: `path`, `method`, `content_type`, `query_params`, `path_params`. Default response property: `status_code`. Pick fields with `request_log_fields` and `response_log_fields`.
3. Obfuscation: `request_cookies_to_obfuscate`, `response_cookies_to_obfuscate`, `request_headers_to_obfuscate`, `response_headers_to_obfuscate`, each a set, for example `{"my-custom-header"}`. By default the `Authorization` and `X-API-KEY` headers and the `session` cookie are obfuscated.
4. Structured logging: `log_structured=True`; the logger must accept arbitrary keyword arguments.
5. structlog: pass the logger directly, `LoggingMiddleware(structlog.get_logger("my.app"), request_log_fields=("query", "body"))`.

## Gotchas

- With both `CompressionConfig` and `LoggingMiddleware`, the response body is omitted from logs when compressed, even if `"body"` is in `response_log_fields`. Also set `include_compressed_body=True` (with `"body"` in `response_log_fields`) to force it.

## Verify

Request the `/` handler and check your logger output contains the configured fields (the page's example logs `query` and `body`).

## Checked

2026-11-07. Read the full cited page(s) (usage/logging.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
