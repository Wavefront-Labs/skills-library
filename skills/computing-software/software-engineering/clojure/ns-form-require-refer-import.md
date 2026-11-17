---
id: computing-software.software-engineering.clojure.ns-form-require-refer-import
name: ns-form-require-refer-import
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, namespaces, ns, require, refer, alias, import, refer-clojure, as, use, load, ns-require-refer, clojure-namespaces]
level: intro
status: docs-checked
description: "Structure the ns form: :require with :as and :refer, :import for classes, :refer-clojure :exclude, plus REPL require :reload and file-to-namespace naming rules."
sources: ["https://clojure.org/reference/namespaces", "https://clojure.org/reference/libs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ns, require, refer, import

**Goal:** declare dependencies cleanly and load code predictably.

```clojure
(ns my.app.core
  (:refer-clojure :exclude [update])
  (:require [clojure.string :as str]
            [clojure.set :refer [union]]
            [my.app.db :as db])
  (:import (java.time Instant)
           (java.util UUID)))
```
- File `src/my/app/core.clj` must declare namespace `my.app.core`; dashes in a namespace become underscores in
  the path (`my-app.core` is `my_app/core.clj`).
- Prefer `:require ... :as` over `:refer :all` / `use`; reserve `:refer` for a few well-known vars (test macros).
- `:import` takes classes only; use `(:import (pkg Class1 Class2))` grouping.
- At the REPL: `(require '[my.app.core :as c] :reload)` reloads that namespace.
- `(in-ns 'x)` switches namespace without the machinery; `(ns x)` is the normal entry.

## Failure modes
- `FileNotFoundException: Could not locate ... on classpath`: path and ns mismatch, or the source dir is not on the classpath.
- Cyclic load dependency: namespace A requires B requires A. Extract the shared piece.
- `already refers to: #'clojure.core/update`: shadowing a core name; use `:refer-clojure :exclude`.

## Self-check
Create two files that require each other and read the error; then break the cycle.

## Checked
2026-11-02. Confirmed: clojure.org/reference/namespaces and clojure.org/reference/libs: ns with :require/:refer/:as/:import/:refer-clojure :exclude, namespace-to-file mapping (dashes become underscores), require with :reload, in-ns, import of classes. Removed: the exact old error text and the :reload-all remark.
Method: documentation only; no commands were run.
