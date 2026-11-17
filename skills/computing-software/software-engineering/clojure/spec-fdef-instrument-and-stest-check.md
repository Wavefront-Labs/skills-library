---
id: computing-software.software-engineering.clojure.spec-fdef-instrument-and-stest-check
name: spec-fdef-instrument-and-stest-check
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, spec, fdef, instrument, check, stest, orchestra, function-specs, generative-testing, args, ret, fn, spec-fdef-instrument]
level: advanced
status: docs-checked
description: "Spec functions with s/fdef (:args :ret :fn), enable argument checking with stest/instrument, and property-test them with stest/check; know instrument vs check."
sources: ["https://clojure.org/guides/spec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fdef, instrument and stest/check

**Goal:** specify function contracts and test them.

```clojure
(require '[clojure.spec.test.alpha :as stest])
(defn ranged-rand [start end] (+ start (long (rand (- end start)))))
(s/fdef ranged-rand
  :args (s/and (s/cat :start int? :end int?) #(< (:start %) (:end %)))
  :ret  int?
  :fn   #(<= (-> % :args :start) (:ret %) (-> % :args :end)))

(stest/instrument `ranged-rand)         ; validates :args on each call (dev only)
(stest/unstrument `ranged-rand)
(stest/check `ranged-rand)              ; generative test of :args/:ret/:fn
```
- `instrument` checks only `:args` (not `:ret` / `:fn`); validating the implementation belongs in `check` at test time.
- The guide recommends instrumentation in development and test, not production, because of the args-checking overhead.
- Generators (`check`, `exercise`) need `org.clojure/test.check` as a dev/test dependency.
- Name functions with a syntax-quote symbol (`` `f ``) so it is namespace-qualified.
- `s/fdef` on a macro validates its `:args` at macro expansion time, so no `instrument` call is needed; spec'ing a macro's `:ret` is usually unhelpful (it is just code).
- `instrument` takes options, e.g. `{:stub #{`f}}` replaces `f` with a stub whose results are generated from its `:ret` spec.

## Failure modes
- Argument errors from instrument print `Execution error - invalid arguments to user/ranged-rand` followed by the failing value and predicate, e.g. `{:start 8, :end 5} - failed: (< (:start %) (:end %))`.

## Self-check
Instrument a function and call it with a bad argument; expect an error naming the failed `:args` predicate.

## Checked
2026-11-03. Confirmed against the clojure.org spec guide: s/fdef with :args/:ret/:fn, instrument and unstrument taking a fully-qualified symbol, instrument checking only :args, check generating args and verifying :ret and :fn, test.check dev dependency, macro specs checked at expansion, `:stub` option, development-only advice, error text. Removed: summarize-results, bare `(stest/instrument)`, the orchestra remark, the captured-fn remark, `Unable to resolve spec`, the `Call to #'ns/f` message and the ExceptionInfo claim (not in the pages read).
Method: documentation only; no commands were run.
