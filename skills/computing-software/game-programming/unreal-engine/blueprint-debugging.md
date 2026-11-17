---
id: computing-software.game-programming.unreal-engine.blueprint-debugging
name: blueprint-debugging
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, blueprints, blueprint-debugging, breakpoints, watch-values, print-string, visual-logger, game-programming]
level: intro
status: docs-checked
description: "Debug Blueprints with the Blueprint Debugger: breakpoints, watches, Data Flow tab, call stack, execution trace and PrintScriptCallstack, per Epic's Blueprint Debugger page."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-debugger-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blueprint debugging

**Goal:** pause Blueprint execution and inspect values using the Blueprint Debugger.

## Controls and breakpoints
- The Blueprint Debugger pauses Play-In-Editor (PIE) or Simulate-In-Editor (SIE); debugging controls in the toolbar
  become enabled while the project runs and change with the type of Blueprint and session state.
- The Blueprint Debugger window is under the Tools menu, or the Debug menu in the Blueprint Editor.
- Add a breakpoint: right-click a node > Add Breakpoint (a solid red octagon at the node's upper-left). The simulation
  pauses before the node executes and navigates to it; a large red arrow marks the paused node.
- Remove / Disable / Enable Breakpoint from the node or the Debugger window. A disabled breakpoint is an outline of a red
  octagon and the page prefers disabling to repeated remove and recreate.
- Breakpoints are saved in the project's `.ini` files: they persist between editor sessions but are not shared with
  other developers.
- An invalid breakpoint shows a yellow icon with an exclamation point and will never be reached; recompiling can fix it,
  otherwise hover for the warning.

## Watches
Right-click a pin's name > Watch this value (or Stop watching this value). A watched pin keeps the value from the most
recent execution of its node. While stopped at a breakpoint, hovering a pin shows an interactive tooltip. Pins whose
nodes have not executed show no value; even variable nodes only fetch their value when another node reads them.

## Debugger window
- Shows Breakpoints, Watchpoints and the Execution Trace stack, with stop, resume and step controls, and tabs for the
  full call stack and per-instance information.
- **Data Flow tab**: lists all instances of a chosen Blueprint class with object filtering, shows a consolidated call stack
  with current data when paused, lets you jump between Blueprints, and expands Arrays, Sets and Maps. It watches Blueprint
  classes that are open in the editor and part of the current call stack.
- **Call Stack**: shows flow between Blueprint functions and native C++ functions, current function at top. Blueprint
  Macros do not appear; they show as part of the calling function. To get the Blueprint call stack in an IDE, call
  `{,,UnrealEditor-Core}::PrintScriptCallstack()` in the Immediate window when stopped at a breakpoint (editor builds only).
- **Execution Trace**: nodes executed, most recent at the top, updating as you step.

## Checked
Date: 2026-11-07. Read in full: the Blueprint Debugger page (all sections), an unversioned en-us page with no engine
version stated. The skill's other source, `blueprint-debugging-in-unreal-engine`, returns empty text and was dropped.
Removed as not on the readable page: F9/F10/F11/Alt+Shift+F11/F5 shortcuts, the "debug object" toolbar dropdown, "Accessed
None" and "Infinite loop detected" messages and the loop-iteration limit default of 1,000,000, Print String Key and
Shipping behaviour, Visual Logger and `UE_VLOG`, Gameplay Debugger, `stat game`, and the Verify checklist.
Method: documentation only; no commands were run.
