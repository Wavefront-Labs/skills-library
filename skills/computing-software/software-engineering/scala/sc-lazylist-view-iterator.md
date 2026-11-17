---
id: computing-software.software-engineering.scala.sc-lazylist-view-iterator
name: sc-lazylist-view-iterator
category: computing-software
field: software-engineering
product: scala
tags: [scala, lazylist-view-iterator]
level: advanced
status: docs-checked
description: "Avoid intermediate collections with view, Iterator and LazyList, and know their memoization pitfalls."
sources: ["https://docs.scala-lang.org/overviews/collections-2.13/concrete-immutable-collection-classes.html", "https://docs.scala-lang.org/overviews/collections-2.13/views.html", "https://docs.scala-lang.org/overviews/collections-2.13/iterators.html", "https://docs.scala-lang.org/overviews/core/collections-migration-213.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy collections
- A view records transformations such as `map` and applies them only when the view is forced; strict collections are the default.
- An `Iterator` is not a collection: after `foreach` or `map` it is at its end, so calling `next` again fails with `NoSuchElementException`.
- `LazyList` computes its elements lazily, only those requested, so it can be infinitely long; otherwise it has the performance of a list.
- In 2.13 `immutable.Stream` (strict head, lazy tail) is deprecated in favour of `LazyList`.
Verify: a `LazyList` created with `#::` prints `<not computed>` until elements are forced.

## Checked

Date: 2026-11-02. Confirmed on the Scala 2.13 pages for views, iterators, concrete immutable collection classes (LazyList) and the 2.13 collections migration guide (Stream deprecated). Removed as not confirmed: memoisation and head-retention memory-leak remark, `.force` on LazyList, the `LazyList.from(1)` example.

Method: documentation only; no commands were run.
