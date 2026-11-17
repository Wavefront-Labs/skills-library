---
id: creative-arts.animation.scripting.qtpy-binding-agnostic-ui
name: qtpy-binding-agnostic-ui
category: creative-arts
field: animation
product: scripting
tags: [qt-py, pipeline-python, dcc-python, pyside2, pyside6, qtpy, maya-ui, nuke-ui, houdini-ui, parent-window]
level: advanced
status: draft
description: "Write one Qt tool UI that runs in Maya, Nuke, Houdini and Blender across PySide2/PySide6 using Qt.py, with correct parenting to the host main window."
sources:
  - https://github.com/mottosso/Qt.py
  - https://doc.qt.io/qtforpython-6/
  - https://help.autodesk.com/view/MAYAUL/2025/ENU/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Binding-agnostic Qt UIs with Qt.py

**Goal:** a pipeline tool UI written once that works in every DCC version the studio uses, even though
Maya 2024 ships PySide2 and Maya 2025+/Nuke 16/Houdini 20.5 ship PySide6.

## Qt.py

`Qt.py` (single file, by Marcus Ottosson) exposes the PySide2 API names and maps them onto whichever
binding is available (PySide6, PySide2, PyQt5).
```python
from Qt import QtWidgets, QtCore, QtGui, QtCompat

class Publisher(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Publish")
        lay = QtWidgets.QVBoxLayout(self)
        self.comment = QtWidgets.QLineEdit(placeholderText="Comment")
        btn = QtWidgets.QPushButton("Publish")
        btn.clicked.connect(self.publish)
        lay.addWidget(self.comment); lay.addWidget(btn)
    def publish(self):
        print("publishing:", self.comment.text())
```
(`qtpy` from Spyder is an alternative with similar goals; pick one studio-wide.)

## Parenting to the host

A tool without a parent falls behind the DCC window or gets garbage-collected.
```python
def host_main_window():
    try:                                       # Maya
        from maya import OpenMayaUI as omui
        ptr = omui.MQtUtil.mainWindow()
        return QtCompat.wrapInstance(int(ptr), QtWidgets.QWidget)
    except ImportError:
        pass
    try:                                       # Houdini
        import hou; return hou.qt.mainWindow()
    except ImportError:
        pass
    app = QtWidgets.QApplication.instance()    # Nuke and others: find the top-level main window
    return next((w for w in app.topLevelWidgets() if isinstance(w, QtWidgets.QMainWindow)), None)

_win = Publisher(host_main_window()); _win.show()      # keep a module-level reference
```

## PySide6 differences to watch

- `exec_()` is `exec()` in PySide6 (Qt.py keeps `exec_`).
- Enums are fully scoped in PySide6 (`QtCore.Qt.AlignmentFlag.AlignLeft`); Qt.py handles many but not all.
- `QAction` moved from QtWidgets to QtGui in Qt6.
- `QtCompat.loadUi` for Designer `.ui` files across bindings.

## Blender

Blender has no Qt; run Qt tools with their own `QApplication` in a separate process or use Blender's
UI API for in-app panels.

## Verify

Launch the tool in two DCCs with different bindings (e.g. Maya 2024 and Maya 2025): it opens on top of
the main window, stays open, and buttons work.
