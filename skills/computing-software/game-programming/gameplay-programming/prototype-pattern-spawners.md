---
id: computing-software.game-programming.gameplay-programming.prototype-pattern-spawners
name: prototype-pattern-spawners
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, prototype-pattern, spawners, cloning, prefabs, data-inheritance, game-programming]
level: practitioner
status: docs-checked
description: "Apply the Prototype pattern: spawning by cloning configured instances, prefabs as prototypes, deep vs shallow copy pitfalls, and prototype-based data inheritance."
sources: ["https://gameprogrammingpatterns.com/prototype.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype pattern: spawners and data inheritance

**Goal:** create new objects by copying a configured example instead of hard-coding a class per
variant (Nystrom, GPP "Prototype").

## Spawner by cloning
```cpp
struct Monster { virtual ~Monster() = default; virtual std::unique_ptr<Monster> clone() const = 0; };
struct Ghost : Monster {
    int health, speed;
    Ghost(int h, int s) : health(h), speed(s) {}
    std::unique_ptr<Monster> clone() const override { return std::make_unique<Ghost>(*this); }
};
class Spawner {
    std::unique_ptr<Monster> prototype;
public:
    explicit Spawner(std::unique_ptr<Monster> p) : prototype(std::move(p)) {}
    std::unique_ptr<Monster> spawn() const { return prototype->clone(); }
};
Spawner fastGhosts(std::make_unique<Ghost>(15, 3));   // a configured prototype, not a new class
```
One spawner class serves every monster type and configuration.

## Deep vs shallow copy
A `clone()` must decide between a deep and a shallow copy: if a cloned demon holds a pitchfork
object, does the clone get its own? Decide per field and copy mutable per-instance state so clones
do not mutate each other.

## Prototype data inheritance (designer data)
JSON/data entries can name a prototype to inherit from, overriding a few fields:
```json
{ "goblin":        { "health": 20, "attack": "club", "speed": 3 },
  "goblin_archer": { "prototype": "goblin", "attack": "bow" },
  "goblin_chief":  { "prototype": "goblin", "health": 60 } }
```
Resolve at load: copy prototype fields, apply overrides, detect cycles. This is the idea from
the Self language that the chapter describes: objects without classes, where failed lookups
delegate to a parent object and new objects are made by cloning.

## Checked
2026-11-01. Confirmed against Game Programming Patterns, Prototype chapter: spawner and clone()
idea, deep versus shallow clone question, Self language delegation and cloning. Removed: Unity,
Godot and Unreal spawn API claims, material sharing details, "hundreds of entries" figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Spawning 100 clones then mutating one leaves others unchanged (no accidental shared state).
- [ ] Data inheritance resolver rejects cycles and unknown prototypes with clear errors.
- [ ] Adding a monster variant requires only data/prefab changes, no new class.
