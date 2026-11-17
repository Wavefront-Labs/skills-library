---
id: computing-software.web-development.fastapi.path-convertor-file-paths
name: path-convertor-file-paths
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-parameters, starlette, path-convertor, file-path]
level: practitioner
status: docs-checked
description: "Capture a whole sub-path including slashes in a FastAPI route with the Starlette :path convertor, and handle a leading slash with a double slash URL."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path parameters that contain paths

Goal: let one parameter hold a value like `dir/sub/myfile.txt`.

## Method
- Use the Starlette option in the route: `/files/{file_path:path}`. The parameter name is `file_path`; the trailing `:path` tells it to match any path.
- The URL for the example becomes `/files/dir/sub/myfile.txt`.
- If the value must start with a slash, such as `/dir/sub/myfile.txt`, the URL has a double slash: `/files//dir/sub/myfile.txt`.

## Limitation
OpenAPI has no way to declare that a path parameter contains a path, so the docs still work but do not say the parameter holds a path.

## Verify
Request the URL with nested segments and confirm the function received the whole sub-path in one argument.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
