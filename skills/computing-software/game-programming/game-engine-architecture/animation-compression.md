---
id: computing-software.game-programming.game-engine-architecture.animation-compression
name: animation-compression
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, animation-compression, skeletal-animation, acl, game-programming]
level: practitioner
status: docs-checked
description: "Compress skeletal animation: constant tracks, range reduction, quantisation, segmenting, error measured by simulated skinning, and integrating the Animation Compression Library."
sources: ["https://github.com/nfrechette/acl", "https://nfrechette.github.io/2016/10/21/anim_compression_toc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animation compression

**Goal:** keep animation memory and sampling time down without compromising visible accuracy. The
ACL README states why: the more memory a clip consumes, the slower it is to sample and extract a
pose at runtime, and high ratios plus fast decompression without losing accuracy "requires a great
deal of care".

## Topic map (Nicholas Frechette's Animation Compression series)
The series table of contents is the reference for the techniques below; read the named post before
implementing one.
- **Measuring compression accuracy**, **simulating mesh skinning** and **dominance based error
  estimation**: measure error as the effect on skinned geometry, not as a per-track numeric
  difference.
- **Constant tracks**: tracks that never change need not be stored per frame.
- **Range reduction** and **simple / advanced quantization**: normalise a track to its range, then
  store fewer bits.
- **Uniform segmenting**: split a clip into segments (ACL uses this).
- **Main compression families**: sub-sampling, linear sample reduction (with four posts on its
  pitfalls), curve fitting, signal processing, and error compensation.
- **Bind pose optimizations** (additive, stripping), **clip metadata packing**, **morph target
  compression**, **progressive streaming**, **compressing looping animations**, and **manipulating
  the sampling time**.
- Case studies cover Unreal 4 and Unity 5, plus the GDC 2017 presentation.

## Animation Compression Library (ACL)
- Goals per its README: production-ready state-of-the-art algorithms, easy engine integration, a
  benchmark for comparing techniques, and documenting what works. Priorities in order: minimise
  compression artefacts (cinematographic quality), fast decompression on all supported hardware,
  then small memory footprint. "Decompression speed will not be sacrificed for a smaller memory
  footprint nor will accuracy be compromised."
- 100% C++11 header files; all allocations go through a game-provided allocator and all asserts
  through a game-provided macro; an intermediary clip format helps debugging and bug reports.
- MIT licence. Conan package `nfrechette-acl`. Runs anywhere C++11 or later is supported; CI covers
  Windows, Linux, macOS and Emscripten, and releases are manually tested on iOS and Android.
- Unreal Engine support is through an ACL plugin, which the README says is distributed with the
  engine releases.
- The README links performance metrics (Carnegie-Mellon and Paragon databases, a Matinee fight
  scene, decompression performance) and integration instructions in the docs folder: use those
  for settings such as error thresholds rather than guessing values.

## Verify
- Report compression ratio, maximum error and decompression time per clip on your own content.
- Visually check the worst-error clips (fingertips, foot sliding).

## Checked

Date 2026-11-08. Pages: the ACL GitHub README and the Animation Compression table of contents (blog). Confirmed: library goals and priorities, header-only C++11, allocator and assert hooks, MIT licence, platforms, Unreal plugin statement, and the list of technique posts. Removed as not stated on these pages: byte-per-bone arithmetic and 360 KB example, quaternion W-drop and smallest-three advice, example precision and shell-distance values, the UE5.3 default codec claim, and the root-motion, additive and facial pitfalls.

Method: docs-only read of cited pages, 2026-11-08
