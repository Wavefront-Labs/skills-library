---
id: computing-software.computer-graphics-engineering.opengl.vulkan-shader-modules-and-spirv-loading
name: vulkan-shader-modules-and-spirv-loading
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, shader-module, vkcreateshadermodule, spirv-entry-points]
level: practitioner
status: docs-checked
description: "Load SPIR-V into Vulkan shader modules correctly: 4-byte alignment, magic checks, entry points, multiple entry points per module, and maintenance5 inline modules."
sources: ["https://docs.vulkan.org/spec/latest/chapters/shaders.html", "https://docs.vulkan.org/spec/latest/appendices/VK_KHR_maintenance5.html", "https://github.com/google/shaderc/blob/main/glslc/README.asciidoc", "https://github.com/KhronosGroup/SPIRV-Headers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader modules and SPIR-V loading

## Loading
```cpp
std::vector<uint32_t> loadSpirv(const char* path) {
    std::ifstream f(path, std::ios::binary | std::ios::ate);
    size_t bytes = (size_t)f.tellg();
    if (bytes % 4 != 0) throw std::runtime_error("SPIR-V size not multiple of 4");
    std::vector<uint32_t> code(bytes / 4);                 // uint32_t storage = correct alignment
    f.seekg(0); f.read(reinterpret_cast<char*>(code.data()), bytes);
    if (code.empty() || code[0] != 0x07230203) throw std::runtime_error("bad SPIR-V magic");
    return code;
}
VkShaderModuleCreateInfo ci = { VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO };
ci.codeSize = code.size() * 4;    // BYTES, not words
ci.pCode = code.data();
vkCreateShaderModule(device, &ci, NULL, &module);
```
Reading into `std::vector<char>` and casting gives possibly misaligned `pCode` (UB) and the
classic `codeSize` in words bug.

Embedding: `glslc -mfmt=num` or `glslangValidator --vn varName` emits a C array of words to
compile into the binary (no file I/O, no missing-file errors on mobile).

## Entry points
- `VkPipelineShaderStageCreateInfo::pName` selects the entry point; default `"main"` for GLSL.
- A SPIR-V module can contain several `OpEntryPoint`s; pick one per stage with `pName` (compiler options for emitting several entry points differ per tool, so check your compiler's documentation).
- `pName` must name an `OpEntryPoint` whose execution model matches the stage (`VUID-VkPipelineShaderStageCreateInfo-pName-00707`).

## Lifetime and maintenance5
- A shader module can be destroyed while pipelines created from it are still in use (spec).
- With `VK_KHR_maintenance5` (promoted to Vulkan 1.4) chain `VkShaderModuleCreateInfo` into the stage
  `pNext` and leave `module` null: no module objects at all (the extension text calls shader modules deprecated).
- `VK_EXT_shader_module_identifier` lets you create pipelines from a cache using only a module
  identifier hash (skip shipping SPIR-V for cached pipelines).

## Validation of SPIR-V itself
- Run `spirv-val --target-env <vulkan env> shader.spv` before shipping (`--target-env` is an `spirv-val` option). The spec requires `pCode` to be valid SPIR-V
  that passes the SPIR-V environment validation rules (`VUID-VkShaderModuleCreateInfo-pCode-08736`/`-08737`).
- Capabilities used must be enabled as device features (e.g. `Int64` needs `shaderInt64`).

## Verify
- [ ] Startup asserts on magic/size pass; validation reports no SPIR-V capability errors on the minimum target device.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json, chapters/shaders.adoc, appendices/VK_KHR_maintenance5.adoc, VK_EXT_shader_module_identifier.adoc, xml/vk.xml), SPIRV-Headers spirv.h, shaderc glslc README, glslang StandAlone.cpp and SPIRV-Tools val.cpp.
Confirmed: codeSize multiple of 4; SPIR-V magic number 0x07230203; modules may be destroyed while pipelines are in use; maintenance5 promoted to Vulkan 1.4 with chained VkShaderModuleCreateInfo; pName/execution model rule; glslc -mfmt=num; glslangValidator --vn (variable-name); spirv-val --target-env. Removed DXC/Slang entry-point options and the claim about the validation layer's shader-validation cost.
Method: documentation only; no commands were run.
