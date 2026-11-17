---
id: computing-software.game-programming.game-engine-architecture.automated-gameplay-tests-and-bots
name: automated-gameplay-tests-and-bots
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, gameplay-test-automation, test-bots, automated-testing, game-programming]
level: practitioner
status: draft
description: "Automate gameplay testing: functional tests in levels, scripted and AI bots that play, smoke tests on builds, screenshot comparison and flake control."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine", "https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated gameplay tests and bots

**Goal:** builds that are known to boot, load every level, and let a player reach the end, checked
automatically.

## Test layers
1. **Unit tests:** pure logic (damage formulas, inventory) with no engine loop.
2. **Functional tests in levels:** small test maps that spawn a scenario and assert outcomes
   (Unreal Functional Testing actors `AFunctionalTest` with `FinishTest(Succeeded)`; Unity Test
   Framework `[UnityTest]` coroutines in Play Mode).
3. **Smoke tests:** boot the packaged build, load each level, run N seconds, check no errors/asserts,
   memory under budget, frame time under budget.
4. **Bots:** scripted or AI-driven players that traverse levels, complete objectives, and exercise
   menus.

## Bots
- **Waypoint/navmesh bots:** follow navmesh paths to objectives; detect stuck (no progress for T seconds) and report position for a heatmap of stuck spots.
- **Input-level bots:** drive the same input layer as a player so the real controller code is exercised.
- **Record/replay:** record a human playthrough as inputs and replay on new builds (needs
  determinism or tolerance checkpoints).
- **Exploration bots** randomly interact to find crashes (monkey testing).

## Screenshot comparison
Render fixed camera views with fixed seeds and compare against goldens with a perceptual tolerance;
flag diffs for review rather than auto-failing on tiny GPU differences.

## Flake control
Fixed timestep, fixed seeds, disable non-deterministic systems (dynamic resolution, streaming
timeouts) in test mode; retry once and track flaky tests separately.

## CI
Nightly: full level sweep + bot playthroughs on target hardware; per-commit: unit + fast functional tests.

## Verify
- Break a door trigger deliberately; the bot run reports the blocked objective with location.
