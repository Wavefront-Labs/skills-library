---
id: computing-software.computer-graphics-engineering.shader-programming.shader-hot-reload
name: shader-hot-reload
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, shader-hot-reload, live-reload, file-watching, pipeline-recreation]
level: practitioner
status: draft
description: "Implement shader hot reload: watch source and include files, recompile off-thread, swap pipelines safely in flight, and keep the last good shader on errors."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readdirectorychangesw", "https://github.com/microsoft/DirectXShaderCompiler/wiki/Using-dxc.exe-and-dxcompiler.dll", "https://man7.org/linux/man-pages/man7/inotify.7.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shader hot reload

## 1. Detect changes
- Watch the shader directory (ReadDirectoryChangesW on Windows, inotify on Linux, FSEvents on
  macOS, or a library such as efsw); poll mtimes once a second as a fallback.
- Track **include dependencies** per shader: have the compiler report them (DXC `-MF` style
  dependency output or a custom include handler that records every opened file), so editing
  `common.hlsli` reloads every dependent shader.
- Debounce: editors write files in several steps; wait ~100 ms after the last event.

## 2. Recompile
- Compile on a worker thread with the same defines/permutation key as the original.
- On error: log the message with file:line (clickable in IDE), **keep the previous working
  pipeline**, and optionally show an on-screen error overlay.

## 3. Swap safely
- Create the new pipeline/PSO, then swap a handle the renderer reads at command-recording time.
- Defer destruction of the old pipeline until the GPU frames that used it have completed
  (frames-in-flight fence or deletion queue).
- Reflection changes (new bindings) may require new pipeline layouts; rebuild descriptor
  layouts or reject the reload with a message.

## 4. Extra
- GL: `glDeleteProgram` is deferred by the driver until unused; still easy, just relink.
- Include a manual "reload all shaders" key for when watchers miss events (network drives, WSL).
- Strip hot reload from shipping builds (precompiled blobs only).

## Gotchas
- Compiling on the render thread causes hitches; with many permutations, reload only variants
  currently in use.
- File watchers on network shares and some editors' atomic-save (rename) need rename events too.

## Verify
- [ ] Edit an include: all dependent shaders reload within a second; a syntax error leaves the
  frame rendering with the old shader.
