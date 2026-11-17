---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-layout-managers
name: qt-layout-managers
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-layout-managers, qt-widgets-basics, qt, qt6, qt-widgets, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Compose responsive widget UIs with QGridLayout, QVBoxLayout and size policies instead of fixed geometry."
sources:
  - https://doc.qt.io/qt-6/layout.html
  - https://doc.qt.io/qt-6/qgridlayout.html
  - https://doc.qt.io/qt-6/qsizepolicy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt layout managers

**Goal:** UIs that resize and survive DPI and font changes.

```cpp
auto* grid = new QGridLayout;
grid->addWidget(new QLabel(tr("Name")), 0, 0);
grid->addWidget(nameEdit, 0, 1);
grid->setColumnStretch(1, 1);
nameEdit->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
grid->addItem(new QSpacerItem(0, 0, QSizePolicy::Minimum, QSizePolicy::Expanding), 1, 0);
central->setLayout(grid);
```

**Gotcha:** Layouts take over geometry management of their widgets and resize them when space changes, so describe the UI with size policy and stretch factors instead of fixed positions; widgets with a zero stretch get extra space only if no other widget wants it, Expanding policies first.

## Checked
2026-11-03. Confirmed in the Layout Management, QGridLayout and QSizePolicy pages: layouts manage geometry and resize automatically, stretch-factor and Expanding rules, QSizePolicy::Expanding/Fixed/Minimum, addItem. Removed: the move()/resize() override claim and the QSettings source (unrelated). Fixed: setLayout(grid) after constructing the grid with a parent replaced by a parentless grid installed with setLayout.

Method: documentation only; no commands were run.

## Verify
- Resize and change the system font size: nothing clips or overlaps.
