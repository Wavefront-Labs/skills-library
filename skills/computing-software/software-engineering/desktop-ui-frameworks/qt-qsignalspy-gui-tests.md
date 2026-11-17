---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qsignalspy-gui-tests
name: qt-qsignalspy-gui-tests
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qsignalspy-gui-tests, qt-testing, qt, qt6, qttest, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Assert signal emissions with QSignalSpy and simulate input with QTest::mouseClick."
sources:
  - https://doc.qt.io/qt-6/qtest-overview.html
  - https://doc.qt.io/qt-6/qsignalspy.html
  - https://doc.qt.io/qt-6/qtest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QSignalSpy and GUI event simulation

**Goal:** tests of widgets without a human.

```cpp
QPushButton b("go");
QSignalSpy spy(&b, &QPushButton::clicked);
QTest::mouseClick(&b, Qt::LeftButton);
QCOMPARE(spy.count(), 1);
QTest::keyClicks(edit, "hello");
QVERIFY(spy.wait(1000));                 // for async signals
// headless CI: run the test with -platform offscreen (fully supported only on X11)
```

**Gotcha:** QSignalSpy::wait returns a bool, so always QVERIFY it; since Qt 6.6 the default timeout is 5 seconds.

## Checked
2026-11-03. Confirmed in the QSignalSpy, QTest and QtTest overview pages: QSignalSpy constructor, count(), wait(), QTest::mouseClick and keyClicks, the offscreen platform plugin (-platform offscreen, fully supported on X11 only), QCOMPARE/QVERIFY. Removed: the QT_QPA_PLATFORM environment variable form and the throws-versus-false remark.

Method: documentation only; no commands were run.

## Verify
- The tests pass with -platform offscreen on CI.
