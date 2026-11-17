---
id: computing-software.game-programming.unreal-engine.cpp-base-class-blueprint-subclass-workflow
name: cpp-base-class-blueprint-subclass-workflow
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, blueprints, cpp-blueprint-workflow, base-classes, blueprintnativeevent, game-programming]
level: practitioner
status: docs-checked
description: "Expose a C++ Actor to Blueprint subclasses: UPROPERTY/UFUNCTION specifiers, BlueprintNativeEvent overrides, native vs Blueprint components, per Epic's LightSwitchBoth example."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/cpp-and-blueprints-example"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++ base class with Blueprint subclass workflow

**Goal:** programmers define a class in C++ that level designers extend in Blueprint.

## What the C++ and Blueprints example shows (Epic's LightSwitchBoth)
- A C++ Actor class (created with the C++ Class Wizard) that derives `AActor`. `Blueprintable` on `UCLASS()` is not needed
  here because Actor is Blueprintable and the specifier is inherited. Components, variables and functions of a code-only
  class would not be accessible to Blueprint graphs; specifiers make them so.
- Specifiers used:
  - Components `UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Switch Components")`: they appear in the My Blueprint
    tab and in the Components tab, where native components have dark blue icons (components added in the Blueprint are
    light blue).
  - `UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Switch Variables") float DesiredIntensity;` editable per instance
    and in Class Defaults, and readable and writable in graphs.
  - `UFUNCTION(BlueprintNativeEvent, Category="Switch Functions")` for overlap handlers. The C++ body is renamed with an
    `_Implementation` suffix; a Blueprint child can place an event that overrides it, and if no such event exists the C++
    implementation runs.
- First code class in a blank project: close the editor, compile in Visual Studio or Xcode, and reopen so the game module
  loads; make sure the Build Configuration matches the editor executable. For an existing C++ project the page says you
  can use Hot Reload to compile in the editor.
- Create the Blueprint with the C++ class as parent (page: `LightSwitchBoth_BP`). Inherited variables may be hidden until
  the "Show inherited variables" checkbox in My Blueprint is ticked.
- Construction Script in the child runs when the Actor is added or moved in the level and when `DesiredIntensity` changes
  (page example: sets the light intensity from it), so exposed values are visible immediately in the editor.
- Blueprint classes can be extended by other Blueprints (Class Viewer dropdown, or right-click > Create New Blueprint Based
  on This).

## Checked
Date: 2026-11-07. Read in full: the C++ and Blueprints example page (all text; header and source listings included).
Unversioned en-us page; its code carries a 1998-2018 copyright header, so the sample is old and shows a bare constructor
style; only the specifier behaviour described in prose is relied on. The second source (Blueprints Visual Scripting index)
was a short link page and contributed nothing checkable; it was dropped.
Removed as not on the page: the C++ vs Blueprint responsibilities table, `Abstract`, `BlueprintImplementableEvent`,
`TSubclassOf`/`TSoftObjectPtr` and asset-path guidance, data-only Blueprints, reparenting steps, nativization,
Live Coding vs restart rules, `ClassRedirects`, Blueprint diff, and the Verify checklist.
Method: documentation only; no commands were run.
