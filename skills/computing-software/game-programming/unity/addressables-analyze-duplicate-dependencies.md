---
id: computing-software.game-programming.unity.addressables-analyze-duplicate-dependencies
name: addressables-analyze-duplicate-dependencies
category: computing-software
field: game-programming
product: unity
tags: [unity, addressables, addressables-analyze, duplicate-dependencies, build-layout, game-programming]
level: practitioner
status: draft
description: "Use Addressables Analyze rules and the build layout report to find duplicated implicit dependencies, scene/bundle duplication and fix them with shared groups."
sources: ["https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/BuildLayoutReport.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Addressables Analyze and duplicate dependencies

**Goal:** no asset is silently copied into several bundles (bigger downloads, double memory, broken
singletons of shared ScriptableObjects).

## How duplication happens
An asset not marked addressable but referenced by entries in two bundles is an **implicit
dependency** and is copied into each bundle. Same for assets referenced by both built-in scenes and
addressables (copied into player and bundle).

## Analyze window (Window > Asset Management > Addressables > Analyze)
Rules:
- **Check Duplicate Bundle Dependencies** — implicit assets in more than one bundle. Fixable: moves
  them to a new group "Duplicate Asset Isolation".
- **Check Resources to Addressable Duplicate Dependencies** — assets in both Resources and bundles.
- **Check Scene to Addressable Duplicate Dependencies** — built-in scene and bundle duplicates.
- **Bundle Layout Preview** — what will be in each bundle.
Run, inspect, then "Fix Selected Rules" or move assets into a deliberately named shared group yourself
(better names, better grouping than the auto group).

## Build layout report
Enable Preferences > Addressables > Debug Build Layout; after a build, `Library/com.unity.addressables/
buildlayout` (JSON in 2.x, viewable in the Build Report Inspector / Addressables Report window) lists
bundle sizes, explicit and implicit assets, and "referenced by" chains.

## Fix patterns
- Shared materials/shaders/fonts/atlases -> one "Shared" group, Pack Together.
- Shaders: put all in one group to avoid variant duplication across bundles.
- Built-in scene duplicates: make that scene addressable too, keep only a tiny bootstrap scene built-in.

## Gotchas
- Duplicated ScriptableObjects become different instances per bundle — event channels or registries
  then "don't fire". Duplicate Analyze explains these bugs.
- Fixing duplicates after release alters bundle hashes -> content update downloads.
- Run Analyze in CI (`AnalyzeSystem.ComputeAnalysis`) and fail on new duplicates.

## Verify
- [ ] Duplicate rule reports zero issues.
- [ ] Total bundle size decreases; shared asset appears once in the layout report.
