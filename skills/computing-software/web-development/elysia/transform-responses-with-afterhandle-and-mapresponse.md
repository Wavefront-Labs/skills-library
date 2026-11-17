---
id: computing-software.web-development.elysia.transform-responses-with-afterhandle-and-mapresponse
name: transform-responses-with-afterhandle-and-mapresponse
category: computing-software
field: web-development
product: elysia
tags: [elysia, life-cycle, after-handle, map-response, after-response, compression]
level: advanced
status: docs-checked
description: "Modify an Elysia response after the handler: set headers with afterHandle, replace the body, compress in mapResponse and log in afterResponse."
sources:
  - https://elysiajs.com/essential/life-cycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: change what the client receives without touching every handler.

## afterHandle

Runs after the route handler, on the value returned by beforeHandle or the handler. Use for adding headers based on the value, or transforming it (compression, event stream). The context adds the response value; the docs' examples name it both `response` and `responseValue`, so check the types in your editor.

```typescript
new Elysia().get('/', () => '<h1>Hello World</h1>', {
	afterHandle({ response, set }) {
		if (isHtml(response)) {
			set.headers['content-type'] = 'text/html; charset=utf8'
			return new Response(response)
		}
	}
})
```

If you return a value (other than `undefined`), it replaces the response. Unlike beforeHandle, returning a value does not skip the remaining afterHandle hooks.

## mapResponse

Runs right after afterHandle to map the value into a Web Standard Response (compression, custom mapping).

```typescript
new Elysia().mapResponse(({ responseValue, set }) => {
	const isJson = typeof responseValue === 'object'
	const text = isJson ? JSON.stringify(responseValue) : (responseValue?.toString() ?? '')
	set.headers['Content-Encoding'] = 'gzip'
	return new Response(Bun.gzipSync(new TextEncoder().encode(text)), {
		headers: { 'Content-Type': `${isJson ? 'application/json' : 'text/plain'}; charset=utf-8` }
	})
})
```

Elysia merges `set.headers` into the response for you. Once one mapResponse returns a value, later ones are skipped.

## afterResponse

Runs after the response is sent: cleanup, logging, analytics. `responseValue` is the handler's returned value, not a Web Standard `Response`; read status and headers from `set`:

```typescript
new Elysia().onAfterResponse(({ set }) => console.log(set.status, set.headers))
```

## Gotchas

- Register each hook before the routes it should affect.
- Default content types show up as `text/plain; charset=utf8` unless a hook changes them.

## Checked

2026-11-07. Read in full: essential/life-cycle (After Handle, Map Response, After Response sections). Confirmed the afterHandle example and replacement behaviour, the gzip mapResponse example, header merging, and afterResponse using `set`. Nothing removed.

Method: documentation only; no commands were run.
