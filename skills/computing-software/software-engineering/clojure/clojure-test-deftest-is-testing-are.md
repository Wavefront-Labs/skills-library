---
id: computing-software.software-engineering.clojure.clojure-test-deftest-is-testing-are
name: clojure-test-deftest-is-testing-are
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure.test, deftest, is, testing, are, thrown, run-tests, assertions, clojure-test-deftest, clojure-testing]
level: intro
status: docs-checked
description: "Write tests with deftest, is, testing and are, assert exceptions with thrown? and thrown-with-msg?, and run them with run-tests."
sources: ["https://clojure.github.io/clojure/clojure.test-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clojure.test basics

**Goal:** write and run unit tests with the built-in framework.

```clojure
(ns my.app.core-test
  (:require [clojure.test :refer [deftest is testing are run-tests]]
            [my.app.core :as c]))

(deftest add-test
  (testing "positive numbers"
    (is (= 3 (c/add 1 2))))
  (testing "errors"
    (is (thrown? ArithmeticException (/ 1 0)))
    (is (thrown-with-msg? clojure.lang.ExceptionInfo #"bad" (c/boom)))))

(deftest table-test
  (are [x y] (= y (c/double x))
    1 2
    2 4))
```
- A failing `(is (= 5 (+ 2 2)))` reports `expected:` (the original expression) and `actual:` (e.g. `(not (= 5 4))`); `is` accepts a message as a second argument: `(is (= 5 (+ 2 2)) "Crazy arithmetic")`.
- Run: `(run-tests 'my.app.core-test)` at the REPL; with no arguments it runs the current namespace, and `(run-all-tests)` runs every loaded namespace. Tests run in an undefined order.
- `(is (thrown? c ...))` checks the exception class; `(is (thrown-with-msg? c re ...))` also matches the message against a regex.
- `deftest` creates a function of no arguments named after the test, so it can be called directly (`(add-test)`) and tests can be composed by calling other tests; nested names appear in reports like `(arithmetic addition)`.
- If you compose tests, define `test-ns-hook` to control order; it prevents fixtures from running.
- Use `use-fixtures` (`:each` or `:once`) for setup and teardown.
- Binding `*load-tests*` to false when loading production code stops `deftest` and `with-test` from creating tests.

## Failure modes
- Test namespaces not run because they were never loaded: `run-tests` and `run-all-tests` only see loaded namespaces.
- State leaking between tests via atoms; reset in fixtures.

## Self-check
Run a failing and a passing test with `run-tests` and confirm the report counts one failure.

## Checked
2026-11-03. Confirmed against the clojure.test API page: is with message, report format, thrown? and thrown-with-msg?, with-test and deftest, testing, are, composing tests, run-tests and run-all-tests defaults, test-ns-hook and fixtures, use-fixtures :each/:once, *load-tests*. Removed: foo.core-test naming convention, lein and clojure -X runner commands, the exit-code self-check, with-redefs advice and the shadowing and suffix failure modes (not on the page).
Method: documentation only; no commands were run.
