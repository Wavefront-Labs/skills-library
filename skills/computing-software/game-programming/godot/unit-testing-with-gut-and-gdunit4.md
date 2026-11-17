---
id: computing-software.game-programming.godot.unit-testing-with-gut-and-gdunit4
name: unit-testing-with-gut-and-gdunit4
category: computing-software
field: game-programming
product: godot
tags: [godot, autoload, gdunit4, gut-testing, godot-unit-tests, game-programming]
level: practitioner
status: draft
description: "Unit-test Godot projects with GUT or gdUnit4: test structure, doubles for autoload-dependent code, scene runners, async tests and running headless in CI."
sources: ["https://gut.readthedocs.io/en/latest/", "https://github.com/MikeSchulze/gdUnit4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit testing with GUT and gdUnit4

**Goal:** automated tests for GDScript (and C# with gdUnit4) gameplay code, including code that uses
autoloads, running in CI.

## Choose
- **GUT** (Godot Unit Test): mature, GDScript only, simple `extends GutTest`.
- **gdUnit4**: GDScript and C#, fluent assertions, scene runner with input simulation, editor
  inspector integration.
Both install from the Asset Library into `addons/` and must be enabled in Project Settings > Plugins.

## GUT test
```gdscript
# res://test/unit/test_inventory.gd
extends GutTest
var inv: Inventory
func before_each(): inv = Inventory.new()
func after_each(): inv.free()          # or autofree(Inventory.new())
func test_add_stacks():
    inv.add(&"wood", 3); inv.add(&"wood", 2)
    assert_eq(inv.count(&"wood"), 5)
func test_emits_changed():
    watch_signals(inv)
    inv.add(&"stone", 1)
    assert_signal_emitted(inv, "changed")
```
Async: `await wait_seconds(0.2)` / `await wait_for_signal(obj.done, 2.0)`.

## gdUnit4 test
```gdscript
extends GdUnitTestSuite
func test_damage() -> void:
    var e := auto_free(Enemy.new())
    e.take_damage(30)
    assert_int(e.health).is_equal(70)
func test_jump_scene() -> void:
    var runner := scene_runner("res://player.tscn")
    runner.simulate_action_pressed("jump")
    await runner.simulate_frames(10)
    assert_float(runner.get_property("velocity").y).is_less(0.0)
```

## Code that uses autoloads
Autoloads exist during test runs (the test runner runs inside the project). For isolation:
- inject dependencies (`var events = EventBus` default, overridable in tests), or
- use doubles: GUT `double(load("res://autoload/save.gd")).new()` + `stub(d, "write").to_return(true)`;
  gdUnit4 `mock(SaveService)`.
- reset autoload state in `before_each` (provide a `reset()` method).

## CI (headless)
```bash
godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://test -gexit
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://test --ignoreHeadlessMode
```
Run `godot --headless --import` first on a clean checkout so resources are imported. Export JUnit XML
for CI reporting (both tools support it).

## Gotchas
- Leaked nodes in tests show orphan warnings; use autofree/auto_free.
- Tests depending on frame timing are flaky; simulate frames/inputs instead of waiting seconds.

## Verify
- [ ] CI job fails when a test fails (exit code checked).
- [ ] Tests pass when run individually and as a suite.
