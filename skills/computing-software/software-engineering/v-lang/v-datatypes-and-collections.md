---
id: computing-software.software-engineering.v-lang.v-datatypes-and-collections
name: v-datatypes-and-collections
category: computing-software
field: software-engineering
product: v-lang
tags: [v-datatypes-and-collections, standard-library-misc, datatypes, stack, queue, linked list, set, binary search tree, priority queue, ringbuffer, collections, v-lang]
level: practitioner
status: draft
description: "Use datatypes.Stack, Queue, LinkedList, Set and BST, and builtin maps and arrays for sets, ring buffers and priority queues."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# datatypes, sets and other collections

Goal: pick collection types beyond arrays and maps.

- `import datatypes`: `mut s := datatypes.Stack[int]{}` (`push`, `pop()!`, `peek()!`, `len()`), `datatypes.Queue[T]` (`push`, `pop()!`), `datatypes.LinkedList[T]`, `datatypes.DoublyLinkedList[T]`, `datatypes.Set[T]` (`add`, `exists`, `remove`, `union`, `intersection`), `datatypes.BSTree[T]`, `datatypes.MinHeap[T]` (priority queue), `datatypes.ListFixed`.
- Sets in plain V: `map[string]bool` or `map[string]struct{}`.
- Ring buffer: `import datatypes; datatypes.RingBuffer`/`sync` ring (confirm names).
- Deduplicate array: copy into a set then `keys()`.
- Pick by access pattern: random access array, FIFO queue, priority heap.

Gotchas:
- Generic collection modules are still evolving; API details (method names, result vs option returns) differ by version.
- Values are copied into containers; use references for shared mutation.

Verify: push 3 values, pop in LIFO order, assert.
