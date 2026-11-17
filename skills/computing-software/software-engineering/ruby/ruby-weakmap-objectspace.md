---
id: computing-software.software-engineering.ruby.ruby-weakmap-objectspace
name: ruby-weakmap-objectspace
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, weakmap-objectspace, memory]
level: advanced
status: docs-checked
description: "Cache without leaking: ObjectSpace::WeakMap and WeakKeyMap, define_finalizer pitfalls and WeakRef."
sources: ["https://docs.ruby-lang.org/en/master/ObjectSpace/WeakMap.html", "https://docs.ruby-lang.org/en/master/ObjectSpace/WeakKeyMap.html", "https://docs.ruby-lang.org/en/master/ObjectSpace.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WeakMap, WeakKeyMap and finalizers

A plain Hash cache holding objects as keys or values keeps them alive forever. Weak containers let the GC reclaim entries.

```ruby
cache = ObjectSpace::WeakMap.new     # keys and values both weak, compared by identity
cache[obj] = computed
cache[obj]                           # nil once collected
cache.key?(obj)

wk = ObjectSpace::WeakKeyMap.new     # Ruby 3.3+: only keys weak, lookup by eql?/hash
wk[key_string] = metadata

require "weakref"
ref = WeakRef.new(big); ref.weakref_alive?
```
Finalizers run after an object is collected:
```ruby
ObjectSpace.define_finalizer(obj, proc { |id| cleanup(path) })
# the proc must NOT reference obj, or it can never be collected
```
Prefer an explicit `close`/`ensure` for resources; finalizers are a safety net.

## Gotchas
- WeakMap compares keys by identity, so two equal strings are different keys; use WeakKeyMap (3.3 or later; check `RUBY_VERSION`) for value-equality lookups.
- WeakKeyMap holds its values strongly, so a value is not collected while its pair is in the map; only garbage-collectable objects can be keys (others raise `ArgumentError`). `getkey` returns the stored key equal to a probe.
- A finalizer runs when the object is destroyed by the GC or when Ruby shuts down, whichever comes first. An exception inside one is reported as a warning ("Exception in finalizer"). Do not depend on finalizers for correctness or for flushing data.
- Defining a finalizer in an instance method can keep the object alive if the block or callable refers to it (including implicitly through `self`). Build the callable in a class method or a separate callable object.
- Collection is nondeterministic: the docs use `GC.start` only for demonstration and say it might not always give the shown results.

Verify: store a fresh object, drop the reference, call `GC.start` and check whether `cache.size` decreases (it may not).

## Checked
2026-11-03. Confirmed against the rdoc comments in ruby/ruby `weakmap.c` and `gc.c` (ObjectSpace::WeakMap, WeakKeyMap, define_finalizer), `lib/weakref.rb` (`weakref_alive?`), and `doc/NEWS/NEWS-3.3.0.md` (WeakKeyMap listed as new). Removed: claims about immediate values and the "swallowed exceptions" wording (source shows a warning).
Method: documentation only; no commands were run.
