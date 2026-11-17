---
id: computing-software.web-development.fastapi.path-route-order
name: path-route-order
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-operations, route-order, path-parameters, routing]
level: practitioner
status: docs-checked
description: "Declare fixed FastAPI paths such as /users/me before parameterised ones like /users/{user_id}, because path operations match in declaration order."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route declaration order

Goal: stop a parameterised route from swallowing a fixed one.

## Rule
Path operations are evaluated in order. If you have `/users/me` (data about the current user) and `/users/{user_id}` (data about a specific user), declare `/users/me` first.

Otherwise `/users/{user_id}` also matches `/users/me`, receiving a `user_id` with the value `"me"`.

## Related
- You cannot redefine a path operation: when two declarations have the same path, the first one is always used because the path matches first.

## Verify
Request `/users/me` and confirm the fixed handler answers, not the parameterised one. If you reorder code, re-test both URLs.

## Checked

Read the "Order matters" section of the Path Parameters tutorial page; the rule and the same-path note match.

Method: docs-only read of cited pages, 2026-11-08
