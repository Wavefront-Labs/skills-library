---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qml-register-cpp-types
name: qt-qml-register-cpp-types
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qml-register-cpp-types, qt-qml, qt, qt6, qml, qt-quick, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Expose C++ types and singletons to QML using QML_ELEMENT and the qt_add_qml_module CMake call."
sources:
  - https://doc.qt.io/qt-6/qtqml-cppintegration-definetypes.html
  - https://doc.qt.io/qt-6/qtqml-cppintegration-exposecppattributes.html
  - https://doc.qt.io/qt-6/qt-add-qml-module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Expose C++ to QML with QML_ELEMENT

**Goal:** C++ backend usable declaratively.

```cpp
class Counter : public QObject {
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged FINAL)
public:  int value() const { return m_v; }
    void setValue(int v) { if (m_v != v) { m_v = v; emit valueChanged(); } }
signals: void valueChanged();
private: int m_v = 0;
};
// CMake: qt_add_qml_module(app URI Demo VERSION 1.0 QML_FILES Main.qml SOURCES counter.h counter.cpp)
// QML: import Demo; Counter { id: c }
```

**Gotcha:** A writable property without a NOTIFY signal is read once and never updates in a binding (and binding to it gives a runtime warning); the module URI passed to qt_add_qml_module is the name used in the QML import.

## Checked
2026-11-03. Confirmed in the Defining QML Types from C++, Exposing Attributes of C++ Classes and qt_add_qml_module pages: QML_ELEMENT, Q_PROPERTY with NOTIFY and FINAL, QML_SINGLETON, URI used in the import statement, behaviour without NOTIFY. Removed: nothing beyond rewording the gotcha.

Method: documentation only; no commands were run.

## Verify
- qmllint passes and the QML text updates when value changes.
