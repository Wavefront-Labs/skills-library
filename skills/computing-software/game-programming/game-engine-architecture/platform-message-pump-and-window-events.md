---
id: computing-software.game-programming.game-engine-architecture.platform-message-pump-and-window-events
name: platform-message-pump-and-window-events
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, message-pump, window-events, game-loop, game-programming]
level: practitioner
status: docs-checked
description: "Integrate the OS message pump with the game loop: Win32 GetMessage versus PeekMessage, WM_QUIT, SDL_PollEvent once per frame, thread rules and the drag-resize stall."
sources: ["https://learn.microsoft.com/en-us/windows/win32/winmsg/using-messages-and-message-queues", "https://wiki.libsdl.org/SDL3/SDL_PollEvent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform message pump and window events

**Goal:** process OS window events every frame without blocking the game loop.

## Win32 (Using Messages and Message Queues)
- The system creates a message queue only for threads that need one. A thread that creates a window
  must run a message loop that retrieves messages and dispatches them to window procedures; most
  applications create windows on a single thread.
- The standard loop uses `GetMessage` plus `DispatchMessage`, with `TranslateMessage` when you need
  character input (it turns virtual-key messages into character messages).
- `GetMessage` does not return until a matching message is queued. `PeekMessage` returns
  immediately whether or not a message is waiting, so a game that must keep ticking drains the
  queue with it instead:
```cpp
bool running = true;
while (running) {
    MSG msg;
    while (PeekMessage(&msg, nullptr, 0, 0, PM_REMOVE)) {  // returns at once; PM_REMOVE removes it
        if (msg.message == WM_QUIT) running = false;
        TranslateMessage(&msg); DispatchMessage(&msg);
    }
    tick();
}
```
- `DispatchMessage` does not return until the window procedure finishes the message, so a long
  operation inside a window procedure stalls input and your loop; the page recommends examining the
  queue with `PeekMessage` during lengthy work.
- `PostQuitMessage` posts `WM_QUIT` to the calling thread and ends its loop; applications usually
  call it from the `WM_DESTROY` handler.
- `GetQueueStatus` is the fastest way to see whether the queue holds messages; `GetInputState`
  reports pending mouse or keyboard messages.
- `PostMessage` queues to a window's thread and returns at once; `PostThreadMessage` targets a
  thread id. A window procedure that may receive cross-thread sent messages should check
  `InSendMessage` and call `ReplyMessage` before yielding.

## SDL3 (SDL_PollEvent)
```c
while (game_is_still_running) {
    SDL_Event event;
    while (SDL_PollEvent(&event)) {   // poll until all events are handled
        // decide what to do with this event
    }
    // update game state, draw the current frame
}
```
- `SDL_PollEvent` returns true if an event was removed from the queue into `event`, false if none.
  With a NULL event it only reports whether one is pending. It does not suspend the main loop.
- Common practice is to fully process the queue once per frame, first, before updating state.
- It may implicitly call `SDL_PumpEvents()`, so call it only on the thread that initialised the
  video subsystem (the page's thread-safety note says the main thread). Available since SDL 3.2.0.
- Quirk: on Windows (and possibly other platforms) events during window drag or resize can make
  the call block for a long time; the SDL wiki page `AppFreezeDuringDrag` covers causes and fixes.
- Related: `SDL_PushEvent`, `SDL_WaitEvent`, `SDL_WaitEventTimeout`.

## Verify
- Drag and resize the window continuously: confirm whether the game keeps updating or pauses
  deliberately.
- Events are consumed once per frame from the thread that created the window.

## Checked

Date 2026-11-08. Pages read in full: Microsoft "Using Messages and Message Queues" (message loop, PeekMessage, PostQuitMessage, queue-status sections) and SDL_PollEvent (SDL wiki). Confirmed: everything above. Removed as not on those pages: the WM_SIZE, WM_ACTIVATEAPP, WM_KILLFOCUS, WM_INPUT, WM_DPICHANGED and WM_CLOSE handling advice, SDL event type names and `e.window.data1`, the WM_ENTERSIZEMOVE/WM_TIMER workaround, macOS main-thread rule, minimised-window and exclusive-fullscreen notes, and the per-frame input buffer advice.

Method: docs-only read of cited pages, 2026-11-08
