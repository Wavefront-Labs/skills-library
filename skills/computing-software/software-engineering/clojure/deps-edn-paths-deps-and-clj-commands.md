---
id: computing-software.software-engineering.clojure.deps-edn-paths-deps-and-clj-commands
name: deps-edn-paths-deps-and-clj-commands
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, deps-edn, clj, clojure-cli, paths, deps, mvn-version, aliases, main-opts, -m, -x, -p, deps-edn-basics, clojure-deps-cli]
level: practitioner
status: docs-checked
description: "Configure projects with deps.edn (:paths, :deps, :aliases) and run the CLI with -M, -X, -T and -P; understand the cache and the clj versus clojure wrappers."
sources: ["https://clojure.org/reference/deps_and_cli", "https://clojure.org/guides/deps_and_cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deps.edn basics and the Clojure CLI

**Goal:** declare dependencies and run code with the official CLI.

```clojure
;; deps.edn
{:paths ["src" "resources"]
 :deps  {org.clojure/clojure {:mvn/version "1.12.0"}      ; use a current stable version
         org.clojure/data.json {:mvn/version "<current>"}}
 :aliases
 {:test {:extra-paths ["test"]
         :extra-deps  {io.github.cognitect-labs/test-runner {:git/tag "<tag>" :git/sha "<sha>"}}
         :main-opts   ["-m" "cognitect.test-runner"]}
  :dev  {:extra-paths ["dev"]}}}
```
```bash
clj                          # REPL (with rlwrap line editing); `clojure` runs without it
clojure -M -m my.app.main    # -M: run a main namespace / clojure.main options
clojure -M:test              # uses the alias :main-opts (several aliases: last :main-opts wins)
clojure -X:deploy :key val   # -X: call a fn from :exec-fn with EDN args
clojure -T:build uberjar     # -T: run a tool fn (project :deps removed, project :paths become ".")
clojure -P                   # prepare: download deps and cache the classpath, do not run
clojure -Spath               # print the classpath
clojure -Stree               # dependency tree
clojure -Srepro              # ignore the user deps.edn
```
- Config merge order: root deps.edn (with the install), user deps.edn (in `$CLJ_CONFIG`, else `$XDG_CONFIG_HOME/clojure`,
  else `~/.clojure`), project `deps.edn`, then command-line `-Sdeps`; merging is `merge-with merge` except that only the
  last source's `:paths` is used.
- Classpath cache lives in `.cpcache/` in the project directory; `-Sforce` forces recomputation, and `.cpcache/` belongs in `.gitignore`.
- Maven coordinates use `:mvn/version`.
- `-A` applies aliases to the classpath and is the only exec option usable for a REPL; `-M`, `-X`, `-T` say how to run.

## Failure modes
- A dep or path from an alias is missing from the classpath: the alias was not named on the command line; check with `clojure -M:alias -Spath`.
- The `clojure -X`/`-T` function is resolved through `:ns-default` and `:ns-aliases` of the aliases when unqualified.

## Self-check
`clojure -Spath` lists `src` and every jar; `clojure -Stree` shows the transitive tree.

## Checked
2026-11-03. Confirmed against the clojure.org Clojure CLI reference and deps.edn reference: clj versus clojure (rlwrap), exec options -A/-X/-T/-M/-P, -Sdeps, -Srepro, -Spath, -Stree, -Sforce, merge order and `:paths` rule, config directory variables, `.cpcache`, -T dropping project :deps, :main-opts replace semantics. Removed: `-Sdescribe`, the claim that aliases combine `:main-opts` (they replace; last wins), the `lein :dependencies` remark, the "Could not locate" message and the -A to -M migration remark.
Method: documentation only; no commands were run.
