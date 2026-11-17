---
id: computing-software.game-programming.game-engine-architecture.component-pattern-composition
name: component-pattern-composition
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, entity-component-system, component-pattern, composition-over-inheritance, game-object-model, component-communication, game-programming-patterns, game-programming]
level: practitioner
status: draft
description: "Structure game objects with the Component pattern: replacing deep inheritance with composition, component communication options, ownership and update order, versus full ECS."
sources: ["https://gameprogrammingpatterns.com/component.html", "https://www.gameenginebook.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component pattern: composition over inheritance

**Goal:** game objects assembled from reusable parts (physics, graphics, input, AI) instead of a deep
class hierarchy where every new entity type forces awkward inheritance (Nystrom, GPP "Component";
Gregory GEA ch. 16.2 "Runtime object model architectures").

## The problem it solves
`GameObject -> Actor -> Pawn -> Character -> FlyingCharacter -> FlyingShootingCharacter`: features
end up duplicated across branches or pushed up into a "blob" base class. Components let each object be
a container of features:
```cpp
class GameObject {
    std::vector<std::unique_ptr<Component>> components;
public:
    template<class T, class... A> T& add(A&&... a) {
        auto c = std::make_unique<T>(std::forward<A>(a)...); T& r = *c; c->owner = this;
        components.push_back(std::move(c)); return r;
    }
    template<class T> T* get() { for (auto& c : components) if (auto p = dynamic_cast<T*>(c.get())) return p; return nullptr; }
    void update(float dt) { for (auto& c : components) c->update(dt); }
};
auto& bjorn = world.spawn();
bjorn.add<InputComponent>(); bjorn.add<PhysicsComponent>(); bjorn.add<GraphicsComponent>(sprite);
```
(Cache `get<>()` results; `dynamic_cast` lookup per frame is slow.)

## Communication between components (Nystrom's three options)
1. **Shared state on the container**: position/velocity on the GameObject that all components read and
   write. Simple; risks implicit coupling and update-order dependence.
2. **Direct references**: `PhysicsComponent` holds a pointer to the `GraphicsComponent` it drives.
   Fast and explicit; tighter coupling.
3. **Messaging**: the container broadcasts messages to its components (`receive(msg)`). Most decoupled;
   harder to trace.
Real engines mix them: Unity (GetComponent references + SendMessage/events), Unreal (Actor owns
components, components found via `FindComponentByClass`, delegates).

## Order and ownership
- Update order between components matters (input -> physics -> graphics): define it by component
  type or phases, not by insertion order.
- Components owned by their object; destroyed with it. Cross-object references via handles/ids.

## Component pattern vs ECS
Component pattern: components have data **and** behaviour, updated through their object (cache
unfriendly at scale, intuitive). ECS: components are pure data in packed arrays, systems hold behaviour
(see game-engine-architecture game-loop-and-entity-component-systems). Many engines use object-component
for gameplay and data-oriented systems for hot paths.

## Verify
- [ ] New entity types are created by combining existing components, not by subclassing.
- [ ] Component update order documented and enforced.
- [ ] No per-frame component lookups in hot code (cached references).
