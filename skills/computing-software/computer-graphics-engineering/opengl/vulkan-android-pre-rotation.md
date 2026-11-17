---
id: computing-software.computer-graphics-engineering.opengl.vulkan-android-pre-rotation
name: vulkan-android-pre-rotation
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, pre-rotation, surface-transform, android-vulkan]
level: advanced
status: draft
description: "Handle Android surface rotation in Vulkan with pre-rotation: currentTransform, swapping extents, rotating the projection, and avoiding compositor rotation cost."
sources: ["https://developer.android.com/games/optimize/vulkan-prerotation", "https://registry.khronos.org/vulkan/specs/1.3-extensions/man/html/VkSurfaceTransformFlagBitsKHR.html", "https://github.com/KhronosGroup/Vulkan-Samples/tree/main/samples/performance/surface_rotation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android pre-rotation

On Android the display has a native orientation. When the device is rotated, someone must
rotate your image: either the compositor (an extra full-screen GPU/DPU pass, more bandwidth and
latency) or you, by rendering already rotated ("pre-rotation").

## 1. Create the swapchain with the current transform
```c
VkSurfaceCapabilitiesKHR caps; vkGetPhysicalDeviceSurfaceCapabilitiesKHR(gpu, surface, &caps);
VkSurfaceTransformFlagBitsKHR pre = caps.currentTransform;
VkExtent2D extent = caps.currentExtent;
if (pre & (VK_SURFACE_TRANSFORM_ROTATE_90_BIT_KHR | VK_SURFACE_TRANSFORM_ROTATE_270_BIT_KHR))
    std::swap(extent.width, extent.height);      // swapchain is in native (unrotated) orientation
sci.preTransform = pre;                            // NOT IDENTITY
sci.imageExtent = extent;
```
Using `VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR` while `currentTransform` differs makes vkQueuePresent
return `VK_SUBOPTIMAL_KHR` on Android 10+ and forces compositor rotation.

## 2. Rotate in the vertex stage
Multiply the projection by a rotation around z matching the transform:
```cpp
float angle = pre == ROTATE_90 ? 90.f : pre == ROTATE_180 ? 180.f : pre == ROTATE_270 ? 270.f : 0.f;
glm::mat4 preRot = glm::rotate(glm::mat4(1), glm::radians(angle), glm::vec3(0, 0, 1));
glm::mat4 proj = preRot * glm::perspective(fovY, (float)logicalW / logicalH, n, f); // logical = user-facing size
```
The aspect ratio stays the *logical* (rotated) one; only the final clip-space is rotated.

## 3. Everything screen-space must follow
- Viewport and scissor use the swapchain (native) extent; scissor rectangles from UI code must be rotated.
- Post-processing that reads neighbouring pixels in screen axes (e.g. directional blurs, UI
  pixel snapping) and touch input mapping need the same transform.
- Render targets sized from the swapchain should be in native orientation too.

## 4. Detecting rotation
Android doesn't always report `OUT_OF_DATE` on 180-degree rotation. Poll
`currentTransform` every frame (cheap) or handle `onNativeWindowResized` /
`APP_CMD_CONFIG_CHANGED`, then recreate the swapchain when it changes.

## Gotchas
- `currentExtent` on some devices is already swapped; base the swap on transform, and validate
  with logs on several devices.
- Disable pre-rotation for 180-degree changes only if you handle it; otherwise the image is upside down.

## Verify
- [ ] `adb shell dumpsys SurfaceFlinger` shows the layer with no rotation applied by the compositor (client composition not used).
- [ ] No `VK_SUBOPTIMAL_KHR` after rotating the device in all four orientations.
