---
id: computing-software.software-engineering.clojure.leiningen-project-clj-and-tasks
name: leiningen-project-clj-and-tasks
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, leiningen, lein, project-clj, defproject, dependencies, source-paths, main, aot, uberjar, lein-run, lein-project-clj, clojure-leiningen]
level: practitioner
status: draft
description: "Configure a Leiningen project with defproject (:dependencies, :main, :aot, :profiles) and run lein repl, test, run, uberjar, deps :tree and check."
sources: ["https://leiningen.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leiningen project.clj

**Goal:** use Leiningen for projects that still depend on it.

```clojure
(defproject my/app "0.1.0-SNAPSHOT"
  :description "..."
  :dependencies [[org.clojure/clojure "1.12.0"]
                 [ring/ring-core "<version>"]]
  :source-paths ["src"]
  :test-paths ["test"]
  :resource-paths ["resources"]
  :main ^:skip-aot my.app.main          ; skip AOT for dev, uberjar profile compiles
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}
             :dev {:dependencies [[org.clojure/test.check "<version>"]]
                   :source-paths ["dev"]}})
```
```bash
lein new app my-app        # template (also: lein new default)
lein repl     lein run     lein test     lein test :only my.ns/test-name
lein uberjar               # target/uberjar/<name>-<version>-standalone.jar
lein deps :tree            # dependency tree, shows conflicts
lein check                 # compile all namespaces, shows reflection warnings
lein ancient               # plugin: outdated deps
```
- `lein` forks a JVM for your project plus its own; startup is slow compared with the Clojure CLI.
- `~/.lein/profiles.clj` holds user-level profiles and plugins (`:user` profile).
- `:jvm-opts ["-Xmx1g"]` sets JVM flags; `:global-vars {*warn-on-reflection* true}` for hints.
- `lein deps :tree` marks conflicting overrides; use `:exclusions [group/artifact]` on a dependency vector.

## Failure modes
- Uberjar fails to start: `:aot` or `:main` missing `(:gen-class)`.
- Stale `target/` classes causing odd failures; `lein clean`.

## Self-check
`lein uberjar && java -jar target/uberjar/*-standalone.jar` runs the app.
