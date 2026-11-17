---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-connect-syntax
name: qt-connect-syntax
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-connect-syntax, qt-signals-slots, qt, qt6, c++, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use the compile-time checked pointer-to-member connect syntax in Qt 6 and fall back to string-based connect only when needed."
sources:
  - https://doc.qt.io/qt-6/signalsandslots.html
  - https://doc.qt.io/qt-6/qobject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt connect syntax

**Goal:** type-checked signal/slot wiring that fails at compile time, not at runtime.

```cpp
connect(button, &QPushButton::clicked, this, &MainWindow::onSave);
// overloaded signal: pick the overload explicitly
connect(completer, qOverload<const QString &>(&QCompleter::activated), this, &MainWindow::onPick);
// signal to signal
connect(src, &Source::changed, this, &Sink::dataChanged);
// disconnect via the handle returned by connect()
QObject::disconnect(conn);
```

**Gotcha:** When a signal or slot is overloaded, name the version with qOverload or static_cast (QCompleter::activated is overloaded). The SIGNAL()/SLOT() macros are the older string-based form.

## Checked
2026-11-03. Confirmed in the Signals and Slots and QObject pages: pointer-to-member connect is checked at compile time, qOverload for overloaded signals (the page uses QCompleter::activated), SIGNAL()/SLOT() string macros exist, the disconnect handle. Removed: the QSpinBox::valueChanged example (not in the pages; it is no longer overloaded in Qt 6 as far as I know, so it was dropped) and the debug-console claim.

Method: documentation only; no commands were run.

## Verify
- Build with no QObject::connect warnings in the console; renaming the slot breaks the build.
