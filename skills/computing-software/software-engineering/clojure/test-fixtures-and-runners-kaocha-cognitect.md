---
id: computing-software.software-engineering.clojure.test-fixtures-and-runners-kaocha-cognitect
name: test-fixtures-and-runners-kaocha-cognitect
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, fixtures, use-fixtures, kaocha, test-runner, cognitect, cloverage, test-selectors, once, each, clojure-test-fixtures-runners]
level: practitioner
status: draft
description: "Share setup with use-fixtures :once/:each, run tests from the CLI with Cognitect test-runner or Kaocha, select by metadata, and measure coverage with cloverage."
sources: ["https://clojure.github.io/clojure/clojure.test-api.html", "https://cljdoc.org/d/lambdaisland/kaocha/CURRENT"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixtures and test runners

**Goal:** share setup and run suites in CI.

```clojure
(defn db-fixture [f]
  (start-db!)
  (try (f) (finally (stop-db!))))
(use-fixtures :once db-fixture)       ; once per namespace
(use-fixtures :each reset-state)      ; around every deftest
(use-fixtures :once fixture-a fixture-b)
```
- A fixture is a function of one argument, the test function; always call it and use `try/finally`.
- Runners:
  - Cognitect `test-runner` (deps.edn alias, see deps-cli skills): `clojure -M:test` or `clojure -X:test`
    with `:dirs`, `:nses`, `:patterns` options.
  - Kaocha (`lambdaisland/kaocha`): `tests.edn` config, `clojure -M:kaocha`, `--focus my.ns/my-test`,
    `--watch`, plugins such as cloverage.
  - Leiningen: `lein test`, `lein test :only ns/var`, `lein test :integration` with test selectors defined as
    `:test-selectors {:integration :integration}` and `^:integration` metadata on the deftest.
- Coverage: `cloverage` (`lein cloverage` or `clojure -M:cov`) instruments namespaces and writes HTML to
  `target/coverage`.
- CI: run with `-Xmx` bounded, fail on non-zero exit code; print JUnit XML via Kaocha's `:kaocha.plugin/junit-xml`
  (plugin name unconfirmed) if the CI needs it.

## Failure modes
- Fixtures that throw before calling `(f)` skip the tests silently in some runners; keep setup minimal.
- Parallel test runners and shared global state (`def`s).

## Self-check
Mark one test `^:slow`, exclude it with a selector or `--skip-meta`, and confirm it is not run.
