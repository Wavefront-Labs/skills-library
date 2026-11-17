---
id: computing-software.web-development.strapi.request-response-context
name: request-response-context
category: computing-software
field: web-development
product: strapi
tags: [strapi, ctx, koa, request-context, ctx-state, requestcontext]
level: intro
status: docs-checked
description: "The Koa ctx object in Strapi: ctx.request, ctx.state, ctx.response, and reaching the request context from anywhere."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/requests-responses.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Request and response context

Strapi's back end is based on Koa. A context object `ctx` is passed to every element of the back end and contains three main objects:

- `ctx.request`: what the client sent
- `ctx.state`: state of the request within Strapi
- `ctx.response`: what the server will return

The request context can also be accessed from code with `strapi.requestContext.get()` (for example in lifecycle hooks). Call it inside functions that run during an HTTP request, not at module top level. Strapi uses Node.js `AsyncLocalStorage` for this.

## Useful `ctx.request` fields
| Field | Meaning |
|---|---|
| `ctx.request.body` | parsed body |
| `ctx.request.files` | files sent |
| `ctx.request.headers` | headers |
| `ctx.request.ip` | IP of the sender |
| `ctx.request.method` | `GET`, `POST`... |
| `ctx.request.params` | URL parameters; for `/restaurants/:id`, `ctx.request.params.id` |
| `ctx.request.path` | path without query |
| `ctx.request.query` | Strapi-specific query parameters (`sort`, `filters`, `populate`, `fields`, `pagination`, `status`, `locale`); `ctx.query` is the whole query object |
| `ctx.request.url` | path plus query parameters |

## `ctx.state`
- `ctx.state.isAuthenticated`: whether the user is authenticated in any way.
- `ctx.state.user` (and `ctx.state.user.role`): the user performing the request.
- `ctx.state.auth.strategy.name`: the authentication strategy in use (Users & Permissions plugin or API tokens); `ctx.state.auth.credentials` holds the credentials.
- `ctx.state.route`: `method`, `path`, `config`, `handler`, and `info.apiName` / `info.type`.

## `ctx.response`
`body`, `status`, `message` (tied to `status` by default), `header`/`headers`, `length`, `redirect(url, [alt])` (302), `attachment([filename], [options])`, `type`, `lastModified`, `etag`.

Koa's own docs cover more of the request and response APIs.

## Checked

2026-11-04: checked against the Strapi docs page Requests and Responses (backend-customization/requests-responses). Confirmed: Koa base, the three main objects, the listed ctx.request fields, the query parameters. Corrected: `strapi.requestContext` is used as `strapi.requestContext.get()` and only inside request-time functions. Removed: the `policyContext.state.user` line, which this page does not state. Added: ctx.state and ctx.response members.

Method: documentation only; no commands were run.
