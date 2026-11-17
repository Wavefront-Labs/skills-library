---
id: computing-software.software-engineering.scala.sc-classtag-typetag
name: sc-classtag-typetag
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-reflection-types, classtag-typetag]
level: advanced
status: docs-checked
description: "Work around erasure with ClassTag and know the Scala 3 alternatives to TypeTag."
sources: ["https://docs.scala-lang.org/scala3/guides/migration/preparing.html", "https://docs.scala-lang.org/overviews/collections/arrays.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClassTag, type erasure and reflection
- Creating an `Array[T]` for a generic `T` needs a runtime hint: a `ClassTag[T]`, passed implicitly or demanded with a context bound (`def evenElems[T: ClassTag](xs: Vector[T]): Array[T]`).
- For Scala 3 migration, code using `scala-reflect` such as `TypeTag` is replaced by `ClassTag`, Java reflection, or izumi-reflect (which also works on Scala 2.13).
Verify: an Array-creating generic method fails to compile without the ClassTag.

## Checked

Date: 2026-11-02. Confirmed on the Collections Arrays page (ClassTag hint for generic arrays) and the migration Preparing page (TypeTag replacements). Removed as not confirmed: the erasure examples, 'Scala 3 has no TypeTag' wording, Mirror/macro alternatives, classOf remark.

Method: documentation only; no commands were run.
