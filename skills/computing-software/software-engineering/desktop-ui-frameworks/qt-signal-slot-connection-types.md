---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-signal-slot-connection-types
name: qt-signal-slot-connection-types
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-signal-slot-connection-types, qt-signals-slots, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Choose Qt::AutoConnection, DirectConnection, QueuedConnection or UniqueConnection correctly across threads."
sources:
  - https://doc.qt.io/qt-6/signalsandslots.html
  - https://doc.qt.io/qt-6/qt.html
  - https://doc.qt.io/qt-6/qobject.html
  - https://doc.qt.io/qt-6/qmetatype.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt connection types

**Goal:** slots run on the right thread with the right ordering.

```cpp
connect(worker, &Worker::result, ui, &Ui::show);                  // Auto: queued if threads differ
connect(a, &A::tick, b, &B::onTick, Qt::DirectConnection);        // runs in emitter's thread
connect(a, &A::tick, b, &B::onTick, Qt::QueuedConnection);        // posted to receiver's event loop
connect(a, &A::tick, b, &B::onTick, Qt::UniqueConnection);        // fails if already connected (member functions only)
// only string-based (SIGNAL/SLOT) connections need a custom type registered by name
qRegisterMetaType<MyStruct>("MyStruct");
```

**Gotcha:** DirectConnection to a receiver living in another thread runs the slot in the emitter thread and races with that object's own data; BlockingQueuedConnection deadlocks if both objects share a thread.

## Checked
2026-11-03. Confirmed in the Qt namespace (ConnectionType), Signals and Slots, QObject and QMetaType pages: Auto/Direct/Queued/BlockingQueued semantics, UniqueConnection fails for duplicates and does not work for lambdas, registration is needed only for string-form type lookup such as old-style connect. Fixed: removed the (confirm) claim that queued connections always need qRegisterMetaType.

Method: documentation only; no commands were run.

## Verify
- Log QThread::currentThread() in the slot and confirm it is the receiver's thread for queued connections.
