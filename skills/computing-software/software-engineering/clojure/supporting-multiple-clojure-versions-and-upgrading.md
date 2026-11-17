---
id: computing-software.software-engineering.clojure.supporting-multiple-clojure-versions-and-upgrading
name: supporting-multiple-clojure-versions-and-upgrading
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, compatibility, backwards-compat, upgrade, deprecation, multi-version-testing, deps-edn-aliases, jdk-versions, version-compat-libraries]
level: advanced
status: docs-checked
description: "Support several Clojure and JDK versions with test aliases, reader conditionals, and a careful upgrade routine including deprecations and dependency alignment."
sources: ["https://clojure.org/dev/dev", "https://clojure.org/news/news", "https://clojure.org/guides/deps_and_cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting multiple versions and upgrading

**Goal:** keep libraries portable and upgrade apps without surprises.

- The Clojure team stresses backward compatibility; major releases come about once per year with no fixed schedule,
  and ongoing changes are visible in alpha releases and the Dev Changelog. Read the release notes (clojure.org news)
  before each upgrade.
- Declare the minimum supported Clojure version in the library's README; depend on the oldest one you support.
- Test matrix via aliases, using `:override-deps` (shown in the deps_and_cli guide) to swap the Clojure version:
```clojure
:aliases {:old {:override-deps {org.clojure/clojure {:mvn/version "<oldest-supported>"}}}
          :new {:override-deps {org.clojure/clojure {:mvn/version "<newest-supported>"}}}}
```
```bash
clojure -M:old:test && clojure -M:new:test
```
- Bridge missing functions in one compat namespace, not scattered version checks.
- Upgrade routine: bump Clojure, run tests and the linter, then bump libraries, then JDK.
- Pin the Clojure version in apps; libraries should not force a specific Clojure on consumers beyond the minimum.
- Test on every JDK you deploy.

## Failure modes
- A new core var colliding with one of your own names after an upgrade; rename your var.
- Mixed versions of dependencies that bundle Clojure libraries causing load errors.

## Self-check
Run the test suite against the oldest and newest Clojure you claim to support.

## Checked
2026-11-08. Confirmed: clojure.org/dev/dev (backward-compatibility emphasis, about yearly major releases, no fixed schedule, alpha releases and Dev Changelog); clojure.org deps_and_cli guide (`:override-deps` alias). Removed: specific version numbers in the example (now placeholders), the claim that releases never remove public APIs, the `parse-long`/`update-vals` examples, the exact warning text, the contrib-library versioning claim, spec.alpha bundling details, `*warn-on-reflection*` and `:refer-clojure` advice, none of which the pages read state.
Method: documentation only; no commands were run.
