---
id: computing-software.computer-graphics-engineering.opengl.opengl-headless-rendering-with-egl
name: opengl-headless-rendering-with-egl
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, opengl-context, egl-headless, egl-device, surfaceless, server-rendering]
level: advanced
status: docs-checked
description: "Render OpenGL with no window or X server: EGL device enumeration, surfaceless/pbuffer contexts, FBO targets, and a software-rendering fallback for CI."
sources: ["https://registry.khronos.org/EGL/extensions/EXT/EGL_EXT_platform_device.txt", "https://registry.khronos.org/EGL/extensions/EXT/EGL_EXT_device_enumeration.txt", "https://registry.khronos.org/EGL/extensions/KHR/EGL_KHR_surfaceless_context.txt", "https://registry.khronos.org/EGL/extensions/MESA/EGL_MESA_platform_surfaceless.txt", "https://registry.khronos.org/EGL/extensions/NV/EGL_NV_device_cuda.txt", "https://docs.mesa3d.org/envvars.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headless OpenGL with EGL

**Use for:** thumbnail/render farms, CI image tests, ML data generation, server-side
visualisation. No X11/Wayland display, no window.

## 1. Pick a device (EGL_EXT_device_enumeration + platform_device)
```c
PFNEGLQUERYDEVICESEXTPROC eglQueryDevicesEXT =
    (PFNEGLQUERYDEVICESEXTPROC)eglGetProcAddress("eglQueryDevicesEXT");
EGLDeviceEXT devs[8]; EGLint n;
eglQueryDevicesEXT(8, devs, &n);
EGLDisplay dpy = eglGetPlatformDisplay(EGL_PLATFORM_DEVICE_EXT, devs[0], NULL);
EGLint major, minor; eglInitialize(dpy, &major, &minor);
```
On Mesa you can also use `EGL_PLATFORM_SURFACELESS_MESA` with `EGL_DEFAULT_DISPLAY`.

## 2. Config and context (no surface)
```c
EGLint cfgAttr[] = { EGL_SURFACE_TYPE, EGL_PBUFFER_BIT, EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
                     EGL_RED_SIZE, 8, EGL_GREEN_SIZE, 8, EGL_BLUE_SIZE, 8, EGL_DEPTH_SIZE, 24, EGL_NONE };
EGLConfig cfg; EGLint nc; eglChooseConfig(dpy, cfgAttr, &cfg, 1, &nc);
eglBindAPI(EGL_OPENGL_API);                     // desktop GL, not GLES
EGLint ctxAttr[] = { EGL_CONTEXT_MAJOR_VERSION, 4, EGL_CONTEXT_MINOR_VERSION, 6,
                     EGL_CONTEXT_OPENGL_PROFILE_MASK, EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT, EGL_NONE };
EGLContext ctx = eglCreateContext(dpy, cfg, EGL_NO_CONTEXT, ctxAttr);
eglMakeCurrent(dpy, EGL_NO_SURFACE, EGL_NO_SURFACE, ctx);   // needs EGL_KHR_surfaceless_context
gladLoadGLLoader((GLADloadproc)eglGetProcAddress);
```
If surfaceless is missing, create a 1x1 pbuffer with `eglCreatePbufferSurface` and make it current.

## 3. Render to an FBO and read back
There is no default framebuffer: create an FBO with colour+depth attachments at the output
size, render, then `glReadPixels` (or a PBO for async). Remember GL's origin is bottom-left;
flip rows before writing PNG.

## 4. Containers and CI
- Container GPU access depends on the vendor runtime: follow your GPU vendor's container documentation so its EGL
  library is visible inside the container.
- No GPU: Mesa documents `LIBGL_ALWAYS_SOFTWARE`, usable to select a software renderer such as llvmpipe; slow but
  predictable, good for golden-image tests.

## Gotchas
- Call `eglBindAPI(EGL_OPENGL_API)` before `eglCreateContext` when you want desktop OpenGL.
- Multi-GPU servers: to pick the GPU a CUDA job uses, query each device with the `EGL_CUDA_DEVICE_NV` attribute
  (EGL_NV_device_cuda) rather than assuming the enumeration order.
- Golden-image tests across vendors differ in rasterisation rules; compare with a tolerance (PSNR/SSIM),
  not exact bytes.

## Verify
- [ ] `glGetString(GL_RENDERER)` shows the GPU, not a software renderer.
- [ ] Output PNG matches a reference within tolerance; process exits cleanly with `eglTerminate`.

## Checked
2026-11-01: EGL function and enum names in the snippets (egl.xml), EGL_EXT_platform_device, device enumeration,
KHR_surfaceless_context, MESA_platform_surfaceless, NV_device_cuda (EGL_CUDA_DEVICE_NV) and Mesa LIBGL_ALWAYS_SOFTWARE
confirmed. Removed: Docker NVIDIA capability strings, glvnd variables, EGL_PLATFORM=surfaceless, eglinfo, CUDA
ordering claim, and the GLES-default claim (not confirmed in the pages read).
Method: documentation only; no commands were run.
