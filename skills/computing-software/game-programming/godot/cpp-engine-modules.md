---
id: computing-software.game-programming.godot.cpp-engine-modules
name: cpp-engine-modules
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-modules, cpp, scons, engine-source, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot C++ engine modules compiled with SCons: config.py, register_types, binding classes with ClassDB, building custom editors and templates, and module vs GDExtension."
sources: ["https://docs.godotengine.org/en/stable/engine_details/engine_api/custom_modules_in_cpp.html", "https://docs.godotengine.org/en/stable/engine_details/development/compiling/introduction_to_the_buildsystem.html", "https://docs.godotengine.org/en/stable/engine_details/architecture/object_class.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# C++ engine modules

**Goal:** native code that lives inside the engine binary, with full access to internals.

## Layout
```
godot/modules/summator/          (or a custom path with custom_modules=)
  config.py  SCsub  register_types.h  register_types.cpp  summator.h  summator.cpp
```
```python
# config.py
def can_build(env, platform): return True
def configure(env): pass
```
```python
# SCsub
Import("env")
env.add_source_files(env.modules_sources, "*.cpp")
```

## Class
```cpp
// summator.h
#include "core/object/ref_counted.h"
class Summator : public RefCounted {
    GDCLASS(Summator, RefCounted);
    int count = 0;
protected:
    static void _bind_methods();
public:
    void add(int p_value) { count += p_value; }
    int get_total() const { return count; }
};
// summator.cpp
void Summator::_bind_methods() {
    ClassDB::bind_method(D_METHOD("add", "value"), &Summator::add);
    ClassDB::bind_method(D_METHOD("get_total"), &Summator::get_total);
}
// register_types.cpp
void initialize_summator_module(ModuleInitializationLevel p_level) {
    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) return;
    GDREGISTER_CLASS(Summator);
}
void uninitialize_summator_module(ModuleInitializationLevel p_level) {}
```
Docs: a `doc_classes` folder in the module holds the class XML (here `Summator.xml`); the module's
`config.py` provides `get_doc_path()` returning it and `get_doc_classes()` listing the classes, and
`godot --doctool <path>` generates the XML.

## Build
```bash
scons platform=windows target=editor custom_modules=../my_modules
scons platform=windows target=template_release custom_modules=../my_modules
```
`custom_modules` takes a comma-separated list of directories of modules (converted to absolute paths).
If the module must work in the running project, recompile every export template you plan to use and
point each export preset at the custom template. A build option like `module_summator_enabled=no`
disables a module.

## Module vs GDExtension
Per the docs, GDExtension is generally better suited to custom game logic because it does not require
recompiling the engine after every code change; C++ modules are mainly for when GDExtension does not
suffice and deeper engine integration is required.

## Gotchas
- Keep modules outside the engine repo (`custom_modules`) so you do not copy sources in and out.
- `dev_build=yes` enables dev-only code, disables optimisation and generates debug symbols.

## Verify
- [ ] Editor and export templates for each target platform include the module; GDScript can call it.

## Checked
2026-11-08. Confirmed against the custom C++ modules page and the build system introduction: GDCLASS,
register_types hooks and MODULE_INITIALIZATION_LEVEL_SCENE, `can_build`/`configure`, `add_source_files`,
`custom_modules`, doctool and doc_classes, export template rebuild, `dev_build`, `target` values. Removed
unconfirmed claims: ADD_PROPERTY/ADD_SIGNAL usage, `-j8`, the comparison table rows on access and rebuild
frequency, and the `scu_build` benefit statement. The code samples are illustrative and were not run.
Method: documentation only; no commands were run.
