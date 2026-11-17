---
id: computing-software.game-programming.unity.unity-mathematics-burst-friendly-math
name: unity-mathematics-burst-friendly-math
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-mathematics, burst, simd, float3, dots, game-programming]
level: practitioner
status: draft
description: "Write Burst-friendly math with Unity.Mathematics: float3/quaternion/float4x4 types, math functions, swizzles, Random struct and converting from Vector3 and Mathf safely."
sources: ["https://docs.unity3d.com/Packages/com.unity.mathematics@1.3/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.mathematics@1.3/api/Unity.Mathematics.math.html", "https://docs.unity3d.com/Packages/com.unity.burst@1.8/manual/csharp-burst-intrinsics.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unity.Mathematics

**Goal:** math code that Burst vectorises and that behaves like shader math.

## Types and conventions
- `float2/3/4`, `int3`, `bool4`, `float3x3`, `float4x4`, `quaternion` (lowercase), HLSL-style.
- Operators are component-wise: `a * b` on float3 is per-component, matrix product is `math.mul(m, v)`.
- Swizzles: `v.xz`, `v.zyx`, `p.xyz = 0`.
- Static `math` functions: `math.length`, `normalize`, `normalizesafe`, `dot`, `cross`, `lerp`,
  `clamp`, `saturate`, `select(a, b, cond)` (branchless), `any`, `all`, `radians`, `sincos`.
- Rotations: `quaternion.Euler(radians)`, `quaternion.LookRotationSafe(fwd, up)`, `math.rotate(q, v)`,
  `math.mul(q1, q2)`. Angles in **radians**, unlike Unity's Quaternion.Euler degrees.

## Interop
`float3` and `Vector3` convert implicitly both ways; `quaternion` and `Quaternion` too. Conversion is
free but keep jobs on Mathematics types throughout.

## Random in jobs
```csharp
var rng = Unity.Mathematics.Random.CreateFromIndex((uint)index);   // per-entity deterministic seed
float3 dir = rng.NextFloat3Direction();
```
`Random` is a struct: copy it back after use or every call repeats values. Seed 0 is invalid.

## Burst-friendly habits
- Prefer `math.select` and `math.min/max` over branches in inner loops.
- Struct-of-arrays data (`NativeArray<float3>`) vectorises better than arrays of big structs.
- Avoid `math.normalize` on zero vectors (NaN); use `normalizesafe`.
- Use `math.distancesq` for comparisons.

## Gotchas
- Integer division by zero and float NaN propagate silently in Burst; `Unity.Burst.CompilerServices`
  hints and safety checks in editor help.
- `Mathf.Approximately` has no direct twin; compare with an epsilon.
- `float4x4.TRS(pos, rot, scale)` for transforms; column-major like HLSL.

## Verify
- [ ] Burst Inspector shows packed SIMD instructions (`vmulps`, `vaddps`) in hot loops.
- [ ] Unit tests compare results against the Vector3/Quaternion reference for sample inputs.
