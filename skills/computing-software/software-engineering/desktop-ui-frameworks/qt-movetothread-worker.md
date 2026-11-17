---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-movetothread-worker
name: qt-movetothread-worker
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-movetothread-worker, qt-threads, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Run work in a QObject worker moved to a QThread instead of subclassing QThread."
sources:
  - https://doc.qt.io/qt-6/threads-qobject.html
  - https://doc.qt.io/qt-6/qthread.html
  - https://doc.qt.io/qt-6/qobject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt worker object with moveToThread

**Goal:** background work with clean signal-based results.

```cpp
auto* thread = new QThread(this);
auto* worker = new Worker;               // no parent
worker->moveToThread(thread);
connect(thread, &QThread::started,  worker, &Worker::run);
connect(worker, &Worker::done,      this,   &Ui::onDone);
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
thread->start();
// shutdown
thread->quit(); thread->wait();
```

**Gotcha:** A QObject with a parent cannot be moved to another thread, and worker slots run in the worker thread only when the connection is queued (the default across threads).

## Checked
2026-11-03. Confirmed in the Threads and QObjects, QThread and QObject pages: moveToThread fails when the object has a parent, finished connected to deleteLater, the AutoConnection rule (queued across threads). Replaced: the dead thread-basics.html source.

Method: documentation only; no commands were run.

## Verify
- Worker slot logs a thread id different from the GUI thread; quit()/wait() returns on exit.
