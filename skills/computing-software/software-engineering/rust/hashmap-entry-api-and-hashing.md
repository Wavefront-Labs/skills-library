---
id: computing-software.software-engineering.rust.hashmap-entry-api-and-hashing
name: hashmap-entry-api-and-hashing
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-collections-strings, rust-hashmap-entry, hashmap, entry-api, hasher]
level: practitioner
status: docs-checked
description: "Use HashMap's entry API, custom keys with Hash and Eq, and know the default hasher, iteration-order and HashDoS trade-offs."
sources:
  - https://doc.rust-lang.org/std/collections/struct.HashMap.html
  - https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html
  - https://doc.rust-lang.org/std/hash/trait.Hash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HashMap, entry API and hashing

**Goal:** one lookup per update, correct keys, and an informed choice of hasher.

Patterns from the `HashMap` documentation:

```rust
use std::collections::HashMap;
let mut player_stats: HashMap<&str, u32> = HashMap::new();
player_stats.entry("health").or_insert(100);                    // insert if absent
player_stats.entry("defence").or_insert_with(random_stat_buff); // lazily computed default
let stat = player_stats.entry("attack").or_insert(100);         // &mut V
*stat += random_stat_buff();
player_stats.entry("mana").and_modify(|mana| *mana += 200).or_insert(100);
```

`entry` returns the `Entry` enum (`Occupied` / `Vacant`) so you can update or insert with one hash lookup.

## Keys
Keys must implement `Eq` and `Hash`; deriving `#[derive(PartialEq, Eq, Hash)]` is the easy route. If you implement them by hand, `k1 == k2` must imply `hash(k1) == hash(k2)`. It is a logic error to modify a key so that its hash or equality changes while it is in the map (possible only through `Cell`, `RefCell`, global state, I/O or unsafe code).

## Hasher
The default hashing algorithm is currently SipHash 1-3 (subject to change). It is competitive for medium-sized keys; other algorithms outperform it for small keys such as integers and large keys such as long strings, but typically do not protect against HashDoS. `HashMap` is randomly seeded per instance, so `HashMap::new` cannot be used in a `const` or `static` initializer (wrap in `LazyLock`, or use a fixed hasher, which is not HashDoS-resistant). Setting the hasher manually with `with_hasher` / `with_capacity_and_hasher` can expose a DoS attack vector.

## Gotchas
- Iteration order is arbitrary; sort, or use an ordered map, when output order matters.
- Do not test against hard-coded hash values; the `Hash` docs say tests should check consistency with `Eq`.

## Checked
2026-11-03. Confirmed against the `HashMap` struct page (entry examples, key requirements, SipHash 1-3, HashDoS note, random seeding, `with_hasher` warning, arbitrary iteration order) and the `Hash` trait page (Hash/Eq property, hard-coded hash values). Removed: `ordered-float`, `rustc-hash`/`FxHashMap`, `ahash`, `IndexMap`, `raw_entry`/hashbrown `entry_ref`, the contains_key anti-pattern and `Borrow`-lookup claims, the cargo bench advice.
Method: documentation only; no commands were run.
