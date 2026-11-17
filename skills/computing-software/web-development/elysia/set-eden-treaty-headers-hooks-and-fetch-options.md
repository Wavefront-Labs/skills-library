---
id: computing-software.web-development.elysia.set-eden-treaty-headers-hooks-and-fetch-options
name: set-eden-treaty-headers-hooks-and-fetch-options
category: computing-software
field: web-development
product: elysia
tags: [elysia, eden-treaty-config, headers, onrequest, onresponse, throwhttperror]
level: advanced
status: docs-checked
description: "Configure Eden Treaty with a URL or instance and the options fetch, fetcher, headers, onRequest, onResponse, parseDate and throwHttpError, including priority rules."
sources:
  - https://elysiajs.com/eden/treaty/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: set default headers, intercept requests/responses and control error behaviour of a Treaty client.

`treaty<App>(urlOrInstance, options?)`.

## urlOrInstance

- String URL: uses `fetch` (or `config.fetcher`). Protocol resolution: explicit protocol is used as given; `localhost` outside production uses http; otherwise https. Same logic picks `ws://` vs `wss://`.
- Elysia instance: Treaty builds a `Request` and calls `Elysia.handle` directly, no network and no server needed; no generic required (`treaty(app)`). Recommended for unit tests and type-safe reverse proxies or microservices.

## Options

- `fetch`: default `RequestInit`, e.g. `{ fetch: { credentials: 'include' } }`.
- `fetcher`: replace fetch (Axios, unfetch...): `fetcher(url, options) { return fetch(url, options) }`.
- `headers`: object, function, or array of functions. `headers(path, options)` receives the path without hostname (`/user/griseo`) and RequestInit; return an object to add headers. An array runs all functions even after one has returned.
- `onRequest(path, options)`: return an object to merge into RequestInit (shallow merge with `headers`). Arrays run all functions.
- `onResponse(response)`: receives the Web Standard Response; return a value (e.g. `response.json()`) to use as the new response. For arrays, Treaty loops until a function returns a value or an error is thrown.
- `parseDate`: default `true`, converts date strings to `Date`.
- `throwHttpError`: default `false`. When true, Treaty throws if status is not 2xx; otherwise you get `{ error }`. A function form, `throwHttpError: (response) => response.status === 418`, throws only when it returns true.

## Header priority

1. Inline method headers (`api.profile.get({ headers: {...} })`)
2. `config.headers` (later array entries win)
3. `config.fetch.headers`

With config `Bearer Aponia` and inline `Bearer Griseo`, Griseo is sent; without the inline headers, Aponia.

## Gotchas

- Don't confuse the two merge behaviours: headers and onRequest arrays run every function; onResponse stops at the first value.
- `onResponse` takes only the `response` argument (no path or options).

## Checked

2026-11-07. Read in full: eden/treaty/config. Confirmed protocol resolution (explicit, localhost outside production is http, else https; same for ws/wss), instance mode via `Elysia.handle`, `fetch`, `fetcher`, `headers` (object, function, array; path without hostname; arrays run every function), `onRequest` (shallow merge, arrays run every function), `onResponse` (one argument; arrays stop at the first returned value), `parseDate` default `true`, `throwHttpError` default `false` with the function form, and the header priority order with the Aponia and Griseo example. Nothing removed.

Method: documentation only; no commands were run.
