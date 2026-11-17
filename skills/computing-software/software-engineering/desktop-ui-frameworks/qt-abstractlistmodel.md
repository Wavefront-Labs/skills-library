---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-abstractlistmodel
name: qt-abstractlistmodel
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-abstractlistmodel, qt-model-view, qt, qt6, c++, model-view, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Implement a QAbstractListModel with roleNames, data and correct begin/end notifications."
sources:
  - https://doc.qt.io/qt-6/model-view-programming.html
  - https://doc.qt.io/qt-6/qabstractlistmodel.html
  - https://doc.qt.io/qt-6/qabstractitemmodel.html
  - https://doc.qt.io/qt-6/qabstractitemmodeltester.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QAbstractListModel subclass

**Goal:** a model that works in both QListView and QML ListView.

```cpp
int rowCount(const QModelIndex& p = {}) const override { return p.isValid() ? 0 : m_items.size(); }
QVariant data(const QModelIndex& i, int role) const override {
    if (!i.isValid()) return {};
    return role == NameRole ? m_items[i.row()].name : QVariant();
}
QHash<int, QByteArray> roleNames() const override { return {{NameRole, "name"}}; }
void add(Item it) {
    beginInsertRows({}, m_items.size(), m_items.size());
    m_items.append(it);
    endInsertRows();
}
```

**Gotcha:** Changing the backing store without beginInsertRows/endInsertRows (or dataChanged) does not notify the views; in a flat list model no index has a valid parent, so return 0 rows for a valid parent. QML needs roleNames() overridden for custom roles.

## Checked
2026-11-03. Confirmed in the QAbstractListModel, QAbstractItemModel and QAbstractItemModelTester pages: roleNames() must be overridden for QML roles, insertions are wrapped in beginInsertRows()/endInsertRows(), flat models have no valid parent index, the tester class exists. Removed: the unsupported claim that stale views or crashes follow.

Method: documentation only; no commands were run.

## Verify
- Run Qt's QAbstractItemModelTester against the model in a unit test.
