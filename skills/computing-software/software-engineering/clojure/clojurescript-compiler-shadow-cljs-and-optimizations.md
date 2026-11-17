---
id: computing-software.software-engineering.clojure.clojurescript-compiler-shadow-cljs-and-optimizations
name: clojurescript-compiler-shadow-cljs-and-optimizations
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojurescript, cljs, shadow-cljs, cljs-main, google-closure, advanced-optimizations, externs, npm, cljs-basics-build, clojure-clojurescript]
level: practitioner
status: draft
description: "Compile ClojureScript with cljs.main or shadow-cljs, choose :none/:simple/:advanced optimizations, use npm packages, handle externs and understand source maps."
sources: ["https://clojurescript.org/guides/quick-start", "https://clojurescript.org/reference/compiler-options"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ClojureScript tooling

**Goal:** build and run ClojureScript for browser or Node.

## Quick start with cljs.main
```bash
clojure -Sdeps '{:deps {org.clojure/clojurescript {:mvn/version "<current>"}}}' -M -m cljs.main --repl
clojure -M -m cljs.main -d out -o out/main.js -c my.app.core          # compile
clojure -M -m cljs.main -O advanced -c my.app.core                     # optimized
```
## shadow-cljs (common choice)
- `shadow-cljs.edn`:
```clojure
{:deps true
 :builds {:app {:target :browser :output-dir "public/js"
                :modules {:main {:init-fn my.app.core/init}}
                :devtools {:http-root "public" :http-port 8020}}}}
```
- `npx shadow-cljs watch app`, `release app`, `node-repl`; dependencies from npm via `package.json`
  and `(:require ["react" :as react])`.
- Optimization levels: `:none` (dev, fast, many files), `:simple`, `:advanced` (Google Closure Compiler, smallest,
  renames properties).
- Advanced mode breaks interop on unrenamed property names: use `(.-prop obj)` / `(goog.object/get obj "prop")` with
  string access for external data, and externs for JS libraries (shadow-cljs infers many externs; see its warnings).
- Compiler options of interest: `:main`, `:output-to`, `:output-dir`, `:target :nodejs`, `:source-map`, `:optimizations`.
- Code reload: use shadow-cljs hot reload or figwheel-main; keep state in `defonce`.

## Failure modes
- Works in `:none` but fails in `:advanced`: renamed properties or missing externs.
- Large bundles: check `:build-report`/shadow-cljs build report and avoid pulling unused libs.

## Self-check
Build with `release` and run the output; compare behaviour with the dev build.
