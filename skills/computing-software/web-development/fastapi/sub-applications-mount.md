---
id: computing-software.web-development.fastapi.sub-applications-mount
name: sub-applications-mount
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, sub-application, mount, root-path, openapi, independent-app]
level: advanced
status: docs-checked
description: "Mount an independent FastAPI sub-application with app.mount so it gets its own OpenAPI schema and docs UI under a sub-path, and how root_path is handled."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/sub-applications.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sub applications

Use when you need two independent apps, each with its own OpenAPI and docs UI.

## Method
- Create the top-level `app = FastAPI()` with its path operations.
- Create `subapi = FastAPI()` with its own path operations.
- Mount: `app.mount("/subapi", subapi)`.
- The main docs at `/docs` show only the main app's operations; the sub-app docs are at `/subapi/docs` with only its operations under the `/subapi` prefix. Both UIs work.

## Behaviour
- FastAPI passes the mount path to the sub-app through ASGI `root_path`, so the sub-app's docs UI uses the prefix. Nested sub-apps work the same.
- A mounted app is completely independent and handles everything under its path; `root_path` is explained in the "Behind a Proxy" section.

## Verify
Open both docs URLs and call an operation from each.

## Checked

Confirmed on the cited FastAPI sub-applications page: independent apps with their own OpenAPI and docs UIs, creating, mounting at `/subapi`, main docs showing only the main operations, sub-app docs at `/subapi/docs`, and `root_path` handling including nested sub-apps. Removed (not on the page): the comparison with `APIRouter` and the lifespan-events limitation (that is on the events page, which this skill does not cite).

Method: docs-only read of cited pages, 2026-11-08
