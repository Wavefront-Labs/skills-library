---
id: computing-software.web-development.elysia.measure-lifecycle-timings-with-trace
name: measure-lifecycle-timings-with-trace
category: computing-software
field: web-development
product: elysia
tags: [trace, lifecycle, performance, on-stop, children, aot]
level: advanced
status: docs-checked
description: "Use Elysia .trace() to time each lifecycle event and its child hooks, read begin/end/elapsed, and write elapsed time into response headers."
sources:
  - https://elysiajs.com/patterns/trace.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: find which lifecycle event or hook is slow by instrumenting it with `trace`.

## Basic use

`trace` injects start/stop code around each lifecycle event. Listen with `on` + event name (`onHandle`, `onBeforeHandle`, ...). The callback must finish before the next event runs.

```ts
new Elysia()
  .trace(async ({ onHandle }) => {
    onHandle(({ begin, onStop }) => {
      onStop(({ end }) => console.log('handle took', end - begin, 'ms'))
    })
  })
  .get('/', () => 'Hi')
```

Events you can listen to: `onRequest`, `onParse`, `onTransform`, `onBeforeHandle`, `onHandle`, `onAfterHandle`, `onMapResponse`, `onError`, `onAfterResponse`.

## Child hooks

Every event except `handle` has children (the hooks registered for it). `total` is the child count and `onEvent` visits each child in order:

```ts
.trace(async ({ onBeforeHandle }) => {
  onBeforeHandle(({ total, onEvent }) => {
    console.log('total children:', total)
    onEvent(({ onStop }) => onStop(({ elapsed }) => console.log('child took', elapsed, 'ms')))
  })
})
.get('/', () => 'Hi', { beforeHandle: [function setup() {}, async function delay() { await sleep() }] })
```

With two `beforeHandle` functions, `total` is 2.

## Parameters

- trace parameter: `id` (random per request), `context`, `set`, `store`, `time`, and the `on[Event]` listeners.
- listener parameter: `name` (function name, or `anonymous`), `begin`, `end` (Promise of number), `error` (Promise of Error or null), `onStop(callback)`.
- `onStop` detail (`TraceEndDetail`): `end`, `error`, `elapsed` (= end - begin).

## Put elapsed time in a header

```ts
.trace(({ onBeforeHandle, set }) => {
  onBeforeHandle(({ onStop }) => onStop(({ elapsed }) => { set.headers['X-Elapsed'] = elapsed.toString() }))
})
```

Mutate context inside `onStop`: a lock ensures the mutation finishes before the next lifecycle event.

## Gotchas

- Trace does not work with `aot: false`; it needs functions to be static and known at compile time.
- Name your hook functions; anonymous ones all report `anonymous`.

## Checked

2026-11-07. Read in full: patterns/trace. Confirmed the `aot: false` warning, `on` + event listeners and the nine listed events, `begin`/`end`/`onStop` usage, children and `total` (2 for the two `beforeHandle` functions), the trace parameters (`id`, `context`, `set`, `store`, `time`), listener parameters (`name`, `begin`, `end`, `error`, `onStop`), `TraceEndDetail` (`end`, `error`, `elapsed`), the `X-Elapsed` header example and the context lock. Nothing removed.

Method: documentation only; no commands were run.
