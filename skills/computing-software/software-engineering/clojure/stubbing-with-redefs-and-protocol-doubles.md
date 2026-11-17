---
id: computing-software.software-engineering.clojure.stubbing-with-redefs-and-protocol-doubles
name: stubbing-with-redefs-and-protocol-doubles
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, with-redefs, mocking, stubs, test-doubles, protocols, spy, dependency-injection, mockery, clojure-test-mocking-stubs]
level: practitioner
status: draft
description: "Isolate code in tests with with-redefs, binding of dynamic vars, protocol-based fakes and passing dependencies as arguments instead of mocking globals."
sources: ["https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stubbing and test doubles

**Goal:** test code with side effects without a real network or database.

```clojure
(deftest fetch-user-test
  (with-redefs [http/get (fn [url] {:status 200 :body "{\"id\":1}"})]
    (is (= 1 (:id (svc/fetch-user 1))))))

(defn save! [db user] ...)                  ; pass db in rather than reading a global
(def calls (atom []))
(with-redefs [mailer/send! (fn [& args] (swap! calls conj args))] (do-work) (is (= 1 (count @calls))))
```
- `with-redefs` swaps var roots for ALL threads for its duration; avoid with parallel tests and with futures
  that outlive the scope.
- Dynamic vars plus `binding` are thread-local and safer, but only work for `^:dynamic` vars.
- Prefer injection: a protocol (`defprotocol Store`) with a real record and a `reify` fake in tests.
- Direct linking (`-Dclojure.compiler.direct-linking=true`) bypasses var lookup, so `with-redefs` has no effect on
  directly-linked callers; keep it off in test builds.
- Inline-expanded functions (such as `+`) cannot be redefined this way.
- Record calls in an atom to assert interactions; keep assertions on observable outputs when possible.

## Failure modes
- Redefining a var that the compiler inlined or that is called through a captured value.
- Test pollution from forgotten global redefinitions in the REPL.

## Self-check
Stub a function in one test and verify the original returns after the `with-redefs` block.
