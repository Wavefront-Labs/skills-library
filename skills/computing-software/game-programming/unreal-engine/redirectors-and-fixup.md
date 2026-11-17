---
id: computing-software.game-programming.unreal-engine.redirectors-and-fixup
name: redirectors-and-fixup
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-asset-manager, redirectors, fix-up-redirectors, coreredirects, game-programming]
level: practitioner
status: draft
description: "Handle Unreal asset and code renames: object redirectors, Fix Up Redirectors, ResavePackages -fixupredirects, and CoreRedirects for C++ class, property and enum renames."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-redirectors-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/core-redirects-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Redirectors and fixing them up

**Goal:** rename/move assets and C++ types without breaking references across a team.

## Asset redirectors
Moving or renaming an asset in the Content Browser leaves an `ObjectRedirector` at the old path so
unloaded packages still resolve. They accumulate and cause problems: duplicate names, cook warnings,
"asset already exists" when recreating the old name, confusing source control.

## Fix up
- Content Browser: right-click folder > **Update Redirector References** (Fix Up Redirectors in older
  versions). Loads referencers, resaves them pointing to the new path, deletes redirectors.
- Commandlet: `UnrealEditor-Cmd.exe <Project>.uproject -run=ResavePackages -fixupredirects -autocheckout
  -projectonly -unattended`
- Show them: Content Browser filter "Show Redirectors".

## Team workflow
- Fix up requires checking out all referencers -> coordinate (locks) or do it at quiet times.
- Commit the moved asset, referencers and deleted redirectors **together**.
- Never delete redirector files outside the editor while referencers still point to them.

## C++ renames: CoreRedirects
```ini
; DefaultEngine.ini
[CoreRedirects]
+ClassRedirects=(OldName="/Script/MyGame.OldEnemy",NewName="/Script/MyGame.EnemyBase")
+PropertyRedirects=(OldName="/Script/MyGame.EnemyBase.HP",NewName="/Script/MyGame.EnemyBase.Health")
+StructRedirects=(OldName="OldStats",NewName="/Script/MyGame.CombatStats")
+EnumRedirects=(OldName="/Script/MyGame.EOldState",NewName="/Script/MyGame.EState",ValueChanges=(("EOldState::Dead","EState::Eliminated")))
+FunctionRedirects=(OldName="/Script/MyGame.EnemyBase.Hit",NewName="/Script/MyGame.EnemyBase.TakeHit")
+PackageRedirects=(OldName="/Script/OldModule",NewName="/Script/NewModule")
```
Without these, Blueprints and saved data referencing the old names lose values or fail to load. Keep
them until all assets are resaved (then they can be removed, but leaving them is harmless).

## Gotchas
- Renaming a C++ class used as a Blueprint parent without a ClassRedirect breaks the Blueprint
  (parent becomes missing).
- Moving assets between plugins/mount points changes package roots — fix up every referencer.

## Verify
- [ ] Redirector filter shows none in the project after fixup.
- [ ] Old Blueprints load with values intact after a property rename.
