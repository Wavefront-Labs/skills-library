---
id: computing-software.software-engineering.clojure.project-structure-and-namespace-design
name: project-structure-and-namespace-design
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, project-layout, namespace-design, src, test, resources, dev, user-clj, monorepo, polylith, api-boundary, project-layout-namespaces, clojure-code-organization]
level: practitioner
status: draft
description: "Lay out a Clojure project (src/test/dev/resources), design namespaces without cycles, separate pure core from effects, and scale with monorepo tools like Polylith."
sources: ["https://clojure.org/guides/deps_and_cli", "https://polylith.gitbook.io/polylith"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Project layout and namespace design

**Goal:** a structure that stays navigable and cycle-free.

```
deps.edn
src/my/app/{core,http,db,domain/...}.clj
test/my/app/...-test.clj
dev/user.clj            ; REPL helpers, only on the :dev alias path
resources/ config.edn migrations/
build.clj
.clj-kondo/ .cljfmt.edn
```
- Namespace per concept: `my.app.domain.user` (pure functions on data), `my.app.db.user` (SQL), `my.app.http.user`
  (handlers), `my.app.system` (wiring). Dependencies point inward toward the domain.
- Avoid cyclic requires: extract shared pure functions or protocols to a lower namespace; use `declare`/`resolve`
  only as a last resort.
- Functional core, imperative shell: effects (IO, time, random) at the edges, pure functions in the middle.
- Plain data (maps, vectors) for domain entities, specs/schemas at the boundary; records only when needed.
- Public API vs internals: use `defn-`, `^:no-doc` metadata, and an `-api` or `core` namespace as the façade;
  document with docstrings.
- File naming: namespace `my-app.core` to file `my_app/core.clj`.
- Monorepos: deps.edn `:local/root` projects, or Polylith (components and bases with interfaces) for large systems.
- Keep `dev/user.clj` out of production artifacts by putting `dev` only on the `:dev` alias.

## Failure modes
- Everything in one `core.clj` that grows to thousands of lines.
- Test namespaces depending on dev-only code.

## Self-check
Generate a require graph (for example with `clojure.tools.namespace.dependency`) and confirm it is acyclic.
