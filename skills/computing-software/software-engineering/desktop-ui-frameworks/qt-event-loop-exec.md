---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-event-loop-exec
name: qt-event-loop-exec
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-event-loop-exec, qt-event-loop, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Understand QCoreApplication::exec, nested loops and why processEvents is a last resort."
sources:
  - https://doc.qt.io/qt-6/eventsandfilters.html
  - https://doc.qt.io/qt-6/qtimer.html
  - https://doc.qt.io/qt-6/qeventloop.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt event loop and processEvents

**Goal:** keep the GUI responsive without re-entrancy bugs.

```cpp
int main(int argc, char** argv) {
    QApplication app(argc, argv);
    MainWindow w; w.show();
    return app.exec();          // the main event loop
}
// local loop waiting for a signal (prefer an async design instead)
QEventLoop loop;
QTimer timer; timer.setSingleShot(true);
connect(&timer, &QTimer::timeout, &loop, &QEventLoop::quit);
timer.start(1000);
loop.exec();
```

**Gotcha:** Calling QApplication::processEvents() or running a nested QEventLoop processes user input unless you pass QEventLoop::ExcludeUserInputEvents, so a handler can be re-entered while half finished; guard with a flag or restructure into async steps. For idle work the docs suggest a zero-timeout timer instead.

## Checked
2026-11-03. Confirmed in the Events and Filters, QEventLoop and QTimer pages: exec() starts a (local) event loop and quit/exit end it, processEvents() flags including ExcludeUserInputEvents, zero-timeout timers for idle processing. Replaced: the QNetworkReply example (not in the pages) with a QTimer example.

Method: documentation only; no commands were run.

## Verify
- Click a button twice quickly during a long operation; the handler must not re-enter.
