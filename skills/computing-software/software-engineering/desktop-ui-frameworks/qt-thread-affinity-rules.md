---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-thread-affinity-rules
name: qt-thread-affinity-rules
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-thread-affinity-rules, qt-threads, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Respect QObject thread affinity: GUI classes only on the main thread, no cross-thread parenting."
sources:
  - https://doc.qt.io/qt-6/threads-qobject.html
  - https://doc.qt.io/qt-6/qobject.html
  - https://doc.qt.io/qt-6/qmetaobject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt thread affinity rules

**Goal:** avoid the classic Qt thread crashes.

```cpp
Q_ASSERT(QThread::currentThread() == qApp->thread());   // GUI-only code
// call into a QObject living on another thread, safely
QMetaObject::invokeMethod(worker, [=] { worker->setLimit(10); }, Qt::QueuedConnection);   // functor with a connection type: Qt 6.7+
```

**Gotcha:** QWidget and all its subclasses can only be used from the main thread, and QObject is not thread-safe (the event loop may deliver events while another thread touches the object). QObject::setParent() fails if the two objects live in different threads.

## Checked
2026-11-03. Confirmed in the Threads and QObjects, QObject and QMetaObject pages: GUI classes main thread only, QObject not thread-safe, setParent fails across threads, invokeMethod(context, functor, connectionType) since Qt 6.7. Removed: the QPixmap and QML item rules, the QImage-in-workers advice and QT_FATAL_WARNINGS (not in the pages).

Method: documentation only; no commands were run.

## Verify
- Q_ASSERT on QThread::currentThread() == qApp->thread() holds at every GUI entry point.
