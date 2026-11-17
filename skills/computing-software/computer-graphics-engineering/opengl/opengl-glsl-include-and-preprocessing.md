---
id: computing-software.computer-graphics-engineering.opengl.opengl-glsl-include-and-preprocessing
name: opengl-glsl-include-and-preprocessing
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, glsl-include, arb-shading-language-include, glsl-line-directive]
level: practitioner
status: docs-checked
description: "Add #include to GLSL for OpenGL: a CPU-side preprocessor with #line mapping, ARB_shading_language_include, defines injection after #version."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shading_language_include.txt", "https://github.com/KhronosGroup/glslang", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# #include and preprocessing for GLSL in OpenGL

Core GLSL has a C preprocessor but no `#include`. Options:

## 1. CPU-side include expansion (most portable)
```cpp
std::string expand(const fs::path& file, int fileId, std::set<fs::path>& seen, std::vector<fs::path>& ids) {
    std::ifstream in(file); std::string line, out; int lineNo = 1;
    while (std::getline(in, line)) {
        std::smatch m;
        if (std::regex_match(line, m, std::regex(R"(\s*#\s*include\s+"([^"]+)\")"))) {
            fs::path inc = file.parent_path() / m[1].str();
            if (seen.insert(fs::canonical(inc)).second) {          // include-once
                int id = (int)ids.size(); ids.push_back(inc);
                out += "#line 1 " + std::to_string(id) + "\n" + expand(inc, id, seen, ids);
            }
            out += "#line " + std::to_string(lineNo + 1) + " " + std::to_string(fileId) + "\n";
        } else out += line + "\n";
        ++lineNo;
    }
    return out;
}
```
`#line <line> <source-string-number>`: GLSL only accepts an integer, not a filename, so keep a
table `ids[]` and translate the source-string number in driver error messages back to file names when
logging (the message format is implementation-defined).

## 2. Inject defines after #version
`#version` must be the first non-comment line. Insert variant defines on the line after it:
```cpp
auto pos = src.find('\n', src.find("#version")) + 1;
src.insert(pos, "#define USE_SHADOWS 1\n#define MAX_LIGHTS 16\n#line 2 0\n");
```
Or pass multiple strings to `glShaderSource` (`{version, defines, body}`), which keeps line
numbers of the body intact if you add `#line 1 0` before it.

## 3. ARB_shading_language_include
Register virtual files with `glNamedStringARB(GL_SHADER_INCLUDE_ARB, "/common/brdf.glsl", ...)`,
then `#extension GL_ARB_shading_language_include : require` and
`glCompileShaderIncludeARB`. Check `GL_EXTENSIONS` for `GL_ARB_shading_language_include` and keep a fallback.

## 4. Offline: glslang with GL_GOOGLE_include_directive
`glslangValidator -I<dir>` adds `<dir>` to the include search path (the shader enables it with
`#extension GL_GOOGLE_include_directive : require`); the same sources can be expanded by option 1 for runtime GLSL.

## Gotchas
- Include guards (`#ifndef BRDF_GLSL`) work, but the include-once set above avoids repeated I/O.
- `#extension` directives must precede non-preprocessor code (GLSL 4.60), including inside included files.
- Hot reload must watch every included file, not just the root.

## Verify
- [ ] A deliberate syntax error in an included file reports the correct file and line.

## Checked

Date: 2026-10-26. Documentation: GLSL 4.60 spec, ARB_shading_language_include extension text, glslang `StandAlone/StandAlone.cpp` and `Versions.cpp` (main branch). Confirmed: core GLSL has `#line line source-string-number` taking integers, not file names; `#version` must precede everything except comments and white space; `#extension` must precede non-preprocessor tokens; `glNamedStringARB`, `GL_SHADER_INCLUDE_ARB`, `glCompileShaderIncludeARB` and the `#extension GL_ARB_shading_language_include` directive exist; glslangValidator accepts `-I<dir>` and implements `GL_GOOGLE_include_directive`. Replaced: the dead GL_GOOGLE_include_directive link in KhronosGroup/GLSL (the extension is implemented in glslang). Removed: vendor availability claims, glslc `-I`, driver log formats.

Method: documentation only; no commands were run.
