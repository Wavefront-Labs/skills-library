---
id: computing-software.game-programming.unity.physics-simulation-mode-and-manual-simulate
name: physics-simulation-mode-and-manual-simulate
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, physics-simulate, simulation-mode, physics-scene, trajectory-prediction, game-programming]
level: advanced
status: docs-checked
description: "Control Unity physics stepping with Physics.simulationMode and Physics.Simulate: script-driven steps, local PhysicsScenes for trajectory preview, and re-simulation."
sources: ["https://docs.unity3d.com/ScriptReference/Physics.Simulate.html", "https://docs.unity3d.com/ScriptReference/Physics-simulationMode.html", "https://docs.unity3d.com/ScriptReference/PhysicsScene.Simulate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics simulation mode and manual Physics.Simulate

**Goal:** decide when physics steps instead of letting the engine step it automatically.

## Modes
`Physics.simulationMode` (a `SimulationMode` value) controls when Unity executes the physics simulation. `SimulationMode.FixedUpdate` is the automatic mode; `SimulationMode.Script` means you step physics yourself with `Physics.Simulate(step)`. Check the `SimulationMode` enum page for the full list of values.

## Manual stepping
`Physics.Simulate(float step)` advances physics by `step`. Call it when the simulation mode is `Script`. A step covers all stages of collision detection, rigidbody and joint integration, and filing of the physics callbacks (contact, trigger and joints).
- It does not cause `FixedUpdate` to be called; `MonoBehaviour.FixedUpdate` still runs at the `Time.fixedDeltaTime` rate whether or not the mode is `Script`.
- Passing framerate-dependent steps (such as `Time.deltaTime`) makes the simulation non-deterministic. Pass a fixed step every time. Steps greater than 0.03 are likely to produce inaccurate results.

```csharp
float timer;
void Update() {
    if (Physics.simulationMode != SimulationMode.Script) return;
    timer += Time.deltaTime;
    while (timer >= Time.fixedDeltaTime) {
        timer -= Time.fixedDeltaTime;
        Physics.Simulate(Time.fixedDeltaTime);
    }
}
```

## Local physics scenes (for example trajectory preview)
`PhysicsScene.Simulate(float step)` simulates only the physics associated with that `PhysicsScene`. A non-default physics scene belongs to a specific Scene, and only components in that Scene are affected. Non-default physics scenes must be simulated manually.

```csharp
extraScene = SceneManager.CreateScene("Scene", new CreateSceneParameters(LocalPhysicsMode.Physics3D));
SceneManager.SetActiveScene(extraScene);   // new GameObjects land in this scene
// each FixedUpdate:
extraScene.GetPhysicsScene().Simulate(Time.fixedDeltaTime);
```

- `PhysicsScene.Simulate` can be called in the Editor outside Play mode, with caution: it moves GameObjects with Rigidbodies. Outside Play mode a full simulation runs including contact generation, but contacts are not reported through the standard script callbacks (a safety measure so callbacks cannot delete objects in an undoable-less way).
- As with `Physics.Simulate`, use a fixed step for more deterministic results.

## Checked
Method: 2026-11-09 docs-only read of the Physics.Simulate, Physics.simulationMode and PhysicsScene.Simulate script reference pages in full. Removed claims the pages do not state: the Update mode, the Project Settings location and default, the Physics2D equivalent, the callbacks-inside-Simulate recursion warning, Physics.SyncTransforms advice, re-simulation recipe and PhysX determinism, and the Verify list. The SimulationMode enum page was not opened, so only FixedUpdate and Script (named in the Simulate page) are used.
