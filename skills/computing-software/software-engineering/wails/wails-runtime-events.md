---
id: computing-software.software-engineering.wails.wails-runtime-events
name: wails-runtime-events
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, events, javascript]
level: practitioner
status: docs-checked
description: "Emit and listen to events between Go and JavaScript in Wails with EventsOn, EventsOnce, EventsOnMultiple, EventsOff, EventsOffAll and EventsEmit."
sources: [https://wails.io/docs/reference/runtime/events]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime events

Goal: send named events with optional data in either direction between Go and JS. Listeners receive data in local types.

## Calls

- `EventsOn(ctx, eventName, callback func(optionalData ...interface{})) func()` / JS `EventsOn(eventName, callback(optionalData?)): () => void`. Returns a function that cancels the listener.
- `EventsOnce(...)`: same signature, fires once.
- `EventsOnMultiple(ctx, eventName, callback, counter int)` / JS `EventsOnMultiple(eventName, callback, counter)`: fires at most `counter` times.
- `EventsOff(ctx, eventName, additionalEventNames ...string)` / JS `EventsOff(eventName, ...additionalEventNames)`: unregisters listeners for one or several event names.
- `EventsOffAll(ctx)` / JS `EventsOffAll()`: unregisters every listener.
- `EventsEmit(ctx, eventName, optionalData ...interface{})` / JS `EventsEmit(eventName, ...optionalData)`: triggers listeners.

## Example (docs)

Frontend (React):

```tsx
import { EventsOn, EventsOff } from "../wailsjs/runtime/runtime";

useEffect(() => {
  const handler = (event: any) => { console.log(event); };
  EventsOn("auth:success", handler);
  return () => { EventsOff("auth:success"); };
}, [])
```

Go:

```go
import "github.com/wailsapp/wails/v2/pkg/runtime"

func (a *App) Auth() {
    runtime.EventsEmit(a.ctx, "auth:success", "user-123")
}
```

Use the returned cancel function or `EventsOff` when a component unmounts.

Related: `computing-software.software-engineering.wails.wails-file-drop` (the `wails:file-drop` event) and `computing-software.software-engineering.wails.wails-runtime-notifications` (forwarding notification responses to JS).

## Checked

2026-11-07. Read the whole Events runtime page (website/docs/reference/runtime/events.mdx: EventsOn, EventsOff, EventsOffAll, EventsOnce, EventsOnMultiple, EventsEmit with Go and JS signatures, and the React/Go code sample). The Go and JS signatures, the cancel-function return values and the counter semantics matched. No claims were trimmed.

Method: documentation only; no commands were run.
