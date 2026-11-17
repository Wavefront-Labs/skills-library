---
id: creative-arts.film-live-action.davinci-resolve.fusion-3d-scenes-and-particles
name: fusion-3d-scenes-and-particles
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, fusion-3d, fusion-particles, fusion-camera-3d, merge3d, renderer3d, camera-tracker, pemitter, image-plane-3d, fbx-import]
level: practitioner
status: draft
description: "Build 3D in Fusion: Merge3D and Renderer3D, cameras and image planes, importing FBX/camera-track data, lights and shading, and particle systems (pEmitter to pRender)."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/Fusion_Reference_Manual.pdf (Fusion Reference Manual - 3D and Particle tools)"
  - "The Visual Effects Guide to DaVinci Resolve / Fusion (Blackmagic official training)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fusion 3D scenes and particles

**Goal:** composite 3D elements, set extensions and particle effects into live-action
plates inside Resolve's Fusion page.

## 1. The 3D pipeline
`3D objects (Shape3D, ImagePlane3D, FBXMesh3D, Text3D) -> Merge3D <- Camera3D, Lights
-> Renderer3D -> 2D Merge over the plate (MediaIn)`.
- **Merge3D** combines objects, cameras and lights into a scene.
- **Renderer3D** turns the scene into a 2D image: Software renderer (shadows, more
  accurate) or OpenGL (faster; good preview, supports some features differently).
- Output aspect/resolution of the renderer must match the plate.

## 2. Cameras and tracking
- **Camera3D**: set focal length and film back (aperture) to match the real camera's lens
  and sensor - otherwise perspective won't match.
- **Camera Tracker** (Studio): solve a moving plate -> *Export* creates a Camera3D,
  point cloud and ground plane in a Merge3D; place objects on the point cloud.
- Import camera solves from other trackers (FBX/ Alembic) via FBXMesh3D/ Alembic import.

## 3. Image planes and set extensions
**ImagePlane3D** carries a 2D image (matte painting, sign) into 3D space - position it
in depth so parallax works with the tracked camera. Use **Projection** (Camera3D
projection mode) to project a painting through a camera onto geometry for 2.5D moves.

## 4. Lights and shading
AmbientLight, DirectionalLight, PointLight, SpotLight; enable Lighting and Shadows on
the Renderer3D (software). Materials: Blinn, Phong, Cook-Torrance; Texture2D maps.
Match light direction to the plate.

## 5. Particles
`pEmitter -> (pDirectionalForce, pTurbulence, pBounce, pKill...) -> pRender -> Merge`
- pEmitter: number/rate, lifespan, velocity, style (point, blob, bitmap from an image).
- Forces shape motion; pRender outputs 2D or 3D (into Merge3D for camera-tracked
  particles).
- Uses: dust, sparks, snow, smoke elements (bitmap style), magic.
Cache/render-in-place heavy particle comps.

## 6. Performance
Use proxy mode and lower viewer quality while building; **Render in Place** or cache
to disk for playback in Edit; check Fusion memory settings in Preferences.

## Gotchas
- Camera3D focal length/sensor not matching the plate.
- OpenGL renderer in final when shadows are needed.
- Particle comps that slow the timeline to a crawl - cache them.
- Renderer resolution mismatched with the plate.

## Verify
- [ ] Camera matches lens/sensor or comes from a solve.
- [ ] Image planes/geometry sit correctly with parallax.
- [ ] Lighting direction matches the plate; renderer chosen deliberately.
- [ ] Particles and 3D cached for playback; output resolution correct.
