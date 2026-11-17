---
id: computing-software.software-engineering.mobile-development.choosing-native-vs-cross-platform
name: choosing-native-vs-cross-platform
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, cross-platform-mobile, native-vs-cross-platform, react-native, flutter, kotlin-multiplatform, architecture-decision]
level: practitioner
status: draft
description: "Decide between native iOS/Android, React Native, Flutter, Kotlin Multiplatform or a PWA using team skills, platform integration, performance, UI fidelity and long-term cost."
sources:
  - https://reactnative.dev/docs/getting-started
  - https://docs.flutter.dev/resources/architectural-overview
  - https://kotlinlang.org/docs/multiplatform/kmp-overview.html
  - https://web.dev/explore/progressive-web-apps
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing native vs cross-platform

**Goal:** a technology choice for a mobile product that fits the team, the product's platform needs and its expected lifetime, recorded as an architecture decision.

## 1. The options
| Approach | Shares | UI | Strengths | Costs |
|---|---|---|---|---|
| Native (Swift/SwiftUI + Kotlin/Compose) | nothing (or backend-driven logic) | platform-native | best platform fidelity, day-one OS features, performance, tooling | two codebases and teams |
| Kotlin Multiplatform | logic (optionally UI via Compose MP) | native or Compose | native UI with shared business logic, incremental adoption | Kotlin skills needed, Swift interop rough edges |
| React Native | logic + UI (JS/TS) | native views via React | web/React skills reuse, OTA JS updates, large ecosystem | native module work for platform features, upgrade churn |
| Flutter | logic + UI (Dart) | own rendering engine | pixel-consistent custom UI, fast development, strong performance | Dart skills, non-native widgets need care, larger binary |
| PWA / web wrapper | everything | web | one web codebase, no store review for the PWA | weaker device APIs (iOS especially), store rejections for thin wrappers |

## 2. Decision drivers
1. **Team**: existing skills and hiring market (React/TS team -> React Native; strong native teams -> native or KMP).
2. **Platform integration depth**: heavy use of camera pipelines, AR, Bluetooth, background processing, widgets, watch/car extensions, or day-one OS features favours native or KMP.
3. **UI**: brand-driven custom UI identical on both -> Flutter; platform-idiomatic UI -> native/KMP/React Native.
4. **Performance**: graphics-heavy, real-time audio/video or games -> native or a game engine; typical business apps run well on any.
5. **Lifetime and cost**: multi-year products accumulate upgrade costs (framework major versions, native dependency compatibility); factor in maintenance, not just initial speed.
6. **Existing code**: an existing native app can adopt KMP or React Native/Flutter screens incrementally (add-to-app) rather than rewrite.
7. **Release model**: OTA JS updates (React Native/Expo) for fast fixes within store rules.

## 3. Evaluate with a spike
Build the riskiest screen or integration (e.g. offline sync + camera + push) in the top two candidates, time-boxed, on real low-end devices. Measure startup time, scrolling smoothness, binary size, and developer velocity; involve both platform experts.

## 4. Record the decision
Write an ADR: context, options considered, drivers and weights, decision, consequences (skills to hire, modules to build, exit strategy). Revisit when drivers change (team composition, new platform requirements).

## Gotchas
- "Write once" is never literal: plan 10-30% platform-specific work for navigation conventions, permissions, notifications, payments and accessibility.
- Rewrites to switch frameworks are expensive; prefer incremental migration paths (add-to-app, KMP modules).
- Hybrid approaches multiply build complexity (two package managers, two toolchains); keep the boundary clear.

## Verify
- The ADR lists measurable spike results for each finalist, and the chosen stack's riskiest integration works on the lowest-end target device before full commitment.
