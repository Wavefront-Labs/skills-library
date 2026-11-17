---
id: computing-software.game-programming.unreal-engine.game-feature-plugins-and-modular-gameplay
name: game-feature-plugins-and-modular-gameplay
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-framework, game-feature-plugin, modular-gameplay, game-feature-actions, game-programming]
level: practitioner
status: docs-checked
description: "Build Unreal Game Feature plugins with Modular Gameplay: setup, the GameFeatureData asset, the built-in actions, Add Components rules and registering receiver actors."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/GameFeatures/UGameFeatureAction_AddComponents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Game Feature plugins and modular gameplay

**Goal:** ship a feature as a standalone plugin that can be activated or deactivated, injecting components into
existing actors without the base code depending on the feature.

## Setup (per the Game Features and Modular Gameplay page)
1. Edit > Plugins: enable **Game Features** and **Modular Gameplay** (both in the Gameplay category), then restart.
2. Plugins window > Add: create a new plugin and select **Game Feature (Content Only)**.
3. Keep the plugin under `/Plugins/GameFeatures/` in your project.
4. In the plugin's top-level content folder create a Data Asset (Miscellaneous > Data Asset), choose the
   `GameFeatureData` class, and name it after the plugin.
The feature then loads when the engine or editor starts. After first creating a GameFeatureData asset you may need
to restart the editor once: these assets load at editor startup. Later edits do not need a restart.

## Actions
Open the Data Asset, expand ACTIONS, add elements to the Actions array and choose the action type. As many as needed.

| Action | Does |
|---|---|
| Add Cheats | Registers a Cheat Manager Extension; debug-only, not instantiated in Shipping builds |
| Add Components | Adds components to matching Actor classes on an opt-in basis (the most common action) |
| Add Data Registry | Adds a Data Registry asset to the project |
| Add Data Registry Source | Adds Data Tables to an existing registry; needs a DataTable Meta Source in the base registry |
| Add World Partition Content | Adds World Partition content to the feature |

## Add Components rules
- You list paired Actor and Component classes; the action tries to add an instance of each component to each
  matching actor. It can add on clients, servers or both (both by default).
- Components should come from the plugin itself and carry the feature's logic and data, with minimal interaction
  with the project's Actor subclass.
- Using the base `AActor` class is unsupported and that part of the action is ignored: name the narrowest actor
  classes, or use several Add Components actions when there is no common parent.
- The action's data is a `ComponentList` of `FGameFeatureComponentEntry` (API page; class
  `UGameFeatureAction_AddComponents`, display name "Add Components", see also `UGameFrameworkComponentManager`).

## Receivers
To receive components, an Actor must register with the `UGameFrameworkComponentManager` and pass itself to
`AddReceiver`, generally in `BeginPlay`, as the page shows:
```cpp
if (UGameFrameworkComponentManager* ComponentManager = GetGameInstance()->GetSubsystem<UGameFrameworkComponentManager>())
{
    ComponentManager->AddReceiver(this);
}
```

## Verify
- [ ] The plugin sits under `Plugins/GameFeatures` and its GameFeatureData asset lists the intended actions.
- [ ] An actor class that should receive components registers itself with `AddReceiver`.

## Checked
Date: 2026-11-07.
Read in full: Game Features and Modular Gameplay (Setup, Game Feature Actions, Adding an Action, Adding
Cheats / Components / Data Registries / Data Registry Sources) and the UGameFeatureAction_AddComponents API page
(variables list; the Functions section is empty on that page). Both from dev.epicgames.com.
Removed as unconfirmed by those pages: plugin activation states and `.uplugin` initial state, the
`PreInitializeComponents`/`EndPlay` receiver code and `SendGameFrameworkComponentExtensionEvent`, `AModularCharacter`
and similar classes, Lyra-style custom actions, `UGameFeaturesSubsystem` activation code, the dependency
direction, Asset Manager and cooking advice, and late-add behaviour. The old receiver code used static
`AddGameFrameworkComponentReceiver`; the page shows `AddReceiver` on the subsystem instead.
Method: documentation only; no commands were run.
