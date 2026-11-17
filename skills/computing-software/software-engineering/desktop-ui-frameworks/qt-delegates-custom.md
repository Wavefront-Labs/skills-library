---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-delegates-custom
name: qt-delegates-custom
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-delegates-custom, qt-model-view, qt, qt6, c++, model-view, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Paint and edit cells with QStyledItemDelegate paint, sizeHint and createEditor."
sources:
  - https://doc.qt.io/qt-6/model-view-programming.html
  - https://doc.qt.io/qt-6/qstyleditemdelegate.html
  - https://doc.qt.io/qt-6/qabstractitemview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom item delegates

**Goal:** custom cell rendering and editing.

```cpp
void RatingDelegate::paint(QPainter* p, const QStyleOptionViewItem& o, const QModelIndex& i) const {
    int stars = i.data(Qt::DisplayRole).toInt();
    p->save();
    drawStars(p, o.rect, stars);
    p->restore();
}
QSize RatingDelegate::sizeHint(const QStyleOptionViewItem&, const QModelIndex&) const { return {96, 20}; }
QWidget* RatingDelegate::createEditor(QWidget* parent, const QStyleOptionViewItem&, const QModelIndex&) const {
    return new QSpinBox(parent);
}
// view->setItemDelegateForColumn(2, new RatingDelegate(view));
```

**Gotcha:** Keep paint() cheap because it is called for the cells being drawn, and always balance save() and restore(). Column delegates are set with setItemDelegateForColumn(); the view does not take ownership unless the delegate is parented.

## Checked
2026-11-03. Confirmed in the QStyledItemDelegate and QAbstractItemView pages: paint(), sizeHint() and createEditor() are the overridable functions, setItemDelegateForColumn(int, QAbstractItemDelegate*). Removed: the performance claims about every repaint and the ownership remark was reworded to a parent hint.

Method: documentation only; no commands were run.

## Verify
- Scrolling a 100k-row view stays smooth.
