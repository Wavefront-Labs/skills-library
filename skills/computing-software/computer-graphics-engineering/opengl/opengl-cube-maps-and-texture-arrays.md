---
id: computing-software.computer-graphics-engineering.opengl.opengl-cube-maps-and-texture-arrays
name: opengl-cube-maps-and-texture-arrays
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, cubemaps, texture-arrays, gl-texture-cube-map, sampler2darray, seamless-cubemap]
level: practitioner
status: docs-checked
description: "Create and sample OpenGL cube maps and 2D texture arrays: immutable storage, face order, seamless filtering, layer uploads and array-indexed materials."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cube maps and texture arrays

**Goal:** use cube maps for environment/skybox/point-shadow lookups and 2D arrays for many
same-size textures behind one binding (terrain layers, material atlases without bleeding,
shadow cascades).

## 1. Cube map
```c
GLuint cube; glCreateTextures(GL_TEXTURE_CUBE_MAP, 1, &cube);
glTextureStorage2D(cube, mips, GL_RGBA16F, size, size);          // square faces
for (int face = 0; face < 6; ++face)                              // +X,-X,+Y,-Y,+Z,-Z
    glTextureSubImage3D(cube, 0, 0, 0, face, size, size, 1, GL_RGBA, GL_HALF_FLOAT, data[face]);
glGenerateTextureMipmap(cube);
glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS);                           // global; filter across face edges
```
With DSA the face is the `zoffset`; non-DSA uses `GL_TEXTURE_CUBE_MAP_POSITIVE_X + face`.
Sample with a direction: `texture(samplerCube, dir)`. Face selection and per-face orientation
follow the spec's cube map tables, so images authored in another convention may need flips; check
with a labelled test cube.

Render to a face: `glNamedFramebufferTextureLayer(fbo, GL_COLOR_ATTACHMENT0, cube, mip, face)`,
or attach the whole cube (`glNamedFramebufferTexture`) and pick the face with `gl_Layer` in a
geometry/vertex shader (layered rendering, one pass for 6 faces).

## 2. 2D texture array
```c
glCreateTextures(GL_TEXTURE_2D_ARRAY, 1, &arr);
glTextureStorage3D(arr, mips, GL_SRGB8_ALPHA8, 1024, 1024, layers);
glTextureSubImage3D(arr, 0, 0, 0, layer, 1024, 1024, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
```
```glsl
uniform sampler2DArray uAlbedo;
vec4 c = texture(uAlbedo, vec3(uv, float(materialIndex)));   // the layer coordinate is not filtered across layers
```
All layers share size, format and mip count. Query `GL_MAX_ARRAY_TEXTURE_LAYERS` for the layer limit;
for cube map arrays it limits layer-faces. Cube map arrays (`GL_TEXTURE_CUBE_MAP_ARRAY`, sampled with
`samplerCubeArray`) use layer-face numbers, layer-face = `layer*6 + face` (also the `zoffset` of
`glTextureSubImage3D`).

## Gotchas
- Without `GL_TEXTURE_CUBE_MAP_SEAMLESS` low mips show visible seams in filtered reflections.
- Arrays vs atlases: filtering and wrapping happen inside one layer, so there is no bleeding between
  sub-images; atlases allow mixed sizes. Prefer arrays when sizes can be normalised.
- Sampler arrays (`sampler2D tex[8]`) can only be indexed with a dynamically uniform expression (GLSL 4.60);
  the layer coordinate of an array texture is an ordinary coordinate and may vary per pixel.

## Verify
- [ ] Labelled debug cube (+X red text etc.) shows each face where expected in a skybox.
- [ ] RenderDoc texture viewer shows every array layer populated with full mip chains.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022) and GLSL 4.60 spec. Confirmed: `GL_TEXTURE_CUBE_MAP_SEAMLESS` is a spec enable; `glTextureSubImage3D` on a cube map treats `zoffset` as the face; cube map array layer-face numbering and the `MAX_ARRAY_TEXTURE_LAYERS` rule for layer-faces; `samplerCubeArray` exists; opaque arrays need dynamically uniform indices. Removed: RenderMan/left-handed convention note, the numeric layer minimums, the GL 4.0 version claim, per-layer wrap-mode wording.

Method: documentation only; no commands were run.
