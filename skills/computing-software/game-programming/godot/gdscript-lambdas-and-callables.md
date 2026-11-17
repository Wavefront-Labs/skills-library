---
id: computing-software.game-programming.godot.gdscript-lambdas-and-callables
name: gdscript-lambdas-and-callables
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, gdscript-lambda, callable, first-class-functions, closures, game-programming]
level: practitioner
status: verified
description: "Use GDScript 2.0 lambdas and first-class functions: Callable syntax, capture-by-value rules, call/callv, array map/filter/reduce/sort_custom and lambda pitfalls."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#lambda-functions", "https://docs.godotengine.org/en/stable/classes/class_callable.html", "https://docs.godotengine.org/en/stable/classes/class_array.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript lambdas and first-class functions

## Syntax
```gdscript
var double := func(x: int) -> int: return x * 2
print(double.call(4))                      # 8; lambdas are Callables, invoke with call()

var on_hit := func(dmg):
    health -= dmg
    if health <= 0:
        died.emit()

var f: Callable = _on_timeout             # a method reference is a Callable too
f.call()
var named := func spawn_enemy(): pass     # optional name shows in the debugger/stack traces
```

## Captures (the big gotcha)
Lambdas capture **local variables by value at creation time**:
```gdscript
var count := 0
var inc := func(): count += 1   # modifies the lambda's copy, outer count stays 0
inc.call(); print(count)        # 0
```
- Capture a container or object instead: `var state := {"count": 0}` then `state.count += 1`
  (Arrays/Dictionaries/Objects are references, so mutation is shared).
- Member variables (`self.health`) are accessed through `self`, so changes are visible (run: a lambda doing `member += 5` changed the member).
- Loop variables captured in a `for` loop each get that iteration's value (good for button binds).

## Collection helpers
```gdscript
var alive := enemies.filter(func(e): return e.health > 0)
var names := alive.map(func(e): return e.name)
var total := scores.reduce(func(acc, s): return acc + s, 0)
enemies.sort_custom(func(a, b): return a.global_position.distance_squared_to(p) < b.global_position.distance_squared_to(p))
var any_boss := enemies.any(func(e): return e.is_boss)
```
`sort_custom` must return true when `a` should come before `b` and be a strict ordering.

## Callables
- `call(args...)`, `callv([args])`, `call_deferred(args...)`, `bind()`/`unbind()`.
- `is_valid()`: false when the bound object was freed. A lambda that captured a freed node logs `Lambda capture at index 0 was freed. Passed "null" instead.` and then fails on use (run).
- Signals: `button.pressed.connect(func(): open_menu("inventory"))`. Disconnecting a lambda needs the
  same Callable instance: store it in a variable first.
- `Callable(obj, "method_name")` for dynamic names; `get_method()`, `get_object()` for introspection.

## Performance
Lambdas allocate; avoid creating them per frame in hot loops. Typed lambdas (`func(x: int) -> int`)
help the analyzer but don't remove the call overhead.

## Verify
- [ ] Counter-in-lambda bugs replaced with shared containers or members.
- [ ] Lambda signal connections that must be removed are stored and disconnected.
## Checked
Ran on Godot 4.7.2 headless: counter lambda leaves the outer `count` at 0 after two calls; `for i in 3` lambdas return 0, 1, 2; typed lambda `func(x: int) -> int`; named lambda prints as `spawn_enemy(lambda)`; `filter`-style helpers (`reduce`, `sort_custom`, `any`); `Callable(self, "_m")` with `get_method()`, `get_object()`, `is_valid()`; connect, `is_connected` and `disconnect` with a stored lambda; the freed-capture message above. `Callable` methods `bind`, `unbind`, `callv`, `call_deferred` exist in the 4.7.2 class reference. The performance paragraph is general advice, not measured.
