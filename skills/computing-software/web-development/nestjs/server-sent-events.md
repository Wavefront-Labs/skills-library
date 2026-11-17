---
id: computing-software.web-development.nestjs.server-sent-events
name: server-sent-events
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, sse, rxjs, observable, streaming]
level: practitioner
status: docs-checked
description: "Stream real-time updates from NestJS with the Sse decorator, Observable MessageEvent, finalize cleanup and the SseSignal AbortSignal."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/http/server-sent-events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Annotate a controller route with `@Sse()` (from `@nestjs/common`) and return an `Observable` (or a `Promise` resolving to one):

```typescript
@Sse('sse')
sse(): Observable<MessageEvent> {
  return interval(1000).pipe(map((_) => ({ data: { hello: 'world' } })));
}
```

`MessageEvent` is `{ data?: string | object; id?: string; type?: string; retry?: number; comment?: string }`. Object `data` is serialized to JSON, `type` becomes the SSE `event` field, `comment` is a comment line (useful as a keep-alive), and Nest numbers events itself if you omit `id`.

Client: `const eventSource = new EventSource('/sse'); eventSource.onmessage = ({ data }) => console.log(JSON.parse(data));`

Status and headers: `@Header()` is honored. From v12.1.3 the status code a handler or interceptor sets before the stream starts is sent too (on Fastify, their headers as well): `sse(@Res({ passthrough: true }) res: Response)` then `res.status(202)`.

Disconnects: Nest unsubscribes from the Observable automatically. Add `finalize(() => console.log('Client disconnected'))` for custom teardown (runs on completion, error or unsubscribe).

Async setup gap: if the client leaves while a `Promise<Observable>` is still resolving, Nest never subscribes, so setup resources leak. Inject the abort signal:

```typescript
@Sse('stream')
async stream(@SseSignal() signal: AbortSignal): Promise<Observable<MessageEvent>> {
  const session = await createSession();
  if (signal.aborted) { await session.close(); return EMPTY; }
  return new Observable(subscriber => { /* ... */ return () => session.close(); });
}
```

Gotchas:
- The signal aborts on completion and errors too, so `signal.aborted` only means "client left" during setup. Make abort cleanup idempotent.
- `@SseSignal()` resolves to `undefined` on non-SSE routes.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: Sse decorator, MessageEvent fields, EventSource client, status and header behaviour, finalize, SseSignal and signal lifetime (server-sent-events page). Removed: status and header claim narrowed to the page; invented Verify step.

Method: documentation only; no commands were run.
