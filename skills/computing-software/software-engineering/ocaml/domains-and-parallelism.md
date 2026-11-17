---
id: computing-software.software-engineering.ocaml.domains-and-parallelism
name: domains-and-parallelism
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, domains-parallel, ocaml-concurrency, domain-spawn, multicore, recommended-domain-count]
level: advanced
status: docs-checked
description: "Spawn and join Domains, size to Domain.recommended_domain_count, and know the 128-domain limit and domain-local state."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domains

```ocaml
let work n = let rec fib n = if n < 2 then n else fib (n-1) + fib (n-2) in fib n
let () =
  let ds = List.init 4 (fun _ -> Domain.spawn (fun () -> work 32)) in
  let rs = List.map Domain.join ds in
  List.iter (Printf.printf "%d\n") rs
let n = Domain.recommended_domain_count ()
```

## Notes
- OCaml 5.0+ only. The manual recommends higher-level libraries such as `domainslib` (async/await tasks and parallel iterators over a work-stealing pool) rather than raw `Domain.spawn`.
- At most 128 domains can be active at the same time and spawning more raises an exception; the `d` OCAMLRUNPARAM option sets the maximum (128 on 64-bit, 16 on 32-bit platforms).
- Mutable data shared across domains needs `Atomic` or `Mutex`/`Condition`; the manual's parallelism chapter uses both.
- `Domain.DLS` provides domain-local state; `Domain.self ()`; `Domain.cpu_relax ()` in spin loops.
- The major heap is collected by a concurrent mark-and-sweep algorithm with a few short stop-the-world pauses per major cycle.
- Systhreads (`Thread`) still exist; threads inside one domain share the domain lock.

## Self-check
- [ ] `time` shows wall time less than the sum of per-domain times.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the parallelism chapter (domainslib recommendation, 128-domain limit, major-heap collection, systhreads inside a domain), the Domain API page (recommended_domain_count, DLS, cpu_relax) and the ocamlrun page (d option).

Removed or corrected: the Saturn mention, the claim that minor collections stop all domains, the allocation-scaling claim and the 'unconfirmed' limit wording.

Method: documentation only; no commands were run.
