---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qml-property-bindings
name: qt-qml-property-bindings
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qml-property-bindings, qt-qml, qt, qt6, qml, qt-quick, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use declarative bindings, avoid breaking them with assignments, and use Qt.binding to restore."
sources:
  - https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html
  - https://doc.qt.io/qt-6/qml-qtqml-binding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QML property bindings

**Goal:** reactive UI without manual updates.

```qml
Rectangle {
    width: parent.width / 2          // binding, re-evaluates when parent.width changes
    color: mouse.pressed ? "orange" : "steelblue"
    MouseArea { id: mouse; anchors.fill: parent
        onClicked: parent.width = 100               // BREAKS the binding
    }
    Component.onCompleted: width = Qt.binding(function() { return parent.width / 2 })  // restore
}
```

**Gotcha:** Assigning a static value to a bound property from a JavaScript statement removes the binding; wrap a new expression in Qt.binding() to re-establish a relationship, or use a Binding object.

## Checked
2026-11-03. Confirmed in the Property Binding and Binding pages: bindings re-evaluate on dependency change, static assignment from JavaScript removes the binding, Qt.binding(function) restores it, Binding type exists. Replaced: arrow-function form with the documented function form. Removed: the states recommendation (not in these pages).

Method: documentation only; no commands were run.

## Verify
- Resize the parent and confirm the child follows both before and after a click.
