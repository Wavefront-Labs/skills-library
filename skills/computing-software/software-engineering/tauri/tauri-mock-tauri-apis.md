---
id: computing-software.software-engineering.tauri.tauri-mock-tauri-apis
name: tauri-mock-tauri-apis
category: computing-software
field: software-engineering
product: tauri
tags: [mocking-apis, tauri, testing, vitest]
level: practitioner
status: docs-checked
description: "Mock Tauri IPC commands, events and windows in frontend tests with mockIPC, mockWindows and clearMocks from @tauri-apps/api/mocks."
sources:
  - "https://v2.tauri.app/develop/tests/mocking/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mock Tauri APIs in frontend tests

Goal: simulate a Tauri environment (IPC, events, windows) with `@tauri-apps/api/mocks`. Examples use Vitest; any frontend test library such as jest works. Always clear mocks after each test with `clearMocks()`.

jsdom has no WebCrypto, so define `window.crypto.getRandomValues` in `beforeAll` using `randomFillSync` from `crypto`.

## IPC commands

`mockIPC` intercepts `invoke` calls:

```javascript
mockIPC((cmd, args) => {
  if (cmd === "add") {
    return (args.a as number) + (args.b as number);
  }
});
```

To count calls, spy on the internals: `vi.spyOn(window.__TAURI_INTERNALS__, "invoke")`, then `expect(invoke("add", { a: 12, b: 15 })).resolves.toBe(27)` and `expect(spy).toHaveBeenCalled()`.

## Sidecar or shell commands

When `spawn()` or `execute()` is called, grab the event-handler ID and emit what the backend would send:

```javascript
mockIPC(async (cmd, args) => {
  if (args.message.cmd === 'execute') {
    const eventEmitter = window[`_${args.message.onEventFn}`];
    eventEmitter({ event: 'Stdout', payload: 'some data sent from the process' });
    eventEmitter({ event: 'Terminated', payload: { code: 0, signal: 'kill' } });
  }
});
```

`Stdout` may fire many times; `Terminated` must be called at the end to resolve the promise.

## Events (since 2.7.0)

Pass `{ shouldMockEvents: true }` as the second argument: `mockIPC(() => {}, { shouldMockEvents: true })`. Then `listen` and `emit` from `@tauri-apps/api/event` work in the test. `emitTo` and `emit_filter` are not supported yet.

## Windows

`mockWindows('main', 'second', 'third')`: the first label is the current window, the rest are additional windows. Then `getCurrent()` and `getAll()` from `@tauri-apps/api/webviewWindow` reflect them. It fakes only the existence of windows, not their properties; intercept those calls with `mockIPC()`.

## Scope

`mockIPC` fakes `invoke` under the mock runtime; no real webview or Rust backend runs. For end-to-end tests, `@wdio/tauri-service` offers `browser.tauri.mock()`.

## Checked

Checked 2026-11-08 against the Tauri v2 mocking page: mockIPC, the jsdom crypto workaround, spying on invoke, sidecar and shell event mocking, shouldMockEvents since 2.7.0 and its limits, mockWindows and the mock runtime note. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
