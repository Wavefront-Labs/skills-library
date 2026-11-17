---
id: computing-software.software-engineering.cpp.choosing-containers-and-iterator-invalidation
name: choosing-containers-and-iterator-invalidation
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, stl-containers, iterator-invalidation, vector, unordered-map, flat-map, data-structures, performance, cpp-containers-deep]
level: practitioner
status: gated
description: "Pick the right C++ standard container (vector by default, flat_map, unordered_map, deque, list) and avoid iterator/reference invalidation bugs on insert and erase."
sources: ["https://en.cppreference.com/w/cpp/container", "https://en.cppreference.com/w/cpp/container#Iterator_invalidation", "https://en.cppreference.com/w/cpp/container/flat_map", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rsl-arrays"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Choosing containers and iterator invalidation

**Goal:** fast, predictable data structures, and no use-after-invalidate crashes when containers
change during iteration.

## Default: std::vector
Contiguous memory beats asymptotics for most sizes because of cache locality. Use vector unless
you have a measured reason not to (the C++ Core Guidelines' container rules; rule number: gated: unconfirmed, source is paywalled or blocked). Sorted vector + `std::lower_bound`
often beats `std::map` for lookups on data that changes rarely.

| Need | Container |
|---|---|
| fixed size known at compile time | `std::array` |
| sequence, append at end | `std::vector` (`reserve` when size known) |
| push/pop both ends | `std::deque` |
| key lookup, no order needed | `std::unordered_map` (or absl::flat_hash_map / boost::unordered_flat_map for speed) |
| ordered keys, range queries | `std::map` / `std::set` |
| ordered, read-mostly, small to medium | `std::flat_map` / `flat_set` (C++23), or sorted vector |
| stable addresses + frequent middle insert/erase with iterators held | `std::list` (rarely the right answer) |
| priority queue | `std::priority_queue` |
| small-size optimisation | `boost::container::small_vector`, `absl::InlinedVector` |
| contiguous view without ownership | `std::span` |

## Invalidation rules (memorise the vector row)
| Container | Insert | Erase |
|---|---|---|
| `vector` | if reallocation (size > capacity): **all** invalidated; else at/after insert point | at/after erase point |
| `deque` | middle: all iterators and references; at either end: iterators invalidated, references stay valid | middle: all; at an end: only erased elements (but erasing the last element also invalidates the past-the-end iterator) |
| `list`, `map`, `set` | none | only erased elements |
| `unordered_*` | if rehash: all iterators (references stay valid); else none | only erased |
| `flat_map` | cppreference marks its invalidation rules as incomplete; assume like vector (gated: unconfirmed, source is paywalled or blocked) | assume like vector |

## Safe patterns
```cpp
// erase while iterating: use the returned iterator
for (auto it = v.begin(); it != v.end(); ) {
    if (bad(*it)) it = v.erase(it); else ++it;
}
// better (C++20): one pass, O(n)
std::erase_if(v, bad);           // C++20, linear; returns the number erased. Other containers have overloads too (check each container's page)
// pre-C++20 erase-remove idiom
v.erase(std::remove_if(v.begin(), v.end(), bad), v.end());
```
- Never keep a pointer/reference/iterator into a vector across `push_back` unless you
  `reserve`d enough first. Store indices instead.
- `for (auto& x : v) v.push_back(..)` is undefined behaviour.
- Map iteration with erase: `it = m.erase(it)`.

## Performance notes
- `emplace_back` constructs in place; `push_back(std::move(x))` is equivalent for existing objects.
- `reserve` avoids repeated reallocations; `shrink_to_fit` is a non-binding request.
- `unordered_map` allocates a node per element; open-addressing tables are usually faster (measure; no figure from the docs). `reserve(n)` avoids rehashes. Bad hash functions degrade lookups. `operator[]` on an unordered_map counts as an insertion for invalidation.
- `std::map::operator[]` inserts default values on lookup; use `find`, `contains` (C++20) (gated: unconfirmed, source is paywalled or blocked), `at`.
- `try_emplace` / `insert_or_assign` avoid constructing values unnecessarily.

## Detection
Debug iterators catch invalidation at runtime: libstdc++ debug mode, libc++ hardening/debug mode and MSVC's iterator debugging (macro names and ABI caveats: see each vendor's docs) (gated: unconfirmed, source is paywalled or blocked). ASan finds use-after-free from reallocation.

## Verify
- [ ] Container choice justified by access pattern; benchmark when deviating from vector.
- [ ] Tests pass under debug iterators / ASan.
- [ ] No iterators held across mutating calls (review loops that insert/erase).

## Checked

2026-11-02. Checked against cppreference: the container page iterator invalidation table (vector, deque incl. last-element erase note, list, associative, unordered with rehash, flat containers marked incomplete; flat_map is C++23) and vector erase_if (C++20, linear, returns count). Fixed: deque rows made precise, unsupported 2-5x speed figure removed, erase_if container list softened. Gated: Core Guidelines rule number, flat_map invalidation, `contains`, debug macro names.

Method: documentation only; no commands were run.
