---
id: computing-software.software-engineering.scala.sc-cats-typeclasses
name: sc-cats-typeclasses
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-cats, cats-typeclasses]
level: advanced
status: draft
description: "Use Cats type classes and syntax: Functor, Applicative, Monad, Semigroup, Monoid, traverse and validated."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Functor, Monad, Semigroup and Monoid with Cats
- `import cats.syntax.all.*`; `(a, b).mapN(f)` for Applicative composition, `list.traverse(f)` flips `List[F[A]]` to `F[List[A]]`.
- `Semigroup[A].combine`, `Monoid[A].empty`; `|+|` syntax combines; `foldMap` folds with a monoid.
- `Validated`/`ValidatedNel` accumulates errors, whereas `Either` stops at the first.
- Monad transformers (`EitherT`, `OptionT`) stack effects but add complexity.
Verify: law-check custom instances with cats-laws and discipline.
