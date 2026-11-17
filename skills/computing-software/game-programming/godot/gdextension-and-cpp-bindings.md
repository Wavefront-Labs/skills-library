---
id: computing-software.game-programming.godot.gdextension-and-cpp-bindings
name: gdextension-and-cpp-bindings
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdextension, godot-cpp, native-module, scons, performance, binding-generator, extension-api, gdnative, c++, register-class, game-programming]
level: advanced
status: docs-checked
description: "Write a native C++ GDExtension for Godot 4 with godot-cpp: project layout, SCons build, .gdextension file, properties and signals."
sources:
  - https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/scripting/cpp/gdextension_cpp_example.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDExtension and C++ bindings in Godot

**Goal:** add native C++ classes to a Godot 4 project through godot-cpp, built as a shared library the editor loads.

## Setup
1. Prerequisites: a Godot 4 executable, a C++ compiler, SCons, and a copy of the godot-cpp repository.
2. Use the godot-cpp branch that matches the Godot version you target (for example branch `4.1` for Godot 4.1). `master` tracks Godot's `master`. An extension built for an earlier minor version should work in later minor versions, not the reverse. Extensions for 4.0 do not work in 4.1 and later.
3. Add godot-cpp as a Git submodule (or clone it) next to a `project/` folder (a Godot project for testing) and a `src/` folder (extension sources).

## Minimal class
- Header: include the binding header (`godot_cpp/classes/sprite2d.hpp`), put the class in `namespace godot`, derive from the engine class and add the `GDCLASS(Class, Parent)` macro. Declare `static void _bind_methods();`.
- `_bind_methods` tells Godot which methods and properties exist. `_process(double delta)` behaves like the GDScript `_process`.
- `register_types.cpp`: an initialize function calls `GDREGISTER_CLASS(Class)` when the level is `MODULE_INITIALIZATION_LEVEL_SCENE`. An `extern "C"` entry function (for example `example_library_init`) builds a `GDExtensionBinding::InitObject`, registers the initializer and terminator, sets the minimum initialization level and returns `init_obj.init()`.

## Build
- Use the `SConstruct` file the tutorial provides, placed beside `godot-cpp`, `src` and `project`, then run `scons platform=<platform>`. `platform=list` shows the options. The library lands in `project/bin/`.
- The default build is debug. For optimised builds use `target=template_release`.

## The .gdextension file
Place `gdexample.gdextension` in `project/bin/`:
- `[configuration]` has `entry_symbol` (the extern "C" entry function name), `compatibility_minimum` (stops older Godot versions loading it) and `reloadable = true`.
- `reloadable` reloads the extension on recompile without restarting the editor, and only works for debug builds.
- `[libraries]` maps platform, build type and architecture keys (for example `linux.debug.x86_64`) to library paths. Only the matching library is exported, so the data pack carries no incompatible libraries.

## Properties and signals
- Properties: add a member, a getter and a setter, bind both with `ClassDB::bind_method(D_METHOD(...), &Class::method)` and register with `ADD_PROPERTY(PropertyInfo(Variant::FLOAT, "name"), "set_x", "get_x")`. `PROPERTY_HINT_RANGE` with `"0,20,0.01"` sets minimum, maximum and step.
- Signals: declare with `ADD_SIGNAL(MethodInfo("name", PropertyInfo(...)))` in `_bind_methods`, and emit with `emit_signal("name", args...)`.
- To react to another object's signal use `other->connect("signal", Callable(this, "my_method"))`. `my_method` must be bound in `_bind_methods` first.

## Verify
- [ ] godot-cpp branch matches the target Godot version.
- [ ] The `.gdextension` library paths match the files in `project/bin/` for each platform and build type.
- [ ] The class appears as a node type in the editor and its properties show in the inspector.
- [ ] Release builds use `target=template_release`.

## Checked

2026-11-08. Read in full: gdextension_cpp_example.rst (godot-docs, master; the old html page has moved under tutorials/scripting/cpp). Confirmed the setup, code structure, SCons commands, .gdextension keys, properties and signals. Removed the unsourced claims comparing GDExtension with engine modules, the Variant marshalling advice, the hot-reload and crash behaviour remarks and the editor-versus-export build target claim; the page covers none of them.

Method: documentation only; no commands were run.
