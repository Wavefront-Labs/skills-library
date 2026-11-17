---
id: computing-software.software-engineering.clojure.scripting-with-babashka-and-clojure-main
name: scripting-with-babashka-and-clojure-main
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, babashka, bb, scripting, bb-edn, tasks, shebang, clojure-main, fast-startup, cli, scripting-babashka]
level: practitioner
status: draft
description: "Write fast-starting Clojure scripts with Babashka (bb.edn tasks, babashka.fs, babashka.process, pods) or clojure -M, and know its limits versus the full JVM."
sources: ["https://github.com/babashka/babashka", "https://book.babashka.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scripting with Babashka

**Goal:** use Clojure for shell glue with ~10 ms startup.

```clojure
#!/usr/bin/env bb
(require '[babashka.fs :as fs] '[babashka.process :refer [shell]] '[cheshire.core :as json])
(doseq [f (fs/glob "." "**/*.edn")] (println (str f)))
(shell "git" "status")                       ; inherits stdio; throws on non-zero exit
(-> (shell {:out :string} "date") :out)
(println *command-line-args*)
```
`bb.edn`:
```clojure
{:paths ["src" "scripts"]
 :deps {medley/medley {:mvn/version "<v>"}}
 :tasks {test  {:doc "Run tests" :task (shell "clojure -M:test")}
         build {:depends [test] :task (clojure "-T:build uber")}}}
```
- Run: `bb script.clj`, `bb -e '(+ 1 2)'`, `bb tasks`, `bb test`.
- Babashka is a native image with an SCI interpreter: most `clojure.core` works, libraries must be pure Clojure
  or Babashka-compatible; some classes/interop are unavailable; no AOT-compiled Java classes at runtime.
- Built-in libs: `clojure.string/set/walk/edn/data/test`, `cheshire`, `babashka.fs`, `babashka.process`,
  `clojure.java.io`, `org.httpkit.client`; more via `:deps` (pure Clojure) and pods (external binaries).
- JVM alternative: `clojure -M script.clj` (slower start, full language), or shebang with `clojure -M`.
- Use Babashka for tasks and glue, the JVM for long-running services.

## Failure modes
- `Could not resolve symbol` from a class not in the Babashka build.
- Relying on `*file*`/`*ns*` behaviour that differs from the JVM.

## Self-check
Write a script that lists files and prints sizes, run it with `bb`, and time it against the JVM version.
