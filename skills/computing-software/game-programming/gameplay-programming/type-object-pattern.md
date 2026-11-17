---
id: computing-software.game-programming.gameplay-programming.type-object-pattern
name: type-object-pattern
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, type-object, data-driven-design, monster-breeds, inheritance-in-data, game-programming]
level: practitioner
status: draft
description: "Apply the Type Object pattern: one class whose instances define kinds (breeds), data-file authoring, inheriting/overriding fields between types, and engine data-asset equivalents."
sources: ["https://gameprogrammingpatterns.com/type-object.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type Object pattern

**Goal:** add new kinds of monster, weapon or item without a new subclass and a recompile; designers
define kinds in data (Nystrom, GPP "Type Object").

## Shape
```cpp
class Breed {
public:
    Breed(const Breed* parent, int health, const char* attack)
      : parent_(parent), health_(health), attack_(attack) {
        if (parent_) {                           // copy-down inheritance at load time
            if (health_ == 0) health_ = parent_->health_;
            if (!attack_)     attack_ = parent_->attack_;
        }
    }
    Monster* newMonster() const { return new Monster(*this); }   // type object acts as factory
    int health() const { return health_; }
    const char* attack() const { return attack_; }
private:
    const Breed* parent_; int health_; const char* attack_;
};
class Monster {
    friend class Breed;
    explicit Monster(const Breed& b) : health_(b.health()), breed_(b) {}
    int health_; const Breed& breed_;            // per-instance state + pointer to its type
public:
    const char* attack() const { return breed_.attack(); }
};
```
```json
{ "Troll":         { "health": 25, "attack": "The troll hits you!" },
  "Troll Archer":  { "parent": "Troll", "health": 0, "attack": "The troll archer fires an arrow!" },
  "Troll Wizard":  { "parent": "Troll", "attack": "The troll wizard casts a spell!" } }
```

## Design choices
- **Copy-down vs delegate inheritance:** copy parent values at load (fast lookups, types immutable at
  runtime) or forward to the parent on each access (supports live edits). Copy-down is the usual choice.
- **Behaviour:** type objects hold data well, behaviour poorly. Options: a fixed set of behaviour
  ids the type picks from, a Strategy/Component reference, or a bytecode/script (see `bytecode-vm-for-designer-scripting`).
- Validate data at load: unknown parent, cycles, missing required fields.
- Compared with Flyweight: same sharing, but Type Object is about defining kinds as data; Flyweight is
  about memory.

## Engine equivalents
Unity ScriptableObject definitions (`EnemyDefinition`) referenced by one Enemy prefab; Unreal Primary
Data Assets or Data Table rows; Godot custom `Resource` classes (`class_name EnemyType extends
Resource`). Inheritance between definitions: Unity has none built in (implement parent lookup);
Unreal Data Asset subclasses or Blueprint class defaults.

## Pitfalls
- Runtime mutation of a type changes every instance (keep types read-only at runtime).
- Saves must store the type **id** (name/GUID), never a pointer or array index.
- Too many optional fields turns the type into a god-struct; split into components.

## Verify
- [ ] A new kind ships by adding data only.
- [ ] Load-time validation rejects bad parents and cycles with the file and key in the error.
- [ ] Save/load restores instances to the right type after reordering the data file.
