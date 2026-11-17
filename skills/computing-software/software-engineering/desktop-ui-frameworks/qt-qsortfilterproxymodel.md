---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qsortfilterproxymodel
name: qt-qsortfilterproxymodel
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qsortfilterproxymodel, qt-model-view, qt, qt6, c++, model-view, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Sort and filter a source model without copying it using QSortFilterProxyModel."
sources:
  - https://doc.qt.io/qt-6/model-view-programming.html
  - https://doc.qt.io/qt-6/qsortfilterproxymodel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QSortFilterProxyModel

**Goal:** searchable sorted views.

```cpp
auto* proxy = new QSortFilterProxyModel(this);
proxy->setSourceModel(model);
proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
proxy->setFilterKeyColumn(-1);          // all columns
proxy->setDynamicSortFilter(true);
view->setModel(proxy);
connect(edit, &QLineEdit::textChanged, proxy, &QSortFilterProxyModel::setFilterFixedString);
view->sortByColumn(0, Qt::AscendingOrder);
```

**Gotcha:** Indexes from the view belong to the proxy; use proxy->mapToSource() before touching the source model.

## Checked
2026-11-03. Confirmed in the QSortFilterProxyModel page: setSourceModel, setFilterCaseSensitivity, setFilterKeyColumn, setDynamicSortFilter, setFilterFixedString, mapToSource.

Method: documentation only; no commands were run.

## Verify
- Typing in the search box filters rows; the selected row maps to the right source item.
