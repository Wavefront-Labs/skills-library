---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qtconcurrent-run
name: qt-qtconcurrent-run
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qtconcurrent-run, qt-threads, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Run functions on the default thread pool with QtConcurrent::run and watch results with QFutureWatcher."
sources:
  - https://doc.qt.io/qt-6/qtconcurrentrun.html
  - https://doc.qt.io/qt-6/qfuturewatcher.html
  - https://doc.qt.io/qt-6/qtconcurrent-index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QtConcurrent run and QFuture

**Goal:** fire-and-collect parallel work.

```cpp
#include <QtConcurrent>
QFuture<QImage> f = QtConcurrent::run([path] { return QImage(path).scaled(256, 256); });
auto* w = new QFutureWatcher<QImage>(this);
connect(w, &QFutureWatcher<QImage>::finished, this, [this, w] {
    setThumb(w->result()); w->deleteLater();
});
w->setFuture(f);
// CMake: find_package(Qt6 REQUIRED COMPONENTS Concurrent)
```

**Gotcha:** QFuture::result() blocks, so use the watcher. To make a task cancellable use the Run With Promise mode: the function takes a QPromise and future.cancel() makes promise.isCanceled() true.

## Checked
2026-11-03. Confirmed in the QtConcurrent::run, QFutureWatcher and Qt Concurrent pages: runs on a thread from the default QThreadPool, QFuture/QFutureWatcher monitoring, result() blocks, cancellation through QPromise in Run With Promise mode. Replaced: the dead thread-basics.html source and the global-pool wording. Removed: the cannot-be-cancelled and atomic-flag advice.

Method: documentation only; no commands were run.

## Verify
- UI stays responsive and the result slot runs on the GUI thread.
