---
id: computing-software.computer-graphics-engineering.rendering-techniques.punctual-lights-and-physical-units
name: punctual-lights-and-physical-units
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, punctual-lights, light-falloff, physical-light-units, inverse-square, spot-light, lux]
level: practitioner
status: docs-checked
description: "Implement punctual lights with physical units: lumens/candela/lux conversions, inverse-square falloff with windowing, spot cone attenuation, and matching exposure to real values."
sources: ["https://github.com/google/filament/blob/main/docs/Filament.md.html", "https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_lights_punctual/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Punctual lights and physical light units

## 1. Units
| Light | Unit | Meaning |
|---|---|---|
| Directional (sun) | lux (lm/m^2) | illuminance at the surface; Filament's table gives about 100,000 lx for the sun alone at midday (about 120,000 lx with sky) |
| Point / spot | lumen (power) or candela (intensity, lm/sr) | |
| Area | lumen or nits (cd/m^2) | |

Conversions (Filament):
- Point: `I [cd] = Phi [lm] / (4 PI)`.
- Spot: `I = Phi / PI` (Filament decouples cone from intensity so changing the cone doesn't change
  brightness); physically `I = Phi / (2 PI (1 - cos(outer/2)))`.
- glTF `KHR_lights_punctual`: point/spot intensity in candela, directional in lux.

## 2. Falloff
Physical: `E = I / d^2`. Lights need a finite range for culling, so window the falloff to reach 0
smoothly at the influence radius (Karis 2013, as used in Filament):
```glsl
float distanceAttenuation(float d2, float invRange2) {
    float factor = d2 * invRange2;
    float smoothFactor = clamp(1.0 - factor * factor, 0.0, 1.0);
    return smoothFactor * smoothFactor / max(d2, 1e-4);      // 1e-4 = 1 cm light size clamp
}
```
glTF `KHR_lights_punctual` recommends `max(min(1 - (d/range)^4, 1), 0) / d^2` for point and spot lights with a `range`.

## 3. Spot cone
```glsl
float spotAttenuation(vec3 L, vec3 spotDir, float cosOuter, float cosInner) {
    float scale  = 1.0 / max(cosInner - cosOuter, 1e-4);
    float offset = -cosOuter * scale;
    float t = clamp(dot(-L, spotDir) * scale + offset, 0.0, 1.0);
    return t * t;
}
```
Precompute scale/offset on the CPU.

## 4. Evaluating
`Lout = BRDF(V, L) * I * attenuation * NoL` with `I` in candela (point/spot) or `E` in lux
(directional; no distance term). Combine with exposure (EV100) so real-world values produce correct
brightness.

## 5. Exposure
With physical units, a camera exposure is mandatory (see the camera exposure skill). Pre-expose light values on the CPU to keep fp16 in range.

## Gotchas
- Mixing artist "intensity 1-10" lights with physical sun values makes interiors black; convert
  everything.
- Point lights very close to surfaces blow out (1/d^2 -> inf); clamp minimum distance (light radius).

## Verify
- [ ] A 800 lm point light at 1 m gives ~64 lux on a perpendicular surface (800 / 4 PI cd, divided by 1 m^2).
- [ ] Light fades to exactly zero at its range (no hard cutoff ring).

## Checked

2026-10-26: Filament materials/lighting document (google/filament docs/Filament.md.html) and the glTF KHR_lights_punctual README, read 2026-10-26. Confirmed: photometric units table, point light I = Phi / (4 PI), spot light physical form and the decoupled I = Phi / PI form, the windowed inverse-square function with max(distanceSquare, 1e-4), the spot scale/offset angle attenuation code, sun and sky illuminance table, glTF candela for point and spot and lux for directional, and the glTF range attenuation recommendation. Removed the 60 W incandescent lumen figure, the overcast illuminance, the EV100 interior value and the IES normalisation advice, which neither document states.

Method: documentation only; no commands were run.
