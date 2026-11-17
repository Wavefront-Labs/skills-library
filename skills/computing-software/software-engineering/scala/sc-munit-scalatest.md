---
id: computing-software.software-engineering.scala.sc-munit-scalatest
name: sc-munit-scalatest
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-testing, munit-scalatest]
level: practitioner
status: draft
description: "Write tests with MUnit or ScalaTest, assert equality on collections and add ScalaCheck properties."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MUnit, ScalaTest and property-based testing
- MUnit: `class MySuite extends munit.FunSuite { test("name") { assertEquals(f(1), 2) } }`; `FunFixtures` for setup; `munit-scalacheck` for properties.
- ScalaTest styles: `AnyFunSuite`, `AnyFlatSpec`, `AnyWordSpec`; matchers `result shouldBe 2`.
- ScalaCheck: `forAll { (a: Int, b: Int) => a + b == b + a }` explores random inputs and shrinks failures.
- Futures: MUnit returns `Future` from a test; ScalaTest has `AsyncFunSuite`.
- Run a single suite with `sbt "testOnly com.acme.MySuite"`.
Verify: break the code and confirm shrinking prints a minimal counterexample.
