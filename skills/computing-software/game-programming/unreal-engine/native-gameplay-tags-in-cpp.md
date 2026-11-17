---
id: computing-software.game-programming.unreal-engine.native-gameplay-tags-in-cpp
name: native-gameplay-tags-in-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, gameplay-tags, native-gameplay-tags, ue-declare-gameplay-tag-extern, fgameplaytag, game-programming]
level: practitioner
status: docs-checked
description: "Define gameplay tags natively in C++ with UE_DECLARE_GAMEPLAY_TAG_EXTERN and UE_DEFINE_GAMEPLAY_TAG macros, add the GameplayTags module, and know what FNativeGameplayTag holds."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/GameplayTags/FNativeGameplayTag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native gameplay tags in C++

**Goal:** tags that C++ relies on are declared in code, not looked up by string at runtime.

## Macros (defined in `NativeGameplayTags.h`)
- `UE_DECLARE_GAMEPLAY_TAG_EXTERN`: in a `.h` file, declares a tag defined in a `.cpp` file.
- `UE_DEFINE_GAMEPLAY_TAG`: in a `.cpp`, defines a tag declared in a `.h`, without a tooltip comment.
- `UE_DEFINE_GAMEPLAY_TAG_COMMENT`: same, with a tooltip comment.
- `UE_DEFINE_GAMEPLAY_TAG_STATIC`: defines a tag available only to the defining file; do not pair it with a DECLARE.

The page's example:
```cpp
// In .h file
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Movement_Mode_Walking);

// In .cpp file
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Movement_Mode_Walking, "Movement.Mode.Walking", "Default Character movement tag");
```
Add the `GameplayTags` module to your project's `Build.cs` to use Gameplay Tags in C++. For a larger example the
page points to `LyraGameplayTags.h` / `.cpp` in the Lyra Sample Game.

## FNativeGameplayTag (API page)
The class holds a gameplay tag registered during static construction of the module and unregistered when the module
unloads. Registration is keyed on the native tag pointer, so if two modules register the same tag and one unloads,
the other keeps it registered. It converts to `FGameplayTag` (`operator FGameplayTag()`, or `GetTag()`);
`GetRegisteredNativeTags()` is a static accessor and `GetGameplayTagTableRow()` returns the table row.

## Other ways to define tags
Tags can also be added in Project Settings (GameplayTags section, with Import Tags From Config reading
`Config/DefaultGameplayTags.ini` and files in `Config/Tags`) or imported from Data Tables using the
`GameplayTagTableRow` row type. All three methods are configured under Project Settings > Project > GameplayTags.
Editing the tag `.ini` files by hand needs an editor restart to load.

## Verify
- [ ] The module's `Build.cs` lists `GameplayTags`.
- [ ] Each tag is declared in one header and defined once in one `.cpp`.

## Checked
Date: 2026-11-07.
Read in full: Gameplay Tags (Defining Gameplay Tags, Defining Tags with C++, Example Implementation, remaining
sections) and the FNativeGameplayTag API page (class description, constructor, function table). dev.epicgames.com.
Removed as unconfirmed: the `MyTags` namespace and `MYGAME_API` export code, `HasMatchingGameplayTag` /
`DynamicGrantedTags` usage, "UE 5.0+" gate, claims that native tags are greyed in the picker, `RequestGameplayTag`
cost and ensure behaviour, the Lyra singleton / `AddNativeGameplayTag` history, load-phase and redirect gotchas, and
the grep-based Verify step.
Method: documentation only; no commands were run.
