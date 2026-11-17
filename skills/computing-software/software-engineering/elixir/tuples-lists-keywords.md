---
id: computing-software.software-engineering.elixir.tuples-lists-keywords
name: tuples-lists-keywords
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, tuple, list, keyword-list, hd, tl, length, linked-list, collection-literals]
level: intro
status: docs-checked
description: "Tuples are fixed-size contiguous, lists are linked lists, keyword lists are lists of {atom, value} pairs; pick by access pattern and complexity."
sources: ["https://hexdocs.pm/elixir/basic-types.html", "https://hexdocs.pm/elixir/List.html", "https://hexdocs.pm/elixir/Keyword.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuples, lists and keyword lists

**Goal:** choose between tuple, list and keyword list, following the Elixir lists, tuples and keyword guides.

```elixir
t = {:ok, "hello"}
elem(t, 1)               #=> "hello"   (index starts at zero; fast)
put_elem(t, 1, "world")  # returns a new tuple
tuple_size(t)            #=> 2         (constant time)

list = [1, 2, 3]
[0] ++ list              # fast: traverses only the left list
list ++ [4]              # slower: cost depends on the left-hand list
length(list)             # linear
[head | tail] = list     # head hd/1, tail tl/1

kw = [parts: 3, trim: true]   # same as [{:parts, 3}, {:trim, true}]
kw[:parts]                    # Access syntax: value of the first matching key
String.split("a b", " ", trim: true)   # last-argument brackets can be dropped
```

## Rules
- Lists are linked lists: `length/1` is linear and concatenation cost depends on the left-hand list. Tuples are stored contiguously: size and index access are fast, updating or adding elements copies the tuple structure (elements themselves are shared).
- Use lists when the number of elements varies (`String.split/1`), tuples when the size is fixed (`File.read/1` returns `{:ok, contents}` or `{:error, reason}`). There is no built-in index access for lists apart from the head.
- Keyword lists are lists of two-item tuples with atom keys; they are mostly used to pass optional arguments. Keys must be atoms, are ordered as written, and can be given more than once.
- Do not pattern match on keyword lists (it requires the same number of items and the same order); use the `Keyword` module, remembering keyword lists have linear performance. For associative data use maps.
- A function named `size` runs in constant time (`tuple_size/1`, `byte_size/1`); `length` is linear (`length/1`, `String.length/1`).

## Self-check
Why is `[0] ++ list` fast and `list ++ [4]` slower? The cost depends on the length of the left-hand list.

## Checked
Date: 2026-11-02. Confirmed against the Elixir lists-and-tuples and keywords-and-maps guides (elem, put_elem, tuple_size, ++ cost, length linear, keyword list properties, Access, last-argument brackets, size vs length). Removed: Keyword.get/fetch!, List.keyfind, Enum.at O(n) and reverse advice, failure-mode list, O(1) wording for prepend as a Big-O claim.
Method: documentation only; no commands were run.
