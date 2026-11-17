---
id: creative-arts.animation.motion-graphics.ae-lights-and-shadows
name: ae-lights-and-shadows
category: creative-arts
field: animation
product: motion-graphics
tags: [ae-lights, lights, shadows, after-effects, 3d-layers, material-options, falloff]
level: practitioner
status: draft
description: "Light 3D layers in After Effects: light types, intensity and colour, cone and falloff, casting and accepting shadows via Material Options, and renderer notes."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lights and shadows (After Effects)

Lights affect **3D layers** only; 2D layers ignore them. Create with Layer > New > Light.

## Light types
- **Parallel**: directional light, like the sun; parallel rays, no falloff.
- **Spot**: cone of light with **Cone Angle** and **Cone Feather**.
- **Point**: omnidirectional from a point, like a bare bulb.
- **Ambient**: uniform light with no direction or shadows.

## Light options
- **Intensity**, **Color**.
- **Falloff** (Spot and Point): None, Smooth, or Inverse Square Clamped, with **Radius** and **Falloff Distance** controlling the range.
- **Casts Shadows**, **Shadow Darkness**, **Shadow Diffusion** (soft shadow edges).

## Layer Material Options
Each 3D layer has Material Options to control how it responds:
- **Casts Shadows**: On, Off or Only.
- **Light Transmission** for translucent look.
- **Accepts Shadows** and **Accepts Lights**.
- **Ambient**, **Diffuse**, **Specular**, **Shininess**, **Metal**: reflectance components.

## Shadows
- A light must have **Casts Shadows** on, and layers must cast and accept shadows. With the Classic 3D renderer, a shadow is cast onto layers behind the casting layer from the light's direction.
- Increase **Shadow Diffusion** to soften, and set darkness below 100% so shadows are not pure black.
- A **three-point lighting** set-up (key, fill, rim) works with spot or point lights plus a dim ambient.

## Renderers
The available 3D renderers differ across After Effects versions (Classic 3D is the long-standing one); check the Composition Settings > 3D Renderer list and Adobe's release notes for what your version provides (`ae-3d-layers-renderers.md`).

## Tips
- Use a **null** to aim and control lights (`ae-parenting-and-null-objects.md`), or Point of Interest for spot and parallel lights.
- Use low ambient and one key for readable direction; avoid many overlapping lights that wash the contrast out.

## Verify
- [ ] Layers are 3D and Accepts Lights is on.
- [ ] Shadows appear with the expected direction and softness.
