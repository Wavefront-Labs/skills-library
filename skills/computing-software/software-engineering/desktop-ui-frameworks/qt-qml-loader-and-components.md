---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qml-loader-and-components
name: qt-qml-loader-and-components
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qml-loader-and-components, qt-qml, qt, qt6, qml, qt-quick, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Load QML lazily with Loader, Component and createObject, and manage object lifetime."
sources:
  - https://doc.qt.io/qt-6/qml-qtquick-loader.html
  - https://doc.qt.io/qt-6/qtqml-javascript-dynamicobjectcreation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QML Loader and dynamic components

**Goal:** lazy UI and dynamic creation.

```qml
Loader {
    id: pageLoader
    active: tabs.current === 2          // while inactive, no item is instantiated
    source: "Settings.qml"
    onLoaded: item.title = "Settings"
}
Component { id: dot; Rectangle { width: 8; height: 8; radius: 4 } }
function addDot() { dot.createObject(container, {x: 10, y: 10}) }
```

**Gotcha:** createObject(parent, properties) takes a parent (null is allowed if you set it later; only visual objects with a visual parent are drawn). Free dynamically created objects with destroy(), which cleans up between the end of the script block and the next frame unless you pass a delay; the creation context must outlive the object.

## Checked
2026-11-03. Confirmed in the Loader and Dynamic QML Object Creation pages: active, source, onLoaded, unloading when source changes or is emptied, createObject(parent, properties), destroy() with optional delay, null parent allowed. Removed: the claim that a null-parent object is not cleaned up with the page.

Method: documentation only; no commands were run.

## Verify
- Setting source to an empty string unloads the loaded item.
