---
id: computing-software.game-programming.game-engine-architecture.typed-message-dispatch
name: typed-message-dispatch
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-system, message-dispatch, typed-events, event-bus, subscriber-handles, observer, type-erasure, game-programming, std-function-callbacks]
level: practitioner
status: draft
description: "Build a typed event/message dispatcher: per-type subscriber lists, subscription handles with automatic unsubscription, per-entity vs global channels, and dispatch costs."
sources: ["https://www.gameenginebook.com/", "https://gameprogrammingpatterns.com/observer.html", "https://github.com/skypjack/entt/wiki/Crash-Course:-events,-signals-and-everything-in-between"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed message dispatch

**Goal:** systems publish strongly typed events (`EnemyKilled`, `ItemPickedUp`) and others subscribe
without knowing each other, with no string ids, no casts in handlers, and no dangling subscribers
(Gregory GEA ch. 16.8 "Events and message passing").

## Dispatcher
```cpp
class EventBus {
    struct ListenerList { std::vector<std::pair<uint64_t, std::function<void(const void*)>>> fns; };
    std::unordered_map<std::type_index, ListenerList> lists;
    uint64_t nextId = 1;
public:
    class Handle {                                   // RAII: unsubscribes on destruction
        EventBus* bus = nullptr; std::type_index type = typeid(void); uint64_t id = 0;
    public:
        Handle() = default;
        Handle(EventBus* b, std::type_index t, uint64_t i) : bus(b), type(t), id(i) {}
        Handle(Handle&& o) noexcept { *this = std::move(o); }
        Handle& operator=(Handle&& o) noexcept { reset(); bus=o.bus; type=o.type; id=o.id; o.bus=nullptr; return *this; }
        ~Handle() { reset(); }
        void reset() { if (bus) bus->unsubscribe(type, id); bus = nullptr; }
    };
    template<class E, class F> [[nodiscard]] Handle subscribe(F&& f) {
        auto& l = lists[typeid(E)];
        uint64_t id = nextId++;
        l.fns.emplace_back(id, [fn = std::forward<F>(f)](const void* e) { fn(*static_cast<const E*>(e)); });
        return Handle(this, typeid(E), id);
    }
    template<class E> void publish(const E& e) {
        auto it = lists.find(typeid(E));
        if (it == lists.end()) return;
        auto snapshot = it->second.fns;              // copy: handlers may (un)subscribe during dispatch
        for (auto& [id, fn] : snapshot) fn(&e);
    }
    void unsubscribe(std::type_index t, uint64_t id) {
        auto& v = lists[t].fns;
        std::erase_if(v, [id](auto& p) { return p.first == id; });
    }
};
// usage
struct EnemyKilled { EntityId enemy; EntityId killer; int score; };
auto h = bus.subscribe<EnemyKilled>([&](const EnemyKilled& e) { score += e.score; });
bus.publish(EnemyKilled{id, player, 100});
```
Storing the `Handle` as a member ties subscription lifetime to the subscriber: no manual unsubscribe,
no calls into destroyed objects.

## Design choices
- **Global bus** vs **per-entity channels** (an entity's own dispatcher for `Damaged`, `Died`):
  per-entity avoids filtering by id in every handler.
- **Immediate** dispatch (above) vs **queued** (see game-engine-architecture event-queue-pattern).
- Event payloads small, by value, containing ids not pointers.
- In engines: Unreal multicast delegates (`DECLARE_MULTICAST_DELEGATE`), Unity C# events/`UnityEvent`,
  Godot signals; EnTT `dispatcher` (queue + sink) for ECS.

## Costs and debugging
`std::function` + hashing per publish is fine for gameplay events (hundreds per frame), not for
per-particle messages: use direct calls or data-oriented systems there. Add a debug mode that logs
event type, publisher and handler count.

## Verify
- [ ] Destroying a subscriber automatically removes its handlers (no crash on next publish).
- [ ] Handlers that subscribe/unsubscribe during dispatch behave deterministically.
- [ ] Unit tests cover multiple event types with no cross-delivery.
