---
id: computing-software.software-engineering.java.watchservice-directory-events
name: watchservice-directory-events
category: computing-software
field: software-engineering
product: java
tags: [java, java-io-nio, watchservice, file-watcher, inotify, directory-events, debounce, hot-reload]
level: practitioner
status: docs-checked
description: "React to file changes with java.nio.file.WatchService: register directories, drain keys, reset, handle OVERFLOW, debounce duplicate events, and know platform limits."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/WatchService.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/WatchKey.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/WatchEvent.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/StandardWatchEventKinds.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WatchService: directory events

## Loop
```java
try (WatchService ws = FileSystems.getDefault().newWatchService()) {
    dir.register(ws, StandardWatchEventKinds.ENTRY_CREATE,
                     StandardWatchEventKinds.ENTRY_MODIFY,
                     StandardWatchEventKinds.ENTRY_DELETE);
    while (true) {
        WatchKey key = ws.take();                       // blocks; poll(timeout) for shutdown checks
        for (WatchEvent<?> ev : key.pollEvents()) {
            if (ev.kind() == StandardWatchEventKinds.OVERFLOW) { rescan(); continue; }
            Path changed = ((Path) key.watchable()).resolve((Path) ev.context());
            handle(ev.kind(), changed);
        }
        if (!key.reset()) break;                        // directory gone or watch cancelled
    }
}
```
Always call `key.reset()` after processing: it lets the key be signalled and queued again, and its return value tells you whether the key is still valid (a key is cancelled automatically if the watched directory is deleted).

## Practical rules
1. `ENTRY_CREATE`, `ENTRY_MODIFY` and `ENTRY_DELETE` are reported for entries of the registered directory. Register each subdirectory you care about yourself, and register new ones on `ENTRY_CREATE` (`Files.walkFileTree` to seed).
2. A modification may produce one event in some implementations and several in others; debounce by collecting paths for a short quiet period before acting.
3. `OVERFLOW` means events were knowingly discarded; use it as the trigger to re-examine the directory (full rescan).
4. An event for a modified file does not mean the writer has finished. Coordinate access, wait for a quiet period, or have writers rename a finished temp file into place.
5. Run the loop on its own thread. Closing the service makes threads blocked in `take()` or `poll()` throw `ClosedWatchServiceException`; the service is safe for multiple consumers, but call `reset()` only after a key's events are processed.

## Platform behaviour
The implementation maps onto the native file-event facility where one exists, and otherwise uses a primitive mechanism such as polling, so timeliness, event counts and ordering are implementation specific. Short-lived files may be missed by polling implementations. For files on non-local storage it is implementation specific whether changes are detected; remote changes are not required to be reported.

## Gotchas
- `ev.context()` is the path relative to the registered directory; resolve it against `key.watchable()`.

## Verify
In a test using a temporary directory, create a file, poll with a 5-second timeout, and assert the event kind and resolved path; test a rename-save sequence separately.

## Checked
2026-11-03. Confirmed against the Java SE 21 API pages for WatchService, WatchKey, WatchEvent and StandardWatchEventKinds: take/poll/close and ClosedWatchServiceException, reset and key validity, OVERFLOW, context() as a relative path, platform dependencies (native facility or polling, non-local storage), and that modification events do not imply the writer is finished.
Removed (not confirmed in the pages read): inotify limit name, Windows and macOS implementation details, SensitivityWatchEventModifier, the 100-300 ms debounce figure, editor save-by-rename behaviour, and the exact exception types thrown on registering a missing path.
Method: documentation only; no commands were run.
