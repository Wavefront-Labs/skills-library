---
id: computing-software.software-engineering.ruby.ruby-hash-defaults
name: ruby-hash-defaults
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-collections, hash-defaults]
level: practitioner
status: docs-checked
description: "Use Hash.new with block vs value correctly and know insertion ordering and mutation rules."
sources: ["https://docs.ruby-lang.org/en/master/Hash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash defaults ordering and iteration
- A Hash returns its default for a missing key: either a `default` value or a `default_proc` (set with `Hash.new { |hash, key| ... }`); the proc may modify the hash but that is not thread-safe.
- Entries are presented in the order they were created (each, keys, values, shift, inspect).
- `compare_by_identity` makes keys equal only if they are the same object; `transform_values`, `slice`, `except` and `merge` (with a block for conflicts) are documented; an unfrozen String key is replaced by a duplicated, frozen String.
- Modifying a key while it is in use damages the hash's index.
Verify: write a regression test for your default-handling choice.

## Checked
2026-11-02. Confirmed against: Hash page: defaults, entry order, compare_by_identity, string keys, method list. Removed or softened (not stated on those pages): shared-array example, add-during-iteration RuntimeError, version tag for except.
Method: documentation only; no commands were run.
