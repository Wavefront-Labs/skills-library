---
id: computing-software.game-programming.godot.custom-export-templates-size-reduction
name: custom-export-templates-size-reduction
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, export-templates, scons, build-size, game-programming]
level: advanced
status: docs-checked
description: "Compile custom Godot export templates with SCons to shrink builds: optimize=size, LTO, disabling 3D and unused modules, build profiles, text server choice."
sources: ["https://docs.godotengine.org/en/stable/engine_details/development/compiling/optimizing_for_size.html", "https://docs.godotengine.org/en/stable/engine_details/development/compiling/introduction_to_the_buildsystem.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Custom export templates for size reduction

**Goal:** smaller binaries (web, mobile, jam builds) than the official templates.

## Build basics
Build from the Godot source at the tag matching your editor. Templates are version-specific: the build
system's `version.txt` (for example `4.4.1.stable`) selects the directory where templates are installed.
```bash
scons platform=windows target=template_release optimize=size_extra lto=full disable_3d=yes \
      module_text_server_adv_enabled=no module_text_server_fb_enabled=yes
```
`target=template_debug` builds the debug template.

## Size levers (from "Optimizing a build for size")
- `optimize=size` (default when targeting Web) favours small binaries at the cost of speed; `optimize=size_extra`
  (introduced in Godot 4.5) is smaller still and slower.
- `lto=full` enables link-time optimisation. `production=yes` is an alias for
  `use_static_cpp=yes debug_symbols=no lto=auto`; LTO stays off for macOS, iOS and MSVC under `lto=auto`
  because linking is very slow or has code issues there.
- Strip debug symbols from Windows (MinGW), Linux and macOS binaries with the `strip` tool.
- `disable_3d=yes` for 2D-only projects; `disable_advanced_gui=yes` if you do not need advanced GUI controls;
  `module_godot_physics_3d_enabled=no` and `module_jolt_enabled=no` drop 3D physics.
- Disable modules with `module_<name>_enabled=no` (the page lists many, for example csg, enet, fbx, camera); only
  disable those the project does not use. Test the full game afterwards.
- Build profile: pass `build_profile=/path/to/profile.gdbuild` (the page uses the `.gdbuild` extension); generate it
  with the editor's engine compilation configuration tooling described in the page.
- Text server: `module_text_server_adv_enabled=no` needs `module_text_server_fb_enabled=yes` or the binary has no
  text server and no text is displayed. The fallback server lacks the advanced server's text features, so check
  that your languages still render correctly.

## Using the templates
Point the export preset's custom template paths at the built binaries; see the export docs for each platform.

## Verify
- [ ] Compare binary sizes before and after and record the SCons flags in the repo.
- [ ] Full playthrough on the custom template with no missing-class errors.

## Checked
2026-10-28. Confirmed on "Optimizing a build for size" and "Introduction to the buildsystem" (Godot 4.7 docs):
optimize levels, size_extra introduced in 4.5, production alias and LTO behaviour, strip, disable_3d,
disable_advanced_gui, module and physics options, `.gdbuild` build profile, text-server rule, version.txt.
Removed or corrected: "size_extra (4.4+)" (4.5), build profile extension `.build` (it is `.gdbuild`) and its
"4.1+" editor path, the PCK encryption key steps, ICU/HarfBuzz and Arabic/Hindi wording, Brotli/wasm-opt notes,
platform list, deprecated=no, and the MinGW/Xcode gotchas.
Method: documentation only; no commands were run.
