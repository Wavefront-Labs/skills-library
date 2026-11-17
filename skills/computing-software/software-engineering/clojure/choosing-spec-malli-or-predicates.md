---
id: computing-software.software-engineering.clojure.choosing-spec-malli-or-predicates
name: choosing-spec-malli-or-predicates
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, spec, malli, schema, validation-strategy, boundary-validation, coercion, trade-offs, spec-vs-malli-choice]
level: practitioner
status: gated
description: "Decide between clojure.spec, Malli and hand-written predicates by where validation happens (boundary, internal, tests), coercion and generation needs."
sources: ["https://clojure.org/about/spec", "https://github.com/metosin/malli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a validation approach

**Goal:** validate at the right places with the least machinery.

- Validate at system boundaries (HTTP input, config, DB rows, files), not inside every function.
- Spec: built in to the Clojure ecosystem, great for function contracts (`fdef`) and generative tests; global
  registry of qualified keywords; poor tooling for coercion/transform and for dynamic schema construction.
- Malli: schemas are data; coercion, humanised errors, JSON schema/OpenAPI export, closed maps; works at runtime and
  in ClojureScript; good for API validation.
- Plain predicates (`string?`, `pos-int?`) and `assert` are enough for simple internal invariants.
- Error format: return structured errors (`{:field :age :message ...}`) with 400 responses; do not leak stack traces.
- Performance: precompile validators; skip deep validation on hot internal paths.
- Do not mix registries for the same domain concept: pick one source of truth, derive the other if required.

## Failure modes
- Validating twice with different rules.
- Trusting client-side validation only.

## Self-check
List the three boundaries in your app where untrusted data enters and confirm each is validated once.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; spec and Malli pages read; the comparison claims and error-format advice are judgement not stated on them. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
