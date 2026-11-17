---
id: creative-arts.design-for-form-and-experience.figma.using-the-variables-rest-api-and-import-export
name: using-the-variables-rest-api-and-import-export
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [variables-rest-api, figma-variables-api, variables-import-export, token-export, figma-api-variables, tokens-sync]
level: advanced
status: docs-checked
description: "Read and write Figma variables through the Variables REST API, export to token files, and import from JSON, with plan and scope requirements to verify."
sources:
  - https://developers.figma.com/docs/rest-api/variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Variables REST API and import and export

Figma exposes variables through a REST API so you can sync them with code and token files. The Variables REST API requires an Enterprise plan, so confirm your plan before building on it.

## Endpoints
- **GET local variables:** returns the variables in a file. Needs the `file_variables:read` scope and view access to the file.
- **GET published variables:** the library's published variables. Same scope and access.
- **POST variables:** creates and updates variables. Needs the `file_variables:write` scope, edit access to the file, and a Full seat or admin role.
- Guests cannot use the API. Find exact paths and payload shapes on the Variables page of the developer docs.
- Never commit tokens; read them from an environment variable.

## Export
1. Call the local variables endpoint and walk collections, modes and variables.
2. Resolve alias entries to token paths.
3. Convert colour values to hex or your target format (check the response schema for the colour representation).
4. Write DTCG or Style Dictionary JSON (see `...design-systems.writing-tokens-in-the-dtcg-json-format`).

## Import
Transform a token file into the POST payload and run it against a test file first. Community import and export plugins cover the same ground without custom code.

## Verify
- [ ] Round trip: export, import to a test file, export again, and compare.
- [ ] Aliases survive the round trip.
- [ ] Tokens and secrets are not stored in the repo.

## Checked
2026-11-01. Confirmed on the Figma Variables REST API page: the three endpoints (GET local, GET published, POST), the `file_variables:read` and `file_variables:write` scopes, the Enterprise requirement, Full seat or admin for POST, file view and edit access, no guests. Removed: URL paths, temporary-ID behaviour, the `VARIABLE_ALIAS` name, the 0 to 1 RGBA statement, OAuth wording and named plugins' behaviour, none stated on the page read.
Method: documentation only; no commands were run.
