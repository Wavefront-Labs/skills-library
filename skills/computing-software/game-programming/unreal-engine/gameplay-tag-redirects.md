---
id: computing-software.game-programming.unreal-engine.gameplay-tag-redirects
name: gameplay-tag-redirects
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, gameplay-tags, gameplay-tag-redirect, renaming-tags, core-redirects, game-programming]
level: intro
status: draft
description: "Rename or reorganise gameplay tags safely with GameplayTagRedirects, resave referencing assets, and remove redirects afterwards without breaking content."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-tags-project-settings-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Renaming gameplay tags with redirects

**Goal:** move `Status.Stun` to `Status.Debuff.Stun` without silently emptying tag fields across hundreds of assets.

## Why it's dangerous
Assets store tags by **name**. If a tag disappears from the tag list, properties referencing it load as
invalid; with "Clear Invalid Tags" on they are wiped on resave, otherwise they warn. There is no compile
error: abilities just stop being blocked.

## Rename in the editor
Tag Manager (Project Settings > GameplayTags > Manage Gameplay Tags) > right-click tag > **Rename**.
The editor adds a redirect and updates the ini.

## Redirect by hand
```ini
; Config/DefaultGameplayTags.ini
[/Script/GameplayTags.GameplayTagsSettings]
+GameplayTagRedirects=(OldTagName="Status.Stun",NewTagName="Status.Debuff.Stun")
```
- The **new** tag must exist in a tag source (or be native).
- Old name must **not** still be defined, or the redirect is ignored.
- Redirects apply at load time; C++ code using `RequestGameplayTag("Status.Stun")` also resolves.
  Native tag definitions in C++ must be updated by hand.

## Make it permanent
1. Add the redirect.
2. Resave referencing assets: Content Browser > find references (tag manager search or Reference Viewer
   for searchable names), or run the `ResavePackages` commandlet over affected content:
   `UnrealEditor-Cmd.exe <project> -run=ResavePackages -PackageFolderToResave=/Game/Abilities -AutoCheckOut`.
3. After everything is resaved and merged, remove the redirect (keeping it forever is harmless but
   clutters; removing too early breaks unsaved assets in other branches).

## Other places tags hide
- Data tables / CSVs with tag strings, config files (`+AbilityTags=...`), save games (persisted tag
  names: migrate on load), analytics strings.
- Blueprint literal tag pins are assets: resaving fixes them.

## Verify
- [ ] Log shows no "Invalid GameplayTag" warnings on loading all maps (`-run=ResavePackages` or cook).
- [ ] Old save files load and convert the tag.
