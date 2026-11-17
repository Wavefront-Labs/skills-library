---
id: computing-software.software-engineering.clojure.malli-validate-explain-and-generate
name: malli-validate-explain-and-generate
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, malli, schema, validation, explain, humanize, transform, generators, registry, malli-schemas, clojure-validation]
level: advanced
status: docs-checked
description: "Validate and transform data with Malli (m/validate, m/explain, me/humanize, m/decode, mg/sample, m/validator), open-by-default maps and registries."
sources: ["https://github.com/metosin/malli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Malli

**Goal:** describe data with plain vectors and keywords, usable at runtime.

```clojure
(require '[malli.core :as m] '[malli.error :as me] '[malli.transform :as mt] '[malli.generator :as mg])
(m/validate :int 1)                                  ;=> true
(m/validate :int "1")                                ;=> false
(def User [:map [:id :int] [:name :string] [:email {:optional true} :string]])
(-> (m/explain User {:id "x"}) me/humanize)          ; readable messages (exact text not verified)
(m/decode :int "42" mt/string-transformer)           ;=> 42
(mg/sample [:and :int [:> 10] [:< 100]] {:seed 123}) ; generated values (needs test.check)
(m/validator [:map [:x :boolean] [:y {:optional true} :int] [:z :string]])  ; optimised pure validator
```
- `m/explain` returns nil for valid values, else a map with `:schema`, `:value` and `:errors`; each error has
  `:path`, `:in`, `:schema` and `:value`. `malli.error/humanize` turns this into readable messages.
- The included transformers are best-effort and pass bad input through unchanged, so validate after decoding.
- Maps are open by default (extra keys pass); `{:closed true}` makes extra keys fail.
- Schemas are looked up via the `malli.registry/Registry` protocol; `malli.core/default-registry` is used
  unless a `:registry` option is passed. Local registries use the `:registry` schema property;
  `mr/set-default-registry!` changes the global default. The default registry has over 100 schemas.
- Function schemas use `[:=> [:cat :int] :int]` syntax (see the repo's docs/function-schemas.md).
- The README mentions reitit coercion only in connection with its Lite syntax.

## Self-check
Validate a bad payload and print the humanized error; decode string inputs to ints.

## Checked
Method: 2026-11-08 read the malli README (first 100,000 of about 123,700 characters). Removed unsupported claims: the schema type list, `malli.instrument` and `m/=>` instrumentation, recursive schema syntax, the "compared to spec" claims, the exact humanize output text, and the recompile-cost claim. Unchanged: the User schema is illustrative and was not run.
