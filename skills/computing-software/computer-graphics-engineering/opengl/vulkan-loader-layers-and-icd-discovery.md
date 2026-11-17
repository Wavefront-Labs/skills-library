---
id: computing-software.computer-graphics-engineering.opengl.vulkan-loader-layers-and-icd-discovery
name: vulkan-loader-layers-and-icd-discovery
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-instance, vulkan-loader, vk-loader-debug, vk-icd-filenames]
level: advanced
status: docs-checked
description: "Debug the Vulkan loader: how ICDs and layers are found (JSON manifests, registry, env vars), VK_LOADER_DEBUG output, and fixing 'no ICD' errors."
sources: ["https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderInterfaceArchitecture.md", "https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderDebugging.md", "https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderLayerInterface.md", "https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderDriverInterface.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan loader, layers and ICD discovery

`vulkan-1.dll` / `libvulkan.so.1` is the loader. It finds **ICDs** (drivers) and **layers**
through JSON manifest files, then builds a call chain app -> layers -> ICD.

## Where manifests live
| Platform | ICDs | Layers |
|---|---|---|
| Windows | per-adapter `VulkanDriverName` values under the display adapter class registry keys, plus `HKLM\SOFTWARE\Khronos\Vulkan\Drivers` | `HKLM`/`HKCU` `SOFTWARE\Khronos\Vulkan\ExplicitLayers` and `ImplicitLayers` |
| Linux | `vulkan/icd.d` under `$XDG_CONFIG_HOME`, `$XDG_CONFIG_DIRS` (/etc/xdg), `/usr/local/etc`, `/etc`, `$XDG_DATA_HOME`, `$XDG_DATA_DIRS` (/usr/local/share, /usr/share) | `explicit_layer.d`, `implicit_layer.d` in the corresponding `vulkan` directories |
| macOS | the same Linux-style list, plus `<bundle>/Contents/Resources/vulkan/icd.d` first | same tree |
| Android | see the Android documentation; not covered by the loader documents cited here | |

## Debug output
```sh
VK_LOADER_DEBUG=all ./app            # or a comma list of error,warn,info,debug,driver,layer
VK_LOADER_DEBUG=driver,layer vulkaninfo --summary
```
Shows each manifest found, why an ICD was rejected (wrong arch, missing library, API version),
and which layers were loaded in which order.

## Environment overrides (filter variables need a loader built with Vulkan headers 1.3.234 or later)
| Variable | Effect |
|---|---|
| `VK_DRIVER_FILES` (old `VK_ICD_FILENAMES`) | use only these ICD manifests |
| `VK_ADD_DRIVER_FILES` | add ICDs without removing system ones |
| `VK_LOADER_DRIVERS_SELECT` / `_DISABLE` | glob filter on driver manifest names |
| `VK_LAYER_PATH` / `VK_ADD_LAYER_PATH` | extra explicit layer search dirs |
| `VK_INSTANCE_LAYERS` | force-enable layers (e.g. `VK_LAYER_KHRONOS_validation`) |
| `VK_LOADER_LAYERS_DISABLE` | disable layers, e.g. a misbehaving implicit overlay |
| `VK_LOADER_DEVICE_SELECT` | `0xVENDOR:0xDEVICE` (hex) to move that GPU to the front of the enumeration order (Linux only; does not remove other devices) |

## Implicit layers
Overlay and capture tools install implicit layers that load into every
app and can cause failures inside `vkCreateInstance` or broken swapchains.
`VK_LOADER_DEBUG=layer` lists them; `VK_LOADER_LAYERS_DISABLE=~implicit~` disables all
implicit layers for testing (`VK_LOADER_LAYERS_ENABLE` re-enables selected ones). An implicit layer manifest also defines a
`disable_environment` variable.

## Common errors
- `VK_ERROR_INCOMPATIBLE_DRIVER` from `vkCreateInstance`: no usable ICD found. Portability devices such as MoltenVK are not
  reported unless the app enables `VK_KHR_portability_enumeration` and sets `VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR`.
- 32-bit app on 64-bit OS: needs the 32-bit ICD (`WOW6432Node` registry, `i386` package).
- Containers: the loader needs the ICD manifest and the driver library inside the container; check `VK_LOADER_DEBUG=driver` output.

## Verify
- [ ] `vulkaninfo --summary` lists the expected GPU(s); loader debug output shows no rejected manifests for them.

## Checked
Checked 2026-10-26 against the Vulkan-Loader docs on main (LoaderDebugging.md, LoaderInterfaceArchitecture.md, LoaderDriverInterface.md, LoaderLayerInterface.md, LoaderApplicationInterface.md) and Vulkan-Docs VK_KHR_portability_enumeration.
Confirmed: VK_LOADER_DEBUG levels; Windows registry keys; Linux and macOS manifest search lists; VK_DRIVER_FILES/VK_ICD_FILENAMES, VK_ADD_DRIVER_FILES, VK_LAYER_PATH, VK_ADD_LAYER_PATH, VK_INSTANCE_LAYERS, VK_LOADER_DRIVERS_SELECT/DISABLE, VK_LOADER_LAYERS_ENABLE/DISABLE and ~implicit~; VK_LOADER_DEVICE_SELECT is Linux-only and reorders only; disable_environment; portability enumeration behaviour. Removed D3DKMT, Android property, overlay product names and container claims.
Method: documentation only; no commands were run.
