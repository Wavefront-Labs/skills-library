---
id: computing-software.web-development.fastapi.cookie-parameters
name: cookie-parameters
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, cookie-parameters, cookie, request, docs-ui]
level: intro
status: docs-checked
description: "Read cookies in FastAPI with Cookie, why plain parameters become query parameters instead, and why Swagger UI cannot send cookies."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/cookie-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookie parameters

Goal: receive cookie values as typed arguments.

## Rules
- Import `Cookie` from `fastapi` and declare parameters with the same structure as `Path` and `Query`; defaults and validation arguments are accepted.
- `Cookie` is a sister of `Path` and `Query` and inherits from the common `Param` class.
- You must use `Cookie`; without it the parameter would be interpreted as a query parameter.

## Docs UI limitation
Browsers handle cookies in special ways and do not easily let JavaScript touch them. The `/docs` page shows the cookie documentation, but filling in values and clicking Execute will not send them and you will see an error as if no values were written. Test with a real client.

## Related
For grouped cookies use the parameter-models skill.

## Verify
Call the route with a cookie header from a command-line client and check the value is received.

## Checked

Confirmed on the cited FastAPI cookie-params tutorial page: `Cookie` declared like `Path` and `Query`, the shared `Param` base class, the need to use `Cookie`, and the `/docs` UI not sending cookies. Removed: nothing. The "test with a real client" advice is a practical inference from the docs UI note.

Method: docs-only read of cited pages, 2026-11-08
