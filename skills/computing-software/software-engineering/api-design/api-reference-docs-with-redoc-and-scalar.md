---
id: computing-software.software-engineering.api-design.api-reference-docs-with-redoc-and-scalar
name: api-reference-docs-with-redoc-and-scalar
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-reference-docs, redoc, scalar, openapi, developer-portal, docs-as-code]
level: practitioner
status: docs-checked
description: "Publish API reference docs from OpenAPI with Redoc or Scalar: build pipeline, examples, auth guides, try-it consoles and docs linting."
sources: ["https://redocly.com/docs/redoc", "https://github.com/scalar/scalar", "https://redocly.com/docs/cli/commands/build-docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference docs and developer portals (Redoc / Scalar)

## Generate reference from the spec, write the rest by hand
Reference (endpoints, schemas, errors) comes from OpenAPI so it can't drift; guides (quickstart,
auth, pagination, errors, webhooks, changelog) are hand-written Markdown in the same repo.

## Redoc
```
npx @redocly/cli build-docs openapi.yaml -o dist/api.html     # static single page
```
`build-docs` writes `redoc-static.html` by default (`--output`/`-o` changes it), renders with Redoc 3, loads the Redoc scripts from the Redocly CDN unless you pass `--inlineBundle`, and sends reader-side telemetry unless turned off (`REDOCLY_TELEMETRY=off` or `telemetry: off` in the config). It accepts OpenAPI, AsyncAPI and GraphQL inputs; options come from the `openapi`, `asyncapi` or `graphql` key of `redocly.yaml` or from `--openapi.<option>` flags.
Or embed (Redoc CE 3.x):
`<redoc spec-url="/openapi.yaml"></redoc><script type="module" src="https://cdn.redoc.ly/redoc/v3.x/bundles/redoc.standalone.js"></script>`.
Redoc CE has a three-panel layout (with a stacked option), search, light and dark modes, payload samples, and reads `x-logo`, `x-tagGroups` and `x-codeSamples`.

## Scalar
```html
<div id="app"></div>
<script type="module">
  import { createApiReference } from 'https://cdn.jsdelivr.net/npm/@scalar/api-reference/esm.js'
  createApiReference('#app', { url: '/openapi.yaml' })
</script>
```
Scalar's README describes an API reference with a built-in API testing tool and generated code examples, plus integrations for ASP.NET Core, Express, FastAPI, NestJS, Django, Spring Boot, Docusaurus and many more; see scalar.com for the integration to use. The README's example sets `proxyUrl` to avoid CORS issues when testing against another origin.

## Content quality in the spec
- `summary` + `description` on every operation, `description` on every field, with units and limits.
- `examples` for requests and responses, including error responses (problem+json).
- `x-codeSamples` (read by Redoc) for curl/Python/JS snippets, or generate from SDKs.
- Tags group operations; `x-tagGroups` for sidebar sections.
- Security schemes documented with how to obtain credentials.
- Lint rules requiring descriptions, examples and operationIds.

## Portal
Docs site with search, versioned reference per API version, changelog, status link, SDK links, and a sandbox key flow. Deploy on every merge to main; preview deploys on PRs so reviewers read rendered docs (project practice, not from the sources).

## Checked
2026-11-08. Confirmed by reading the Redoc CE overview and the Redocly CLI `build-docs` page in full, and the first part of the Scalar README (about 230 lines; the rest not needed). The OpenAPI 3.1.0 spec source was not used for any remaining claim. Replaced the old `<script id="api-reference" data-url>` Scalar snippet with the README's `createApiReference` form. Removed (not in the sources): "no built-in try-it in open-source Redoc", `MapScalarApiReference()`, "Swagger UI is the default in many frameworks", the lint command and the portal product names. The Redoc `latest` CDN path was changed to `v3.x`, as the Redoc page shows.
Method: documentation only; no commands were run.
