---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qtest-unit-tests
name: qt-qtest-unit-tests
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qtest-unit-tests, qt-testing, qt, qt6, qttest, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Write QObject-based QtTest cases and register them with CTest."
sources:
  - https://doc.qt.io/qt-6/qtest-overview.html
  - https://doc.qt.io/qt-6/qtest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QtTest unit tests with CMake

**Goal:** automated Qt tests.

```cpp
class TstMath : public QObject { Q_OBJECT
private slots:
    void add_data() { QTest::addColumn<int>("a"); QTest::addColumn<int>("b"); QTest::addColumn<int>("sum");
                      QTest::newRow("small") << 1 << 2 << 3; }
    void add() { QFETCH(int, a); QFETCH(int, b); QFETCH(int, sum); QCOMPARE(a + b, sum); }
};
QTEST_APPLESS_MAIN(TstMath)
// CMake: find_package(Qt6 REQUIRED COMPONENTS Test); add_test(NAME math COMMAND tst_math)
// the QtTest overview sets CMAKE_AUTOMOC ON for the test target
```

**Gotcha:** Each private slot of the QObject subclass is a test function; QTEST_APPLESS_MAIN is for tests without a QApplication (QTEST_MAIN creates one); data-driven tests add columns with QTest::addColumn and rows with QTest::newRow, read with QFETCH.

## Checked
2026-11-03. Confirmed in the QtTest overview and QTest pages: private slots as test functions, QTest::addColumn/newRow/QFETCH, QTEST_APPLESS_MAIN, find_package(Qt6 REQUIRED COMPONENTS Test), add_test, CMAKE_AUTOMOC. Removed: the tst_math.moc include and the claim that it is required (CMake AUTOMOC behaviour, not in the Qt pages).

Method: documentation only; no commands were run.

## Verify
- ctest --output-on-failure passes, and a deliberate failure is reported.
