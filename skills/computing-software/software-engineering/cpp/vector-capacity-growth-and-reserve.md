---
id: computing-software.software-engineering.cpp.vector-capacity-growth-and-reserve
name: vector-capacity-growth-and-reserve
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-containers-deep, cpp-cd-reserve, vector-capacity-reserve, std-vector, reserve, shrink-to-fit, emplace-back, reallocation]
level: practitioner
status: docs-checked
description: "Control std::vector reallocation with reserve, understand invalidation, emplace_back and exception guarantees, and avoid misusing reserve."
sources: ["https://en.cppreference.com/w/cpp/container/vector/reserve", "https://en.cppreference.com/w/cpp/container/vector/emplace_back"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vector capacity, growth and reserve

`size()` is how many elements exist; `capacity()` is how many fit before reallocation. When an insertion would exceed capacity the vector reallocates and every iterator and reference to its elements is invalidated (cppreference, emplace_back and reserve).

```cpp
std::vector<int> v;
v.reserve(1000);                 // capacity >= 1000; size stays 0
for (int i = 0; i < 1000; ++i) v.push_back(i);        // no reallocation until size would exceed capacity

std::vector<int> w(1000);        // resize: creates 1000 value-initialised elements (size 1000)
std::vector<Item> items;
items.reserve(n);
items.emplace_back(id, name);    // constructs the element in place from the arguments

v.shrink_to_fit();               // reserve() cannot lower capacity; shrink_to_fit() is the tool for that
```

## Rules
- Reserve when the final size is known or estimable: after `reserve`, insertions do not trigger reallocation unless the size would exceed capacity.
- `reserve` does not change `size()`; do not index into reserved-but-unconstructed slots. If the new capacity is not greater than the current one it does nothing and invalidates nothing.
- If T's move constructor is not `noexcept` and T is not CopyInsertable, `reserve` and `emplace_back` use the throwing move constructor and the strong exception guarantee is waived: mark move constructors `noexcept`.
- Do not call `reserve` before every `push_back`: cppreference warns this makes capacity grow linearly instead of exponentially, with higher complexity. A function that appends to a caller's vector should usually not call `reserve` at all.
- To insert a range, prefer the range version of `insert`: it preserves correct capacity growth, unlike `reserve` followed by `push_back`s.

## Gotchas
- A reallocation invalidates all iterators (including `end()`) and all references to elements; without reallocation `emplace_back` invalidates only `end()`.
- `reserve` with a value above `max_size()` throws `std::length_error`; allocator failures (typically `std::bad_alloc`) propagate. On an exception `reserve` has no effect.
- `reserve` is at most linear in `size()`.

## Verify
- [ ] Count reallocations by watching `capacity()` changes in a loop, or with a counting allocator: expected 1 after reserve.

## Checked
2026-11-03. Confirmed on cppreference vector::reserve (semantics, invalidation, exceptions, complexity, Notes on misuse and range insert, shrink_to_fit) and vector::emplace_back (in-place construction, invalidation, noexcept move note). Removed: growth-factor numbers per standard library, the swap idiom, `clear()` capacity behaviour, `std::move_if_noexcept` wording, `append_range`, `vector<bool>`, deque and unique_ptr advice, the `resize` cost note and the benchmark check.
Method: documentation only; no commands were run.
