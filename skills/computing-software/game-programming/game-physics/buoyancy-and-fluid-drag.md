---
id: computing-software.game-programming.game-physics.buoyancy-and-fluid-drag
name: buoyancy-and-fluid-drag
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, rigid-body, buoyancy, fluid-drag, floating-objects, archimedes, boats, game-programming]
level: practitioner
status: verified
description: "Simulate floating rigid bodies: sample-point buoyancy from submerged volume, applying forces at points for natural rolling, linear/quadratic water drag and wave height queries."
sources: ["https://www.gamedeveloper.com/programming/water-interaction-model-for-boats-in-video-games", "https://docs.unity3d.com/ScriptReference/Rigidbody.AddForceAtPosition.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buoyancy and fluid drag

## Physics
Archimedes (a 1 m cube at density ratio 0.25, 0.5, 0.75 settled with its centre 0.25 m above, level with and 0.25 m below
the surface in a 1D simulation, matching `0.5 - ratio`): upward force = fluid density x gravity x submerged volume (`F = rho * g * V_sub`), acting
at the centre of the submerged volume. Water `rho` ~ 1000 kg/m3. An object floats when its average
density is below the fluid's.

## Sample-point method (robust, cheap)
Place N points (4-16) over the hull/volume; each represents `V_total / N`.
```csharp
void FixedUpdate() {
    foreach (var p in points) {
        Vector3 wp = transform.TransformPoint(p);
        float depth = Water.HeightAt(wp.x, wp.z) - wp.y;      // >0 means under water
        if (depth <= 0) continue;
        float sub = Mathf.Clamp01(depth / pointHeight);       // partial submersion
        Vector3 buoy = Vector3.up * (waterDensity * -Physics.gravity.y * volumePerPoint * sub);
        rb.AddForceAtPosition(buoy, wp, ForceMode.Force);     // at the point: gives roll/pitch righting
        Vector3 v = rb.GetPointVelocity(wp);
        rb.AddForceAtPosition(-v * linearDrag * sub - v * v.magnitude * quadDrag * sub, wp);
    }
}
```
Forces at points make boats roll and self-right naturally; one central force can't.

## Drag
- Linear `-k v` is stable and good at low speed; quadratic `-c |v| v` is physically right at speed.
- Add angular drag in water (or raise `angularDamping` while submerged) to kill endless rocking.
- Separate drag per axis for hulls: high sideways drag, low forward drag gives a keel effect.

## Accurate method
Clip the hull mesh's triangles against the water surface each step; submerged triangles give
buoyancy (pressure on faces) plus pressure/viscous drag forces (the Kerner "Water interaction model
for boats" approach). Use a low-poly hull proxy; cost is per triangle.

## Waves
Query the **same** wave function the water shader uses (Gerstner sum) on the CPU, or read back a
displacement map at low resolution. Mismatch makes objects float above or sink into visible waves.

## Gotchas
- Too few points: jitter when points cross the surface; smooth with partial submersion (above) and more points.
- Very light objects with big volume explode upward: clamp per-point force or add damping.
- Fixed timestep matters; buoyancy is a spring and can oscillate at low rates.

## Verify
- [ ] Crates of different densities float at different heights and settle within a few seconds.
- [ ] A boat tilted 30 degrees rights itself; a capsized-by-design hull stays capsized.
