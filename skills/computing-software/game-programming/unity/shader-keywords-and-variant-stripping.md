---
id: computing-software.game-programming.unity.shader-keywords-and-variant-stripping
name: shader-keywords-and-variant-stripping
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-urp, shader-variants, shader-keywords, variant-stripping, game-programming]
level: practitioner
status: docs-checked
description: "Control Unity shader variant explosion: multi_compile vs shader_feature, local keywords, IPreprocessShaders stripping, URP feature stripping and build logs."
sources: ["https://docs.unity3d.com/Manual/shader-variants.html", "https://docs.unity3d.com/Manual/shader-variant-stripping.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader keywords and variant stripping

**Goal:** build times, build size and runtime shader-load hitches under control.

## How variants multiply
- Unity compiles one set of variants per graphics API for the current build target.
- The variant count for a shader program is the product of its keyword sets: one variant per
  combination taking one element from each set. Two sets of two keywords give four variants; ten such
  sets give 1024 (combinatorial explosion).
- Many variants mean longer builds, larger files, more runtime memory, longer loading and compilation
  stutters. Unity deduplicates identical variants in a Pass, but they still cost compile time,
  memory and loading time, so strip what you do not need.
- Alternatives to keywords: shader constants (a `#define` guarded by `#ifndef`, overridden in the
  Shader Constant Defines list in Graphics settings or per build profile) fix a value at build time
  without variants.

## Stripping
- Edit > Project Settings > Graphics > Shader Build Settings: add a keyword set (space-separated,
  include `_` if present). Set Type Override to `shader_feature` or `dynamic_branch` to limit
  variants, or untick keywords to exclude their code. Build profiles have their own Shader Build
  Settings that override the Graphics window.
- Shader Stripping section of Graphics settings; for URP see Unity's "Reducing shader variants in
  URP"; for HDRP "Reduce shader variants in HDRP".
- Editor script stripping: `IPreprocessShaders.OnProcessShader` (called before a graphics shader Pass
  compiles into a build) and `IPreprocessComputeShaders.OnProcessComputeShader` for compute shaders.

## Avoid stripping what you use
If you strip a variant a Material needs at runtime, Unity tries a similar available variant instead,
which can look wrong. Enable strict shader variant matching to count variants honestly, add shaders to
Always Included Shaders in Graphics settings, and do not use a `shader_feature` keyword to switch code
branches at runtime.

## Verify
- [ ] Variant count (strict matching on) drops after changes; build size diff recorded.
- [ ] Test runtime-toggled keywords in a player build, on each target platform and quality level.

## Checked
2026-11-01. Confirmed against the Unity manual pages Introduction to shader variants and Reduce shader
variants: product-of-sets rule and the 4 and 1024 examples, costs, deduplication, shader constants,
Shader Build Settings and Type Override, build-profile override, the two Editor stripping callbacks,
fallback variant behaviour, Always Included Shaders, the shader_feature runtime caveat. Removed
unconfirmed claims: `_local`, `_vertex` and `_fragment` suffix behaviour, the 32-variant figure, log
message text, Unity 6 usage reports, GraphicsStateCollection and ShaderVariantCollection warmup, the
stripper code sample.
Method: documentation only; no commands were run.
