---
id: computing-software.game-programming.godot.gdscript-enums-and-match
name: gdscript-enums-and-match
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, gdscript-match, enums, pattern-matching, export-enum, game-programming]
level: intro
status: verified
description: "Use GDScript enums and match statements: named enums as types, exporting enums, match patterns (literal, array, dictionary, binding, guards with when) and fallthrough rules."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#enums", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#match"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript enums and match statements

## Enums
```gdscript
enum State { IDLE, RUN, JUMP, FALL }          # named: State is a type
enum { TILE_GRASS, TILE_WATER = 10 }          # unnamed: constants in the class scope

@export var start_state: State = State.IDLE   # inspector dropdown
var state: State = State.IDLE

func _ready() -> void:
    print(State.keys()[state])                # "IDLE": enum values are ints; keys() gives names
    print(State.size())
```
- Values are `int`; typed `var state: State` warns when assigning unrelated ints (with static typing warnings on).
- Use from other scripts via `class_name`: `Player.State.RUN`.
- `@export_enum("Warrior", "Mage")` exports an int (or String) without declaring an enum.
- Save files: store the **name** (`State.keys()[s]`) if enums may be reordered; stored ints break.

## match
```gdscript
match state:
    State.IDLE, State.RUN:                 # multiple patterns
        _ground_move(delta)
    State.JUMP when velocity.y > 0.0:      # guard (in the Godot 4.2 docs onward)
        state = State.FALL
    State.FALL:
        _air_move(delta)
    _:                                     # wildcard default
        push_warning("unhandled state %s" % state)
```

## Pattern types
| Pattern | Example |
|---|---|
| literal / constant | `42`, `"jump"`, `State.RUN` |
| wildcard | `_` |
| binding | `var x` (captures the value) |
| array | `[1, var second, ..]` (`..` = open-ended) |
| dictionary | `{"type": "hit", "dmg": var d}` |
| multiple | `"a", "b"` |

```gdscript
match event_data:
    {"type": "damage", "amount": var amt}:
        health -= amt
    ["move", var dir]:
        position += dir
```

## Rules
- No fallthrough and no `continue`-to-next-branch in Godot 4 (the docs say the 3.x `continue` in match was removed in 4.0);
  first matching branch wins and execution continues below the `match`.
- Types must match: `1` does not match `1.0` (run: `match 1.0: 1:` takes the default branch); `"1"` does not match `1`.
- Dictionary and array patterns must match the size exactly (run: `{"type": "damage", "amount": var a}` did not match a
  dictionary with an extra key, and `["move", var d]` did not match a 3-element array); end the pattern with `..` to allow
  extra keys or elements (both `..` forms matched).

## Verify
- [ ] Every enum value handled or explicitly sent to `_`.
- [ ] Save/load round-trips enum fields after reordering the enum (if stored by name).
## Checked
Ran on Godot 4.7.2 headless: `State.keys()[state]` gives `IDLE`, `State.size()` is 4, unnamed enum constant `TILE_WATER` is 10; `when` guard branch taken; multiple patterns, dictionary and array patterns with and without `..`, literal type strictness; `@export_enum("Melee", "Ranged") var x: int` exports an int and `@export_enum("A","B") var s: String` exports a String (property list `hint=2`, types 2 and 4); the `int_as_enum_without_cast`, `int_as_enum_without_match` and `enum_variable_without_default` warning settings exist. Guard availability from the Godot 4.1, 4.2 and 4.3 docs (the 4.1 page has no pattern guards section, 4.2 does), and the `continue` removal note from the current GDScript reference.
