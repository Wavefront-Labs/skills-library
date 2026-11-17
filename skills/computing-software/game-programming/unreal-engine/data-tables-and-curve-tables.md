---
id: computing-software.game-programming.unreal-engine.data-tables-and-curve-tables
name: data-tables-and-curve-tables
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, data-table, curve-table, ftablerowbase, csv-import, data-driven-design, data-tables-tuning, game-programming]
level: practitioner
status: docs-checked
description: "Drive Unreal game data from Data Tables and Curve Tables: FTableRowBase row structs, CSV import and reimport, import options, row handles, interpolation types and soft references."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data Tables and Curve Tables

**Goal:** designers edit stats in a spreadsheet; the game reads them by row name; balancing changes need no
code.

## Data Tables
A Data Table holds related data where fields can be any valid UObject property, including asset
references. A programmer must first create the row container so the engine knows how to interpret the data:
a `USTRUCT` that inherits from `FTableRowBase`. Columns map 1:1 to the struct's variables.
```cpp
USTRUCT(BlueprintType)
struct FLevelUpData : public FTableRowBase
{
    GENERATED_USTRUCT_BODY()
    // one UPROPERTY per column (the page's example has XPtoLvl, AdditionalHP, AchievementIcon)
};
```
The first column is expected to be named `Name` and holds the row names used in game; each other column is
headed by a variable name:
```
Name,XPtoLvl,AdditionalHP,AchievementIcon
2,1000,9,"Texture2d'/Game/Textures/AchievementIcon2'"
```
The double quotes around the asset-type text matter for the property importer; without them the text is
imported as `Texture2d`.

## Importing and reimporting
1. Save the sheet as `.csv` (Epic's sample workflow uses a macro-enabled `.xlsm` with export buttons that
   produce the CSV).
2. In the editor, click Import in the Content Browser and choose the file.
3. Choose Import As: DataTable, CurveTable, Float Curve, Vector Curve or Linear Color Curve.
4. For a DataTable pick the Row Type from the drop-down.

Import options: **Ignore Extra fields** (true ignores extra fields, false warns), **Ignore Missing Fields**
(true ignores expected-but-missing fields, false warns), **Import Key Field** (explicit key field; if empty it
uses `Name` for JSON and the field found for CSV).

Double-click the object to view contents; right-click and choose Reimport to update it. The original file
path is used when reimporting.

## Data Curves and Curve Tables
- Data curves support floating-point types only. First column `Name`; each later column heading is an X
  value and the cells below are the Y values, so each row is a curve (the page's example has rows such as
  `Melee_Damage` with X values 0 to 3).
- Curve Tables hold two-dimensional numeric data; Simple Curves and Rich Curves are editable in the Curve
  Data Table Editor, with a graph button and a multi-curve view. Curves can be renamed or deleted by
  right-clicking. Create one in the Content Browser under Miscellaneous.
- On import as a Curve Table you choose an interpolation type: **Constant** (no interpolation, clamps to the
  previous known X), **Linear**, or **Cubic**.

## Hooking up data
Put a Blueprint-exposed `FDataTableRowHandle` or `FCurveTableRowHandle` variable on your class. It shows two
subfields: the table reference (DataTable or CurveTable) and `RowName`. The handles provide `FindRow()` and
`GetCurve()` helpers. For a `FCurveTableRowHandle` an `FRichCurve` pointer is returned; for a
`FDataTableRowHandle` you name the struct type in the template call, either the final struct or a parent.

Do not cache returned structs or curves beyond the local scope of a function, so that a re-import takes
effect immediately and no invalid pointers are used.

Use `TSoftObjectPtr` for asset columns: the page's texture column is lazy loaded, whereas a `UTexture` field
would load every asset whenever the table loads.

## Verify
- [ ] Reimporting the CSV changes values in play without code changes.
- [ ] Every row handle in content resolves to an existing `RowName`.
- [ ] Curve evaluation matches the spreadsheet at sample X values for the chosen interpolation type.

## Checked
Checked 2026-11-08 against the Data Driven Gameplay Elements page.
Confirmed: row struct and CSV format, import steps and options, curve table behaviour and interpolation types,
row handles, caching rule, soft-reference note.
Removed because the page does not state them: the weapon sample, `FindRow` argument details and warning
behaviour, `FScalableFloat`, Composite Data Tables, validators, JSON-vs-CSV advice, and the unreadable API
reference source.
Method: docs-only read of cited pages, 2026-11-08
