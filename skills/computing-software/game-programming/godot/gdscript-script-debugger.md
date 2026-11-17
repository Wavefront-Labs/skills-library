---
id: computing-software.game-programming.godot.gdscript-script-debugger
name: gdscript-script-debugger
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript-debugger, debugging, breakpoints, remote-tree, game-programming]
level: practitioner
status: docs-checked
description: "Debug GDScript with the Godot debugger: breakpoints and the breakpoint keyword, stack trace, expressions, push_error and assert, profilers."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html", "https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript script debugger

**Goal:** find logic bugs by stopping and inspecting rather than sprinkling prints.

## Breakpoints
- Click the script editor gutter left of the line numbers: a red dot marks the breakpoint; click it again to remove it.
  Gutter breakpoints persist across editor restarts but are not stored in the script.
- The `breakpoint` keyword in GDScript is stored in the script itself, so it is shared through version control
  (remember to remove stray ones before committing).
- When the debugger breaks, the **Stack Trace** tab opens, a green arrow marks the line in the gutter, and buttons
  control execution (including Continue and a "skip all breakpoints" toggle).
- While paused you can type an **expression** at the top of the debugger panel; it can use member variables and
  locals in scope at that line. Uncheck Clear on Run to keep expressions across runs.
- Breakpoints and the debugger do not work on `@tool` scripts (they are ignored); use print statements there.

## Message helpers
```gdscript
push_warning("odd state")        # prints a warning with a stack trace
push_error("bad index %d" % i)   # prints an error; does not pause execution
assert(hp >= 0, "hp negative")   # in debug builds prints the message and pauses
```
Godot recommends `push_error()` / `push_warning()` over `print()` for problems, because they stand apart from
debug prints and show a stack trace.

## Runtime inspection
- Debugger panel tabs include Stack Trace, Errors, Profiler, **Visual Profiler** (CPU and GPU rendering cost only;
  not scripting or physics; unsupported with the Compatibility renderer on macOS), **Network Profiler** (nodes using
  the multiplayer API plus a bandwidth meter) and **Monitors**.
- The Debug menu has Visible Collision Shapes, Synchronize Scene Changes and Synchronize Script Changes, among others
  (see "Overview of debugging tools").

## Gotchas
- `print` every frame on many nodes floods the output; remove or gate it.
- Check the editor's Debug menu and the Godot docs for current keyboard shortcuts and remote-debug options, which
  this skill no longer lists.

## Verify
- [ ] No leftover `breakpoint` keywords in commits.

## Checked
2026-10-28. Confirmed on the Debugger panel, Overview of debugging tools and @GlobalScope pages: gutter and
keyword breakpoints, Stack Trace behaviour, expression field, tool-script limitation, push_error/push_warning/assert
behaviour, profiler tabs and limits, Debug menu options. Removed (not found on the pages): F9/F10/F11/F12 shortcuts,
the VS Code port 6006, the `--remote-debug tcp://` port 6007, `print_debug` and `print_stack` descriptions, "Keep
Debugger Open", Android one-click deploy, release-export and thread claims, and the @tool Output-panel claim.
Method: documentation only; no commands were run.
