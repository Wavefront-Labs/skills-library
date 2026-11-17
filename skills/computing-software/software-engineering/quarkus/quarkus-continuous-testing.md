---
id: computing-software.software-engineering.quarkus.quarkus-continuous-testing
name: quarkus-continuous-testing
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, continuous-testing, dev-mode, test-filtering, surefire, gradle]
level: practitioner
status: docs-checked
description: "Run Quarkus tests automatically on save: dev-mode hotkeys, quarkus:test without dev mode, and selecting tests with include/exclude patterns, -Dtest or --tests."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/continuous-testing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus continuous testing

Quarkus detects which tests cover which code and re-runs only the relevant tests after you save a change.

## Start it
Run dev mode. The bottom of the terminal shows `Tests paused, press [r] to resume, [h] for more options>`. Press `r` to start. To start automatically set `quarkus.test.continuous-testing=enabled` in `application.properties`; set `disabled` to turn it off entirely.

## Hotkeys (press `h` to list)
- `r` re-run all tests; `f` re-run failed tests
- `b` toggle "broken only" mode (only previously failing tests run, even if others are affected; useful when changing code used by many tests)
- `v` print failures from the last run again
- `p` pause (no feedback until you are done editing)
- `o` toggle test output (filtered by default so it does not interleave with dev mode output; filtered output is still viewable in the Dev UI)
- `i` toggle instrumentation based reload (avoids a restart if a change does not affect class structure, keeping state)
- `l` toggle live reload
- `s` force restart (scans for changes and restarts even with none; works with live reload disabled)
- `h` help, `q` quit

## Without dev mode
Run `mvn quarkus:test` or `gradle quarkusTest`. Useful when dev mode interferes (for example WireMock on the same port). The Dev UI is not available in this mode.

## Selecting tests
Config `quarkus.test.include-pattern` and `quarkus.test.exclude-pattern` are regular expressions matched against the fully qualified test class name. If include is configured, exclude is ignored.

Alternatively use the build tool's own filter with `quarkus:dev`/`quarkus:test` or `quarkusDev`/`quarkusTest`; when used, the `quarkus.test.[include|exclude]-pattern` config is ignored.
- Maven `-Dtest=...`: Surefire format, comma-separated globs of class paths and/or methods; prefix `!` excludes (exclusions win); `#` separates class glob from method globs, `+` separates multiple method globs. Examples: `Basic*`, `!Unstable*`, `pkg/**/Ci*leTest`, `#fast*+slowTest`. The `%regex[...]` and `%ant[...]` syntaxes are NOT supported.
- Gradle `--tests ...`: repeatable; pattern starting with an upper case letter matches the simple class name, otherwise the fully qualified name; method after a `.`; only wildcard is `*` (text based, ignores package delimiters). Examples: `com.example.Basic*`, `MyTest.test*`.

## Multi-module
Tests in modules other than the application also run on changes (enabled by default); restrict with `quarkus.test.only-test-application-module=true`.

## Checked

2026-11-07. Read in full: continuous-testing.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: an unconfirmed Verify line with a sample test-run summary.

Method: documentation only; no commands were run.
