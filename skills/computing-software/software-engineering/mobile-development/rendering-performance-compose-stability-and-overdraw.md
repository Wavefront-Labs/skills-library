---
id: computing-software.software-engineering.mobile-development.rendering-performance-compose-stability-and-overdraw
name: rendering-performance-compose-stability-and-overdraw
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, compose-stability, overdraw, recomposition, strong-skipping, jetpack-compose, swiftui-performance, rendering, jank]
level: advanced
status: docs-checked
description: "Fix Android rendering cost: Compose stability, strong skipping, deferring state reads, release-mode configuration, GPU overdraw and transparency."
sources: ["https://developer.android.com/develop/ui/compose/performance", "https://developer.android.com/develop/ui/compose/performance/stability", "https://developer.android.com/develop/ui/compose/performance/stability/strongskipping", "https://developer.android.com/topic/performance/rendering/overdraw"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Rendering performance (Compose stability / overdraw)

**Goal:** keep each frame within its budget by doing less recomposition, layout and drawing.

## Configure first
- Run in release mode with R8 optimizing and shrinking; debug mode imposes a performance cost and hides other issues.
- Use Baseline Profiles. Compose ships a default profile, but an app-specific one is better.

## Compose best practices
The three phases are composition, layout and drawing.
- `remember` the results of expensive calculations; do not sort or filter in the composable body.
- Give lazy layouts stable `key` and `contentType` to minimise recomposition and enable slot reuse.
- Use `derivedStateOf` (or `computedStateOf` in Compose 1.13 and higher) to limit recomposition when reading rapidly
  changing state.
- Defer state reads as long as possible by wrapping them in lambdas, and prefer lambda modifiers such as
  `Modifier.offset { ... }` for frequently changing state.
- Never write to state that has already been read in a composable (backwards write).

## Stability and skipping
A type is stable if it is immutable or Compose can tell whether it changed between recompositions. Stable parameters
are compared with `equals()`; with strong skipping (default since Kotlin 2.0.20) unstable parameters are compared by
instance (`===`). Without strong skipping, a composable with unstable parameters always recomposes when its parent does.
- Strong skipping makes all restartable composables skippable and remembers every lambda inside a composable (keyed by
  its captures). Opt out with `@NonSkippableComposable` or `@DontMemoize`. Before Kotlin 2.0.20 enable it with
  `composeCompiler { enableStrongSkippingMode = true }`.
- A class with `var` properties is unstable: mutating it in place will not recompose, while a new instance with
  identical values will. Classes from modules where the Compose compiler does not run are unstable too.
- `List`, `Set` and `Map` are treated as unstable. Under strong skipping they still skip when the reference does not
  change. Be careful annotating models that hold collections with `@Stable`/`@Immutable` or swapping to immutable
  collections: element-by-element `equals()` can cost more than recomposing.
- Add `@Stable` or `@Immutable` only when the compiler cannot infer stability (for example non-Compose modules), new
  identical instances are allocated often, and `equals()` is cheap. A stability configuration file is the other option.
- Use the Compose compiler reports to see what stability is inferred for your classes.
- Allocating new instances of unstable parameters on every recomposition defeats instance equality.

## Overdraw and layout
Overdraw is the same pixel drawn more than once in a frame. Stacked content is drawn back to front.
- The Debug GPU Overdraw tool colour-codes how many times each pixel is drawn; Profile GPU Rendering shows per-stage
  frame time (the orange Process part signals buffer swaps and hints at overdraw). Profile GPU Rendering does not work
  with NDK apps.
- Remove backgrounds that are completely covered by what is drawn on top; set the window background to the main
  colour and leave containers above it without backgrounds. Use the Layout Inspector to find them.
- Reduce transparency (alpha rendering). Prefer an opaque colour such as `Color.Black.copy(alpha = 0.5f)` on the text
  over `Modifier.alpha(0.5f)`.
- Flattening the view hierarchy is not a performance requirement in Compose: the UI tree is laid out in a single pass
  however deeply nested.
- On low-end devices the page advises optimising UI-thread work first unless targeting a known weak GPU.

## Verify
- [ ] Hot composables are skipped when their inputs are unchanged.
- [ ] Overdraw checked with the Debug GPU Overdraw tool on main screens.

## Checked
2026-11-08. Confirmed against the Android Developers pages Jetpack Compose Performance, Stability in Compose, Strong skipping mode and Reduce overdraw: release/R8 and baseline profile advice, best-practice list, stability and strong-skipping rules, collections caveat, annotation trade-offs, overdraw tools and fixes. Removed: the SwiftUI section (Apple page returned 404), the code sample claiming per-phase read costs, `graphicsLayer` example, and the "Understand baseline profiles" aside.
Method: documentation only; no commands were run.
