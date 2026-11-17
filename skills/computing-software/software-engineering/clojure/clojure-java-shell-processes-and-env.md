---
id: computing-software.software-engineering.clojure.clojure-java-shell-processes-and-env
name: clojure-java-shell-processes-and-env
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, shell, clojure.java.shell, sh, processbuilder, babashka-process, getenv, system-properties, exit, shell-processes-env]
level: practitioner
status: docs-checked
description: "Run external commands with clojure.java.shell/sh (:in, :dir, :env, :out-enc), read the :exit/:out/:err result map, and avoid building shell strings from input."
sources: ["https://clojure.github.io/clojure/clojure.java.shell-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell commands, processes, environment

**Goal:** call external programs and read configuration safely.

```clojure
(require '[clojure.java.shell :as sh])
(sh/sh "ls" "-la")                          ;=> {:exit 0 :out "..." :err ""}
(sh/sh "cat" :in "input text")
(sh/sh "make" :dir "/path/to/project" :env {"CC" "gcc"})
(let [{:keys [exit out err]} (sh/sh "git" "status")] (when-not (zero? exit) (throw (ex-info err {}))))
(sh/with-sh-dir "/path/to/project" (sh/sh "make"))     ; bind :dir for several calls; with-sh-env does the same for :env
```
- `sh` passes the given strings to `Runtime.exec()` and returns a map of `:exit` (exit code), `:out` (stdout, a String or byte[]) and `:err` (stderr, a String via the platform default encoding).
- Options: `:in` (any input source `io/copy` accepts, e.g. a String, fed to stdin), `:in-enc` and `:out-enc` (charset name, default UTF-8; `:out-enc :bytes` returns a byte array), `:env` ("override the process env with a map"), `:dir` (a String or `java.io.File`).
- Pass arguments as separate strings; do NOT build one shell string with user input (command injection). `(sh/sh "sh" "-c" cmd)` is only for trusted commands.
- Clojure 1.12 also ships a `clojure.java.process` namespace for process control; it is not covered here.

## Failure modes
- `:out` is a byte array, not a String, when `:out-enc :bytes` is given.
- A non-zero `:exit` is not an exception: check it yourself.

## Self-check
Run `sh/sh` with a command that fails (for example `ls` on a missing path) and read `:exit` and `:err`.

## Checked
2026-11-03. Confirmed against the clojure.java.shell API page: sh arguments and options (:in, :in-enc, :out-enc, :env, :dir), the :exit/:out/:err result map, with-sh-dir and with-sh-env; the namespace list on the Clojure API pages shows clojure.java.process. Removed: ProcessBuilder, babashka/process, System/getenv, System/getProperty, System/exit and shutdown-hook advice, the claim that :env replaces the whole environment, *command-line-args* notes, and the IOException and deadlock failure modes (Java behaviour, not on the pages read).
Method: documentation only; no commands were run.
