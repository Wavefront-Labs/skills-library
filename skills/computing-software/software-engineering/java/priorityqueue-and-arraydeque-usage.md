---
id: computing-software.software-engineering.java.priorityqueue-and-arraydeque-usage
name: priorityqueue-and-arraydeque-usage
category: computing-software
field: software-engineering
product: java
tags: [java, java-collections, priorityqueue, arraydeque, stack-replacement, top-k, heap]
level: practitioner
status: docs-checked
description: "Pick ArrayDeque over Stack/LinkedList, use PriorityQueue for top-k and scheduling, and know its tie, iteration, remove(Object) and thread-safety behaviour."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/PriorityQueue.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Deque.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PriorityQueue and ArrayDeque

## ArrayDeque: the default stack and queue
```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.pop(); stack.peek();         // LIFO: push inserts at the front, pop removes the first element
Queue<Task> q = new ArrayDeque<>();                // Task is a placeholder
q.offer(t); q.poll();                              // FIFO; poll returns null when empty
```
- Resizable array with no capacity restriction. The Javadoc says it is likely to be faster than `Stack` when used as a stack and faster than `LinkedList` when used as a queue.
- Null elements are prohibited.
- Not thread-safe without external synchronisation. `Deque` lists `ConcurrentLinkedDeque` and `LinkedBlockingDeque` among its implementations.
- From Java 21 it implements `SequencedCollection` (`addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`).
- `Deque.pop` and `removeFirst` throw `NoSuchElementException` on an empty deque; `poll`/`peek` variants return `null`.

## PriorityQueue: heap-ordered, unbounded
```java
PriorityQueue<Integer> heap = new PriorityQueue<>();   // natural ordering; default initial capacity 11
heap.offer(5); Integer next = heap.poll();             // head is the least element
```
- Ordering is natural ordering or a `Comparator` given at construction. The head is the least element.
- Time costs (Javadoc implementation note): `offer`, `poll`, `remove()`, `add` are O(log n); `remove(Object)` and `contains` are linear; `peek`, `element`, `size` are constant.
- Top-k largest of a stream: keep a min-heap of size k; offer each value and `poll` whenever `size() > k`:
```java
PriorityQueue<Integer> top = new PriorityQueue<>(k);   // k must be at least 1
for (int x : data) { top.offer(x); if (top.size() > k) top.poll(); }
```

## Gotchas
- The iterator and spliterator are not guaranteed to traverse in any particular order. For ordered traversal drain with `poll()` or use `Arrays.sort(pq.toArray())` as the Javadoc suggests.
- No null elements. With natural ordering, non-comparable elements may cause `ClassCastException`.
- Ties for the least value are broken arbitrarily; add your own sequence number to the ordering if equal priorities must stay FIFO.
- Not synchronized: use `PriorityBlockingQueue` if several threads modify it.

## Verify
Test with equal priorities and compare the polled order to a sorted copy of the input.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for ArrayDeque, PriorityQueue and Deque: speed comparison, null prohibition, thread-safety, SequencedCollection, default capacity 11, complexities, unordered iteration, arbitrary tie-breaking, ClassCastException, PriorityBlockingQueue pointer, Deque null-versus-exception behaviour.
Removed (not in the pages read): the "Vector-based, synchronized legacy" description of Stack, the "lighter" claim, `thenComparing` comparator example, `TreeSet`/indexed-heap advice, the comparator subtraction overflow tip, and the DelayQueue suggestion.
Method: documentation only; no commands were run.
