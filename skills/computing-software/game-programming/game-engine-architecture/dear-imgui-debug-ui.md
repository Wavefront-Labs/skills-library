---
id: computing-software.game-programming.game-engine-architecture.dear-imgui-debug-ui
name: dear-imgui-debug-ui
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, dear-imgui, imgui, immediate-mode-gui, debug-ui, tweak-panels, docking, game-programming]
level: practitioner
status: docs-checked
description: "Integrate Dear ImGui as engine debug UI: build setup, backends, frame loop, input capture with WantCapture flags, the ID stack, docking and multi-viewports."
sources: ["https://github.com/ocornut/imgui", "https://github.com/ocornut/imgui/wiki/Getting-Started", "https://github.com/ocornut/imgui/blob/master/docs/FAQ.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dear ImGui debug UI

**Goal:** tweak values, inspect entities and visualise systems at runtime with minimal code (Dear
ImGui by Omar Cornut).

## Setup (from the Getting Started wiki)
- Branch: `master`, or `docking`, which adds Docking and Multi-viewports. Both are maintained.
- Add the repository as a submodule or copy it in. Add `imgui/` and `imgui/backends/` to the
  include paths and compile all `imgui/*.cpp` in the root plus the backend pair you need
  (for example `imgui_impl_win32` with `imgui_impl_dx12`, `imgui_impl_glfw` with
  `imgui_impl_opengl3`, `imgui_impl_sdl3` with `imgui_impl_vulkan`). The wiki recommends adding the
  sources directly rather than building a static or shared library, since the API is call-heavy.
- `misc/cpp/imgui_stdlib.*` gives `InputText()` support for `std::string`.
- Run the `examples/` applications first; they are the reference when integration fails.

Steps (as listed on the wiki):
1. Include `imgui.h` and the backend headers.
2. `ImGui::CreateContext()` (preceded by `IMGUI_CHECKVERSION()` in the examples).
3. Optionally set config flags, fonts and style.
4. Initialise the platform and renderer backends (`ImGui_ImplWin32_Init(hwnd)`; DX12 takes an
   `ImGui_ImplDX12_InitInfo` with Device, CommandQueue, NumFramesInFlight, RTVFormat and SRV
   descriptor heap plus alloc/free callbacks).
5. Loop start: poll events, call the backends' `ImGui_ImplXXX_NewFrame()` functions, then
   `ImGui::NewFrame()`.
6. Loop end: `ImGui::Render()`, then the renderer backend's `RenderDrawData(ImGui::GetDrawData(), ...)`.
7. Forward events where the backend needs it (Win32: `ImGui_ImplWin32_WndProcHandler` in the
   WndProc; SDL: `ImGui_ImplSDL3_ProcessEvent`).
8. Shut down the backends, then `ImGui::DestroyContext()`.

`ImGui::ShowDemoWindow()` and `imgui_demo.cpp` are the reference for how each widget is used.
Dear ImGui expects a game-like loop that updates continuously at interactive frame rates;
going idle or variable-rate use is possible but not well supported by default.

## Input capture
Read `io.WantCaptureMouse`, `io.WantCaptureKeyboard` (and `io.WantTextInput`) from `ImGuiIO`.
- When `WantCaptureMouse` is set, discard or hide mouse input from your game; likewise for the
  keyboard flag.
- Always pass mouse and keyboard input to Dear ImGui regardless of those flags (it needs, for
  example, clicks on empty space to unfocus its windows). With the default backends this is
  automatic.
- Prefer the flag over checking whether the mouse hovers a window; it handles dragging, popups and
  modals correctly.
- A text field releases focus on the Return key-down, so the following key-up may arrive with
  `WantCaptureKeyboard` false; track which key-downs went to ImGui if that matters.

## ID stack
The FAQ has a section on the label and ID stack: use `PushID()`/`PopID()` or a `##` suffix to give
widgets with the same label distinct IDs, `##` alone for an empty label, and `###` for a label that
changes while keeping its ID. Read the FAQ section "About the ID Stack system" for the full rules.

## Docking and multi-viewports
- Docking: use the `docking` branch and set `io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;`.
- Multi-viewports: also the `docking` branch, set `ImGuiConfigFlags_ViewportsEnable`, and at the
  end of the render loop (after rendering the main viewport, before presenting) call
  `ImGui::UpdatePlatformWindows();` and `ImGui::RenderPlatformWindowsDefault();`. OpenGL needs the
  current GL context restored afterwards; check the example for your backend.
- Keyboard and gamepad navigation: `ImGuiConfigFlags_NavEnableKeyboard` and
  `ImGuiConfigFlags_NavEnableGamepad`.

## Verify
- [ ] The demo window renders and responds with the chosen backends.
- [ ] Typing in an ImGui field does not trigger game input.
- [ ] Rows with identical labels edit the intended data.

## Checked

Date 2026-11-08. Pages: the Dear ImGui repository page, Getting Started wiki (read in full), and docs/FAQ.md (index and the input-dispatch section). Confirmed: branch choice, build steps, backend names, DX12 init info fields, frame loop calls, event forwarding, WantCapture flags and the always-forward rule, docking and viewport flags and calls, nav flags. Removed as not on the cited pages: the code listing with a made-up DX12 init, the claim that `End()` must be called even when `Begin()` returns false, `PlotLines`, ImPlot, `GetForegroundDrawList`, reflection-driven inspector advice, Unreal and Unity plugin remarks, and the compile-out shipping advice.

Method: docs-only read of cited pages, 2026-11-08
