---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-translations-lupdate
name: qt-translations-lupdate
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-translations-lupdate, qt-resources-i18n, qt, qt6, i18n, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Mark strings with tr(), build .ts and .qm files with qt_add_translations and load them with QTranslator."
sources:
  - https://doc.qt.io/qt-6/internationalization.html
  - https://doc.qt.io/qt-6/qtlinguist-cmake-qt-add-translations.html
  - https://doc.qt.io/qt-6/qtranslator.html
  - https://doc.qt.io/qt-6/qcoreapplication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt translations with lupdate and lrelease

**Goal:** a translatable UI.

```cmake
qt_add_translations(app TS_FILES app_de.ts app_fr.ts)   # creates update_translations and release_translations targets
```

```cpp
// code: label->setText(tr("Open file"));
QTranslator tr;
if (tr.load(QLocale(), "app", "_", ":/i18n")) qApp->installTranslator(&tr);
// in widgets: void changeEvent(QEvent* e) { if (e->type()==QEvent::LanguageChange) ui->retranslateUi(this); }
```

**Gotcha:** Use %n in the source string for plural forms ("%n file found" vs "%n files found" is chosen from n). release_translations builds the .qm files from the .ts files and is built by default; for plurals the source language may need its own .ts file.

## Checked
2026-11-03. Confirmed in the qt_add_translations, QTranslator, QCoreApplication and Internationalization pages: TS_FILES, update_translations and release_translations targets, load(QLocale, filename, prefix, directory), installing a translator generates LanguageChange and widgets re-translate (retranslateUi), %n plurals. Fixed: a cmake code fence that contained C++ comments. Removed: the concatenation advice and the QML qsTr remark (not in these pages).

Method: documentation only; no commands were run.

## Verify
- Installing a QTranslator triggers LanguageChange and the visible text updates.
