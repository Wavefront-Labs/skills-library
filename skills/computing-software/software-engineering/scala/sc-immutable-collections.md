---
id: computing-software.software-engineering.scala.sc-immutable-collections
name: sc-immutable-collections
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-collections, immutable-collections]
level: practitioner
status: docs-checked
description: "Pick List, Vector, ArraySeq, Map and Set and know their performance characteristics."
sources: ["https://docs.scala-lang.org/overviews/collections-2.13/concrete-immutable-collection-classes.html", "https://docs.scala-lang.org/overviews/collections-2.13/concrete-mutable-collection-classes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List, Vector, Map, Set and choosing between them
- `List` is a finite immutable linked list: access, add and remove at the head take constant time, later elements take time linear in the depth.
- `Vector` reads and functionally updates elements at arbitrary positions in effectively constant time (a larger constant than List head access); it is the default immutable indexed sequence.
- Default immutable `Set` and `Map` are hash tries (CHAMP encoding); sets and maps of one to four elements are stored as single small objects.
- `TreeSet` and `TreeMap` use a red-black tree internally. `ListMap` is a linked list of pairs with linear operations and little use because standard maps are almost always faster; `VectorMap` keeps insertion order.
- Mutable hash maps and sets have no guaranteed iteration order; a linked hash map or set iterates in insertion order.
Verify: the concrete type shows in the REPL output.

## Checked

Date: 2026-11-02. Confirmed on the Scala 2.13 collections pages (concrete immutable and mutable collection classes). Removed as not confirmed: Seq being immutable.Seq in 2.13 and Scala 3, 'import the package not the type' advice, 'ListMap and SortedMap keep order' (replaced by the documented behaviour), `xs.getClass` check.

Method: documentation only; no commands were run.
