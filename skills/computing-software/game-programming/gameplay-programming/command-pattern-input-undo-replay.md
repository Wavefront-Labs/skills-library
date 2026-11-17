---
id: computing-software.game-programming.gameplay-programming.command-pattern-input-undo-replay
name: command-pattern-input-undo-replay
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, command-pattern, undo-redo, input-handling, replay-system, ai-commands, level-editor, game-programming]
level: practitioner
status: draft
description: "Use the Command pattern in games: decoupling input from actions, letting AI and players share commands, undo/redo in editors and turn-based games, and input-recorded replays."
sources: ["https://gameprogrammingpatterns.com/command.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Command pattern: input, undo and replay

**Goal:** represent "do this action" as an object, so the same action can come from a key press, an
AI decision, a network packet or a replay file, and can be undone (Nystrom, GPP "Command").

## Input -> commands
```cpp
struct Command { virtual ~Command() = default; virtual void execute(Actor& a) = 0; };
struct JumpCommand  : Command { void execute(Actor& a) override { a.jump(); } };
struct FireCommand  : Command { void execute(Actor& a) override { a.fire(); } };

class InputHandler {
    std::unordered_map<Button, std::unique_ptr<Command>> bindings;   // rebinding = swap entries
public:
    Command* handle(const InputState& in) {
        for (auto& [btn, cmd] : bindings) if (in.pressed(btn)) return cmd.get();
        return nullptr;
    }
};
// game loop
if (Command* c = input.handle(state)) c->execute(player);
// AI uses the same commands:
if (Command* c = ai.decide(enemy)) c->execute(enemy);
```
Commands take the actor as a parameter, so any actor can be controlled by any source (possession,
demo mode, AI taking over a disconnected player).

## Undo/redo
Commands that change state capture what they need to revert:
```cpp
struct MoveUnitCommand : Command {
    Unit* unit; Vec2 to; Vec2 from;
    MoveUnitCommand(Unit* u, Vec2 t) : unit(u), to(t) {}
    void execute() { from = unit->pos; unit->moveTo(to); }
    void undo()    { unit->moveTo(from); }
};
```
Keep a history list and a cursor: executing a new command truncates the redo tail. Used in level
editors, puzzle/turn-based games (Into the Breach-style undo), strategy planning phases.
Gotchas: commands with side effects outside their target (random rolls, spawned objects) must
record those too (store the seed or spawned ids); cap history size or memory grows.

## Replays and networking
A stream of `(tick, playerId, command)` is a compact replay or a lockstep network message, provided
the simulation is deterministic. Serialize commands as small structs (type id + parameters), not
function pointers.

## In modern engines
- Unity Input System actions / Unreal Enhanced Input actions already decouple devices from actions;
  the command layer sits after them: action callback -> create command -> execute or queue.
- In ECS, commands become components/events consumed by systems (e.g. a `MoveRequest` component).

## When not to
For trivial games, a direct `if (jumpPressed) jump();` is fine. Add the command layer when you need
any of: rebinding beyond what the input system provides, AI/player symmetry, undo, replay, or
networked input.

## Verify
- [ ] Player and AI drive the same character type through identical command classes.
- [ ] Undo after N random commands restores exact initial state (automated test).
- [ ] A recorded command stream replays to the same end state hash.
