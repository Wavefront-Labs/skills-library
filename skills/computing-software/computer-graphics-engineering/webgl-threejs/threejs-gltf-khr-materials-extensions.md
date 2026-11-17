---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-gltf-khr-materials-extensions
name: threejs-gltf-khr-materials-extensions
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-loading, khr-materials, meshphysicalmaterial, transmission, clearcoat, gltf-extensions]
level: advanced
status: docs-checked
description: "Use glTF KHR_materials_* extensions in three.js: how each maps to MeshPhysicalMaterial, authoring from Blender, performance cost, and checking what loaded."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/GLTFLoader.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/MeshPhysicalMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glTF KHR_materials extensions in three.js

GLTFLoader turns materials that use the physical extensions below into **MeshPhysicalMaterial**; KHR_materials_unlit gives MeshBasicMaterial.

| Extension | three.js property | Typical use |
|---|---|---|
| KHR_materials_clearcoat | clearcoat, clearcoatRoughness, clearcoatNormalMap | car paint, lacquer |
| KHR_materials_transmission | transmission, transmissionMap | glass, thin plastic |
| KHR_materials_volume | thickness, attenuationColor, attenuationDistance | thick tinted glass, liquids |
| KHR_materials_ior | ior | refraction strength (default 1.5) |
| KHR_materials_specular | specularIntensity, specularColor | non-metal reflectance tweak |
| KHR_materials_sheen | sheen, sheenColor, sheenRoughness | fabric, velvet |
| KHR_materials_iridescence | iridescence, iridescenceIOR, iridescenceThicknessMinimum / iridescenceThicknessMaximum | soap bubbles, coatings |
| KHR_materials_anisotropy | anisotropy, anisotropyRotation, anisotropyMap | brushed metal, hair |
| KHR_materials_emissive_strength | emissiveIntensity | HDR emissive for bloom |
| KHR_materials_dispersion | dispersion | prism rainbow |
| KHR_materials_unlit | MeshBasicMaterial | baked/stylised assets |

## Cost
- Transmission renders the opaque objects (and the back faces of double-sided transmissive objects) into one shared
  render target per camera, so a transmissive object does not show another transmissive object's front faces.
- MeshPhysicalMaterial extends MeshStandardMaterial; use the standard material where the extra layers are not needed.

## Check what loaded
`gltf.parser.json.extensionsUsed`; inspect `mesh.material.type === 'MeshPhysicalMaterial'` and the
properties above. Loader plugins (`loader.register(parser => new MyExt(parser))`) add vendor extensions.

## Gotchas
- `attenuationDistance` default is Infinity: no tint until set.
- KHR_materials_variants is not built in: GLTFLoader lists it among the extensions supported by separately registered plugins (three-gltf-extensions).

## Verify
- [ ] Glass refracts objects behind it and tints with thickness.
- [ ] Clearcoat shows a second sharp highlight over the base layer.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), GLTFLoader.js and MeshPhysicalMaterial.js source.
Confirmed: the extension to property mapping in the table (clearcoat, transmission, volume incl. `attenuationDistance`
default Infinity, ior default 1.5, specular, sheen, iridescence, anisotropy, emissive strength to `emissiveIntensity`,
dispersion, unlit to MeshBasicMaterial); `ior` default 1.5; the transmission pass renders opaque objects (plus back faces
of double-sided transmissive objects) to a shared target; KHR_materials_variants is a separately registered plugin;
`LoaderPlugin` registration via `register(parser => ...)` and `parser.json` exist.

Method: documentation only; no commands were run.
