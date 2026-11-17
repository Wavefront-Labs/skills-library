---
id: computing-software.software-engineering.clojure.tools-build-jar-and-uberjar
name: tools-build-jar-and-uberjar
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, tools-build, uberjar, jar, compile-clj, copy-dir, create-basis, build-clj, deps-new, deploy, clojars, tools-build-uberjar]
level: advanced
status: docs-checked
description: "Build jars and uberjars with tools.build (create-basis, copy-dir, compile-clj, uber) from a build.clj, and deploy libraries to Clojars."
sources: ["https://clojure.org/guides/tools_build", "https://clojure.org/reference/deps_and_cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tools.build: jar and uberjar

**Goal:** package an application reproducibly with the official build library.

deps.edn alias:
```clojure
:build {:deps {io.github.clojure/tools.build {:git/tag "<tag>" :git/sha "<sha>"}}
        :ns-default build}
```
`build.clj`:
```clojure
(ns build (:require [clojure.tools.build.api :as b]))
(def class-dir "target/classes")
(def uber-file "target/app.jar")
(defn clean [_] (b/delete {:path "target"}))
(defn uber [_]
  (clean nil)
  (let [basis (b/create-basis {:project "deps.edn"})]
    (b/copy-dir {:src-dirs ["src" "resources"] :target-dir class-dir})
    (b/compile-clj {:basis basis :src-dirs ["src"] :class-dir class-dir
                    :ns-compile '[my.app.main]})
    (b/uber {:class-dir class-dir :uber-file uber-file :basis basis :main 'my.app.main})))
```
```bash
clojure -T:build uber
java -jar target/app.jar
```
- The main namespace should have `(:gen-class)` and a `-main` function; `b/compile-clj` compiles the `:ns-compile` namespaces and everything they load, so add namespaces that are loaded dynamically or optionally.
- Libraries use `b/write-pom` and `b/jar`; `deps-deploy` reads Clojars credentials from the env vars `CLOJARS_USERNAME` and `CLOJARS_PASSWORD` (a token) and gets name and version from `pom.xml`.
- `create-basis` downloads deps as a side effect.
- Never commit deploy tokens.

## Failure modes
- The jar does not start: check the main namespace has `(:gen-class)`, is listed in `:ns-compile`, and `:main` is passed to `b/uber`.
- A namespace loaded only at runtime is missing from the uberjar: add it to `:ns-compile`.

## Self-check
Run `java -jar target/app.jar` on a machine without Clojure installed; it must start.

## Checked
2026-11-03. Confirmed against the clojure.org tools.build guide (create-basis, copy-dir, compile-clj with :ns-compile, uber with :main, write-pom, jar, delete, `(:gen-class)` and `-main` requirement, `clj -T:build` invocation) and the deps-deploy README (CLOJARS_USERNAME/CLOJARS_PASSWORD, pom.xml). Removed: the manifest Main-Class explanation, the META-INF/services merge and `:conflict-handlers` remark, and the JVM "Could not find or load main class" message (none in the pages read).
Method: documentation only; no commands were run.
