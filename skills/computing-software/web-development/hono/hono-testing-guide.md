---
id: computing-software.web-development.hono.hono-testing-guide
name: hono-testing-guide
category: computing-software
field: web-development
product: hono
tags: [hono, guide, testing, vitest]
level: practitioner
status: docs-checked
description: "Test Hono apps with app.request: GET, POST, JSON, FormData, Request objects and mock Env bindings, plus Vitest on Cloudflare Workers."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing with app.request

Pass a request to the app and assert on the Response; no server needed. Cloudflare recommends Vitest with `@cloudflare/vitest-pool-workers`. For a typed client see the testClient helper.

```ts
app.get('/posts', (c) => c.text('Many posts'))
app.post('/posts', (c) => c.json({ message: 'Created' }, 201, { 'X-Custom': 'Thank you' }))

describe('Example', () => {
  test('GET /posts', async () => {
    const res = await app.request('/posts')
    expect(res.status).toBe(200)
    expect(await res.text()).toBe('Many posts')
  })
})
```

## POST variants
```ts
// plain
await app.request('/posts', { method: 'POST' })

// JSON
await app.request('/posts', {
  method: 'POST',
  body: JSON.stringify({ message: 'hello hono' }),
  headers: new Headers({ 'Content-Type': 'application/json' }),
})

// multipart
const formData = new FormData()
formData.append('message', 'hello')
await app.request('/posts', { method: 'POST', body: formData })

// Request object
await app.request(new Request('http://localhost/posts', { method: 'POST' }))
```
Assert `res.status`, `res.headers.get('X-Custom')`, `await res.json()`.

## Env (bindings)
The third argument sets `c.env`:

```ts
const MOCK_ENV = {
  API_HOST: 'example.com',
  DB: { prepare: () => { /* mocked D1 */ } },
}
const res = await app.request('/posts', {}, MOCK_ENV)
```

## Gotcha
The page notes that testing this way is like an end-to-end test. Its JSON example sets the `Content-Type: application/json` header on the request.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/testing.md. Removed: the invented Verify step and the claim that validators see nothing without a Content-Type header.
Method: documentation only; no commands were run.
