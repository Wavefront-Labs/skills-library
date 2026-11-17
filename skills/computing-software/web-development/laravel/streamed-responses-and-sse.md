---
id: computing-software.web-development.laravel.streamed-responses-and-sse
name: streamed-responses-and-sse
category: computing-software
field: web-development
product: laravel
tags: [laravel, responses, streaming, server-sent-events, usestream]
level: advanced
status: docs-checked
description: "Stream Laravel responses with response()->stream, streamJson and eventStream (SSE), and consume them with the @laravel/stream-* hooks."
sources:
  - https://laravel.com/docs/responses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Streaming lowers memory use and lets the client start processing early.

```php
return response()->stream(function (): void {
    foreach (['developer', 'admin'] as $string) {
        echo $string;
        ob_flush();
        flush();
        sleep(2);
    }
}, 200, ['X-Accel-Buffering' => 'no']);
```

If the closure returns a Generator, Laravel flushes between yielded strings and disables Nginx output buffering.

JSON, streamed incrementally:

```php
return response()->streamJson(['users' => User::cursor()]);
```

Server-sent events (`text/event-stream`); yield values from the closure. Yield a `StreamedEvent` to name the event, and pass `endStreamWith` to customise the final event (the default sends `</stream>` at the end):

```php
return response()->eventStream(function () {
    foreach ($stream as $response) {
        yield new Illuminate\Http\StreamedEvent(event: 'update', data: $response->choices[0]);
    }
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

Plain browser consumption:

```js
const source = new EventSource('/chat');
source.addEventListener('update', (event) => {
    if (event.data === '</stream>') { source.close(); return; }
});
```

Frontend hooks: `npm install @laravel/stream-react` (or `-vue`, `-svelte`).

```tsx
const { data, isFetching, isStreaming, send, cancel, id } = useStream("chat");
const { message } = useEventStream("/chat");
const { data: users } = useJsonStream("users"); // parses JSON when finished
```

`useStream` options: `id`, `initialInput`, `headers`, `csrfToken`, `onResponse`, `onData`, `onCancel`, `onFinish`, `onError`. `send` cancels the active connection first and sends a JSON POST, so a valid CSRF token is required (a meta tag in the layout head is the easiest). The stream ID goes to the server in the `X-STREAM-ID` header. `useEventStream` options: `eventName`, `onMessage`, `onError`, `onComplete`, `endSignal`, `glue`.

## Checked

2026-11-07

Method: read the whole responses page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed response()->stream with the X-Accel-Buffering note, generator flushing, streamJson with cursor(), eventStream and StreamedEvent, endStreamWith, EventSource usage, and the useStream, useEventStream and useJsonStream option lists. npm package names and OpenAI links were not opened or installed.
