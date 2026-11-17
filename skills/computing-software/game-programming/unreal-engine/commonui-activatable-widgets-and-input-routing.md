---
id: computing-software.game-programming.unreal-engine.commonui-activatable-widgets-and-input-routing
name: commonui-activatable-widgets-and-input-routing
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, umg, common-ui, input-routing, gamepad-navigation, input-action-data-table, controller-glyphs, game-programming]
level: advanced
status: docs-checked
description: "Set up Unreal Common UI input routing: CommonGameViewportClient, Input Action Data Tables, default Click/Back data and controller data assets for platform icons."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-plugin-for-advanced-user-interfaces-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-quickstart-guide-for-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CommonUI: input routing and controller data

**Goal:** menus that work with mouse, keyboard and gamepad, with the right button icons per platform.

## What Common UI provides (plugin page)
Common UI widgets, style data assets separating styling from UI elements, an Input Routing system giving widgets selective
interactivity (easier focus in multi-layered UIs), console-specific UI elements such as controller button icons, and
cardinal navigation management for gamepads.

## Setup (Quickstart guide)
1. **Viewport**: Edit > Project Settings > Engine > General Settings > Game Viewport Client Class = `CommonGameViewportClient`.
   Common UI sends captured input to the Viewport first, then to whichever root node is drawn on top. A custom viewport class
   must extend `CommonGameViewportClient`.
2. **Input Action Data Table**: Content Browser right-click > Miscellaneous > Data Table Asset, row structure
   `CommonInputActionDataBase`. Row fields: Display Name, Hold Display Name, Nav Bar Priority, Keyboard Input Type Info,
   Default Gamepad Input Type Info, Gamepad Input Overrides (for example swapping back and forward on Switch), Touch Input
   Type Info. These tables are separate from Project Settings input actions and the Advanced Input System, and used only for
   UI input. Examples named: `GenericInputActionDataTable` (Common UI content) and `NavigationInputActionDataTable`
   (Content Example project). Widgets reference a table plus row (for example the Triggering Input Action on
   `CommonButtonBase`). For fewer version-control conflicts, split actions across tables and reference them from one
   composite table.
3. **Default navigation**: create a Blueprint from `CommonUIInputData`, give it a Data Table with default Click and Back
   actions, and assign it at Project Settings > Game > Common Input Settings > Input Data. Click stands in for mouse
   clicks when highlighting widgets; Back navigates to the previous menu. Cardinal navigation is native to the engine.
4. **Controller data**: Blueprint from `CommonInputBaseControllerData`; fields Input Type (Gamepad, Mouse and Keyboard,
   Touch), Gamepad Name (default is Generic), Input Brush Data Map, Input Brush Key Sets (several keys to one element, for
   D-pads). Add them under Project Settings > Game > Common Input Settings > Platform Input, in the Controller Data array of
   the platform. The Default Gamepad Name must exactly match a Gamepad Name or its icons will not appear.
5. **Widgets and styles**: Common UI widgets appear in the UMG Palette under Common UI Plugin. They use Common Style Assets
   (Blueprint of a Common Style class) instead of base UMG styling; unassigned widgets use Template Styles from Project
   Settings > Plugins > Common UI Editor. Project Settings > Plugins > Common UI Framework holds a Default Throbber
   Material and Default Image Resource Object.

## Checked
Date: 2026-11-07. Read in full: the Common UI plugin page (a short overview) and the Common UI Quickstart Guide (all five
sections), unversioned en-us pages with no engine version stated. The Lyra sample page, a third source, was read and
contains nothing on Common UI, so it was dropped.
Removed as not on the pages: all material on `UCommonActivatableWidget`, `UCommonActivatableWidgetStack`/Queue,
`GetDesiredFocusTarget`, `NativeOnHandleBackAction`, `GetDesiredInputConfig`/`FUIInputConfig`, `UCommonBoundActionBar`,
`UCommonActionWidget`, `RegisterUIActionBinding`, Build.cs module names, "Enable Enhanced Input Support (UE 5.2+)",
the layer names, the pitfalls and the Verify checklist. The skill id keeps its original name though activatable widgets
are not covered by the sources; that content needs a page that documents it.
Method: documentation only; no commands were run.
