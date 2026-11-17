---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qtimer-usage
name: qt-qtimer-usage
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qtimer-usage, qt-event-loop, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use QTimer repeating, singleShot and precise timers, and run work from the event loop without threads."
sources:
  - https://doc.qt.io/qt-6/eventsandfilters.html
  - https://doc.qt.io/qt-6/qtimer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QTimer patterns

**Goal:** periodic and deferred work on the event loop.

```cpp
auto* t = new QTimer(this);
t->setInterval(1000);
connect(t, &QTimer::timeout, this, &Poller::poll);
t->start();
QTimer::singleShot(0, this, &Init::lateInit);   // zero timeout: fires as soon as the event loop is free
QTimer::singleShot(std::chrono::seconds(2), this, [] { qDebug() << "2s"; });
t->setTimerType(Qt::PreciseTimer);               // CoarseTimer may fire up to 5% of the interval early
```

**Gotcha:** A QTimer works in any thread that has a running event loop and must be started and stopped in its own thread; reach that thread with a queued call or QMetaObject::invokeMethod. Keeping the event loop busy with a zero-timer causes erratic UI behaviour.

## Checked
2026-11-03. Confirmed in the QTimer and Events and Filters pages: timers need an event loop in their thread and cannot be started from another thread, zero-timeout timers, Qt::CoarseTimer 5% margin, std::chrono singleShot overloads, setInterval/start. Removed: the run-after-current-event wording.

Method: documentation only; no commands were run.

## Verify
- The timeout fires on the intended thread and stops when the owner is destroyed.
