---
id: computing-software.web-development.hono.hono-http-exception
name: hono-http-exception
category: computing-software
field: web-development
product: hono
tags: [hono, api, errors, http-exception]
level: practitioner
status: docs-checked
description: "Throw and handle HTTPException in Hono with custom messages, custom responses, cause, onError and getResponse (which ignores Context headers)."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/exception.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPException

Import: `import { HTTPException } from 'hono/http-exception'`.

## Throw
```ts
throw new HTTPException(401, { message: 'Unauthorized' })
```

Custom response (use `res` for other types or headers). The status passed to the constructor is the one used:

```ts
const errorResponse = new Response('Unauthorized', {
  status: 401, // this gets ignored
  headers: { Authenticate: 'error="invalid_token"' },
})
throw new HTTPException(401, { res: errorResponse })
```

Cause:

```ts
app.post('/login', async (c) => {
  try {
    await authorize(c)
  } catch (cause) {
    throw new HTTPException(401, { message, cause })
  }
  return c.redirect('/')
})
```

## Handle
`HTTPException.getResponse()` builds a Response from the status and either the message or your custom response:

```ts
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return err.getResponse()
  }
  console.error(err)
  return c.text('Internal Server Error', 500)
})
```

## Gotcha
`getResponse` is NOT aware of `Context`. Headers you set with `c.header()` (for example CORS headers) are not included, so apply them to a new Response yourself.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/api/exception.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
