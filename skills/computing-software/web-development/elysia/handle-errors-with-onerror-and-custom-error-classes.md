---
id: computing-software.web-development.elysia.handle-errors-with-onerror-and-custom-error-classes
name: handle-errors-with-onerror-and-custom-error-classes
category: computing-software
field: web-development
product: elysia
tags: [elysia, error-handling, life-cycle, onerror, custom-error, not-found]
level: practitioner
status: docs-checked
description: "Catch Elysia errors with onError, branch on error codes such as NOT_FOUND and VALIDATION, and register custom error classes with status and toResponse."
sources:
  - https://elysiajs.com/essential/life-cycle.html
  - https://elysiajs.com/tutorial/patterns/error-handling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn thrown errors into controlled responses with correct status codes.

## onError

Runs when an error is thrown in any lifecycle stage. Its context is the normal context plus `error` (the thrown value) and `code`.

```typescript
new Elysia()
	.onError(({ code, status }) => {
		if (code === 'NOT_FOUND') return 'uhe~ are you lost?'
		return status(418, "My bad!")
	})
	.get('/', () => 'ok')
```

Codes: `NOT_FOUND`, `PARSE`, `VALIDATION`, `INTERNAL_SERVER_ERROR`, `INVALID_COOKIE_SIGNATURE`, `INVALID_FILE_TYPE`, `UNKNOWN` (default for thrown errors), or a number from an HTTP status. If no response is returned, the error is sent using `error.name`. Return `status(...)` to override the default status.

## Custom error classes

Register with `.error()` so `code` narrows the type of `error`:

```typescript
class NicheError extends Error {
	status = 418                       // status used when thrown
	constructor(message: string) { super(message) }
	toResponse() { return { message: this.message } }   // custom body
}

new Elysia()
	.error({ NICHE: NicheError })
	.onError(({ error, code, status }) => {
		if (code === 'NICHE') return status(418, 'We have no idea how you got here')
	})
	.get('/', () => { throw new NicheError('Custom error message') })
```

## throw vs return status

`throw status(418)` is caught by onError; `return status(418)` is not, it is a normal response.

## Local error

A route can pass its own `error()` hook next to `beforeHandle` to handle only its errors.

## Gotchas

- `onError` must be registered before the routes it should cover (order of code).
- Validation errors surface with code `VALIDATION`; see the validation-message skill.
- A custom 404: `throw new NotFoundError()` (imported from `elysia`) and handle `NOT_FOUND`.

## Checked

2026-11-07. Read in full: essential/life-cycle (On Error section, error codes, context, local error, `NotFoundError` example, "must be registered before the handler", and the throw-versus-return `status(418)` demo in the page's script block) and tutorial/patterns/error-handling (`.error()` registration, `status` property, `toResponse`). Every claim matched the page text; nothing removed.

Method: documentation only; no commands were run.
