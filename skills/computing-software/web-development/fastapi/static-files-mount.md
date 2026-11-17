---
id: computing-software.web-development.fastapi.static-files-mount
name: static-files-mount
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, static-files, staticfiles, mount, sub-application]
level: intro
status: docs-checked
description: "Serve a directory of static files from FastAPI by mounting StaticFiles at a path, and what mounting means for routing and OpenAPI."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/static-files.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static files

## Method
- `from fastapi.staticfiles import StaticFiles` (same as `starlette.staticfiles`; FastAPI re-exports it as a convenience).
- Mount an instance: `app.mount("/static", StaticFiles(directory="static"), name="static")`. The page's example code is in a separate file, so this line is the standard form of its "mount a `StaticFiles()` instance in a specific path" step.
- `"/static"` is the sub-path: any path starting with it is handled by the mounted app. `directory` names the folder with the files. `name` gives it a name FastAPI can use internally. All three can differ from `static`.

## What mounting means
Mounting adds a complete, independent application at a path, which handles all sub-paths. Unlike `APIRouter`, the main app's OpenAPI and docs do not include anything from the mounted app.

## Frontends
To host a frontend, the page's tip says to use `app.frontend()` instead; it uses `StaticFiles` underneath and adds advantages such as client-side routing. Details are on the separate Frontend page.

## More
Starlette's static files documentation covers further options.

## Checked

Read the whole Static Files tutorial page. Removed the Verify step, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
