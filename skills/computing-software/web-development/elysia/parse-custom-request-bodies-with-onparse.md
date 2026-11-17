---
id: computing-software.web-development.elysia.parse-custom-request-bodies-with-onparse
name: parse-custom-request-bodies-with-onparse
category: computing-software
field: web-development
product: elysia
tags: [elysia, life-cycle, parse, onparse, body-parser, content-type]
level: advanced
status: docs-checked
description: "Control how Elysia parses a request body: default content types, explicit parse option, a named custom parser, and parse none for third-party handlers."
sources:
  - https://elysiajs.com/essential/life-cycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: parse a body type Elysia does not handle, force a parser, or skip parsing.

## Defaults

Elysia parses `text/plain`, `application/json`, `multipart/form-data` and `application/x-www-form-urlencoded`. The result goes to `Context.body`. Elysia also picks a parser ahead of time from the body schema:

- `application/json`: body typed as `t.Object`
- `multipart/form-data`: `t.Object` one level deep containing `t.File`
- `application/x-www-form-urlencoded`: `t.URLEncoded`
- `text/plain`: other primitive types

## Custom parser with onParse

The context adds `contentType`. Return a value to assign it to `body`; if nothing is returned Elysia tries the next parser on the `onParse` stack until the body is set or all have run.

```typescript
new Elysia().onParse(({ request, contentType }) => {
	if (contentType === 'application/custom-type') return request.text()
})
```

## Force a parser

```typescript
.post('/', ({ body }) => body, { parse: 'json' })
```

Allowed values: `'text'`, `'json'`, `'formdata'`, `'urlencoded'`, `'none'`, or the full `text/plain`, `application/json`, `multipart/form-data`, `application/x-www-form-urlencoded`.

## Named parser

```typescript
new Elysia()
	.parser('custom', ({ request, contentType }) => {
		if (contentType === 'application/elysia') return request.text()
	})
	.post('/', ({ body }) => body, { parse: ['custom', 'json'] })
```

## Skip parsing for a library

A Web Standard Request body can be read only once. If tRPC or oRPC fails with `Body is already used`, set `parse: 'none'` so the library reads `request` itself:

```typescript
.post('/', ({ request }) => library.handle(request), { parse: 'none' })
```

## Gotchas

- Like beforeHandle and mapResponse, a parser returning a value stops later parsers.

## Checked

2026-11-07. Read in full: essential/life-cycle (Parse section). Confirmed default content types, ahead-of-time parser choice by schema, `contentType` in the onParse context, fall-through to the next parser, `parse` values, named `.parser()`, and `parse: 'none'` for libraries that read the body themselves. Removed the claim that body parsing is disabled for GET and HEAD; the page does not say it.

Method: documentation only; no commands were run.
