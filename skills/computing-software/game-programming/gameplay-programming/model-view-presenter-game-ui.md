---
id: computing-software.game-programming.gameplay-programming.model-view-presenter-game-ui
name: model-view-presenter-game-ui
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, model-view-presenter, game-ui, ui-architecture, game-programming]
level: practitioner
status: draft
description: "Structure game UI with model-view-presenter: presenters bind game state to dumb views, event-driven updates, testable UI logic and no gameplay in widgets."
sources: ["https://gameprogrammingpatterns.com/observer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model-view-presenter for game UI

**Goal:** HUD and menu code that does not reach into gameplay objects and can be tested without
rendering.

## Roles
- **Model:** gameplay state (player health, inventory). Knows nothing about UI. Raises change
  events or exposes observable values.
- **View:** widgets only: `setHealth(float pct)`, `showItems(list)`, raises `onItemClicked(i)`.
  No game logic, no references to the model.
- **Presenter:** subscribes to the model, formats values, calls view setters; handles view events by
  issuing commands to gameplay (`EquipItemCommand`).

```csharp
class HealthPresenter : IDisposable {
    readonly Health model; readonly IHealthView view;
    public HealthPresenter(Health m, IHealthView v) { model = m; view = v;
        model.Changed += OnChanged; OnChanged(); }          // initial sync
    void OnChanged() => view.SetHealth(model.Current / model.Max, model.Current < model.Max * 0.25f);
    public void Dispose() => model.Changed -= OnChanged;    // avoid dangling listeners
}
```

## Why games benefit
- Polling-in-Update UIs read every value every frame; event-driven presenters update only on change.
- View swaps (new HUD skin, VR version) reuse presenters.
- Presenters are plain classes: unit test with a fake view.

## Pitfalls
- Initial state: always push current values on bind, or the view shows defaults until the first change.
- Lifetime: unsubscribe on view destroy; scene reloads otherwise call into destroyed widgets.
- High-frequency values (cooldown fill, compass) can poll in the view's tick through a presenter
  getter; events for those cost more than polling.
- Do not let presenters grow into god objects; one per screen region.

## Verify
- Unit test: fake view, change model, assert setter calls.
- Grep views for gameplay namespaces; there should be none.
