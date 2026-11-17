---
id: computing-software.game-programming.gameplay-programming.validating-designer-data
name: validating-designer-data
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, data-driven-design, data-validation, content-validation, asset-linting, game-programming]
level: practitioner
status: draft
description: "Catch broken designer data before it ships: schema and range checks, reference integrity, editor-time validation hooks, CI content validation and clear error reporting."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnValidate.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating designer data

**Goal:** missing references, out-of-range values and inconsistent tables are found when saved or in
CI — not by players.

## What to check
- **Schema**: required fields present, types right, enums valid.
- **Ranges**: HP > 0, drop weights >= 0, cooldown >= animation length, speed within sane bounds.
- **References**: assets exist, ids resolve (loot table entries, quest prerequisites, dialogue node
  links), no references to editor-only or test content in shipping assets.
- **Cross-record consistency**: unique ids, no cycles in prerequisites, level-scaling tables monotonic,
  localisation keys exist for every displayed string.
- **Budgets**: texture sizes, polycounts, number of spawners per level.

## Where to run
- On edit: Unity `OnValidate` (clamp/warn), custom inspectors with error boxes; Unreal
  `IsDataValid(FDataValidationContext&)` overrides and **Data Validation** plugin (validate on save,
  `EditorValidatorBase` subclasses for project rules); Godot `_validate_property` / `@tool` warnings
  (`_get_configuration_warnings` shows a node warning icon).
- On save/commit: pre-submit validation (Unreal "Validate Assets" on submit, Perforce triggers, git hooks).
- In CI: headless validation run over all content:
  - Unreal: `UnrealEditor-Cmd <proj> -run=DataValidation`
  - Unity: `-executeMethod Validation.RunAll` iterating `AssetDatabase.FindAssets("t:ItemData")`.
  - Custom JSON/CSV: JSON Schema validation step.

## Example rule
```csharp
#if UNITY_EDITOR
void OnValidate() {
    if (cooldown < castTime) Debug.LogWarning($"{name}: cooldown {cooldown} < cast time {castTime}", this);
    if (icon == null) Debug.LogError($"{name}: missing icon", this);
}
#endif
```

## Reporting
Errors must name the asset, field and fix ("Item 'Iron Sword' field Icon is empty"), link/select the asset
in editor, and CI should fail on errors while warnings are summarised.

## Gotchas
- Validation that's slow won't be run; keep per-save checks fast, heavy checks in CI.
- Rules owned by programmers but data owned by designers — review new rules with designers to avoid
  noise.
- Don't auto-"fix" silently in OnValidate (e.g. clamping) without telling the designer.

## Verify
- [ ] Introduce a broken reference: CI fails with a message naming asset and field.
- [ ] Full validation runs in under a few minutes on the whole project.
