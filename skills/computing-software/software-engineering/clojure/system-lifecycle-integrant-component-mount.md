---
id: computing-software.software-engineering.clojure.system-lifecycle-integrant-component-mount
name: system-lifecycle-integrant-component-mount
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, integrant, component, mount, system, lifecycle, dependency-injection, ig-init, ig-halt, reloaded-workflow, system-lifecycle-integrant, clojure-system-design]
level: advanced
status: docs-checked
description: "Manage stateful resources (servers, pools) with Integrant (init-key/halt-key!) or Component, and a reloaded workflow with go/reset; avoid global state."
sources: ["https://github.com/weavejester/integrant", "https://github.com/stuartsierra/component"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component lifecycle with Integrant

**Goal:** start and stop the application's stateful parts in dependency order.

```clojure
(require '[integrant.core :as ig])
(def config {:app/db {:url "jdbc:..."}
             :app/server {:port 3000 :db (ig/ref :app/db)}})
(defmethod ig/init-key :app/db [_ opts] (make-pool opts))
(defmethod ig/halt-key! :app/db [_ pool] (.close pool))
(defmethod ig/init-key :app/server [_ {:keys [port db]}] (run-jetty (handler db) {:port port :join? false}))
(defmethod ig/halt-key! :app/server [_ s] (.stop s))
(def system (ig/init config))
(ig/halt! system)
```
- Config is plain EDN data (so it can come from aero), with `ig/ref` expressing dependencies; start order is
  topological and halt order reversed.
- `halt-key!` should be idempotent; `halt!` is side-effectful and its return value should be ignored.
- Add `ig/assert-key` methods to fail fast on bad config; the error is wrapped in an `ExceptionInfo`.
- Reloaded workflow at the REPL (Stuart Sierra's pattern): use Integrant-REPL, linked from the Integrant README.
- Component (Stuart Sierra) uses records implementing `component/Lifecycle`; `system-map` + `using` for dependencies.
  It starts components in dependency order. For very small apps the README says wiring dependencies by hand may be
  less work.
- Keep resource creation out of `def` at namespace load; start from `-main` and tests so tests can build isolated
  systems.
- Pass dependencies explicitly as arguments rather than reaching for globals.

## Failure modes
- Forgetting `halt-key!` leaks ports across `reset` calls.

## Self-check
Start the system twice with `reset`; confirm the port is released and rebound each time.

## Checked
2026-11-08. Partial read of both READMEs (searched and read the relevant sections). Confirmed: Integrant `ig/init-key`, `ig/halt-key!`, `ig/ref`, reverse-order `halt!`, idempotent `halt-key!`, `assert-key` with ExceptionInfo, pointer to Integrant-REPL; Component `Lifecycle` protocol, `system-map`, `using`, dependency-ordered start, small-app caveat. Removed: Mount description, `dev/user.clj` and `tools.namespace.repl/refresh` specifics, and the claim that Integrant halts partially started systems on init failure.
Method: documentation only; no commands were run.
