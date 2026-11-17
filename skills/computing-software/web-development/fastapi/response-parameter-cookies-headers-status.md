---
id: computing-software.web-development.fastapi.response-parameter-cookies-headers-status
name: response-parameter-cookies-headers-status
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, response-parameter, set-cookie, response-headers, change-status-code, expose-headers]
level: practitioner
status: docs-checked
description: "Set cookies, headers and the status code in FastAPI through a temporary Response parameter while response_model still filters the returned data."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/response-cookies.md, https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/response-headers.md, https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/response-change-status-code.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response parameter: cookies, headers, status code

## Method
- Declare a parameter typed `Response` (`from fastapi import Response`) in the path operation function or in a dependency.
- Set cookies (`set_cookie`), headers, or `status_code` on that temporary object, then return any data (dict, database model...). FastAPI copies cookies, headers and status code into the final response; any `response_model` still filters and converts the returned data.
- Use case for status: default 200, but return 201 when the data had to be created.
- If several dependencies set the status code, the last one set wins.

## Returning a Response directly instead
- Create the response, set cookies on it (or pass `headers=` to the constructor) and return it. FastAPI returns it as is, so you must ensure JSON-compatible content and no data that a `response_model` should have filtered.

## Custom headers
Use the `X-` prefix for proprietary headers. For a browser client to read them, add them to CORS `expose_headers`.

## More
Starlette's Responses documentation lists all `set_cookie` options.

## Verify
Inspect the response headers and `Set-Cookie`.

## Checked

2026-11-08: Read the Response Cookies, Response Headers and Change Status Code pages (temporary Response parameter, response_model still applies, direct Response return, X- prefix and expose_headers, last dependency wins for status). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
