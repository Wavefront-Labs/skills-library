---
id: computing-software.game-programming.game-ai-programming.behaviour-tree-runtime-implementation
name: behaviour-tree-runtime-implementation
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, behaviour-trees, bt-runtime, behavior-tree, running-status, blackboard, decorators, game-programming]
level: advanced
status: verified
description: "Implement a behaviour tree runtime: node status contract, composites and decorators, resuming Running nodes, per-agent state vs shared tree data, aborts and blackboard."
sources: ["https://www.gamedeveloper.com/programming/behavior-trees-for-ai-how-they-work", "https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter06_The_Behavior_Tree_Starter_Kit.pdf", "https://www.behaviortree.dev/docs/learn-the-basics/BT_basics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing a behaviour tree runtime

## Contract
Every node `tick()` returns `Success`, `Failure` or `Running`. `Running` means "call me again next
tick and I'll continue". Nodes may have `onEnter` (first tick after not running) and `onExit/abort`
(cleanup when interrupted).

```python
SUCCESS, FAILURE, RUNNING = "Success", "Failure", "Running"
class Agent:
    def __init__(self): self.mem = {}                  # per-agent state, keyed by node
class Sequence:                                         # memory sequence: resumes at the running child
    def __init__(self, kids): self.kids = kids
    def tick(self, a):
        i = a.mem.get(id(self), 0)
        while i < len(self.kids):
            s = self.kids[i].tick(a)
            if s == RUNNING: a.mem[id(self)] = i; return s
            if s == FAILURE: a.mem[id(self)] = 0; return s
            i += 1
        a.mem[id(self)] = 0; return SUCCESS
    def abort(self, a):
        i = a.mem.get(id(self), 0)
        if i < len(self.kids): self.kids[i].abort(a)   # note: also fires when the sequence was idle (i = 0)
        a.mem[id(self)] = 0
```
(Python re-implementation of the usual C++ shape: `tick` returns a status, `abort` is virtual with a no-op default.)
Selector is the mirror image (first Success wins). Parallel ticks all children with a success/failure
policy. Decorators wrap one child: Inverter, Repeat(n), Cooldown, TimeLimit, Condition (blackboard check).

## Shared tree, per-agent state
Build the tree once (from data) and share it across agents. Store running indices, timers and
started-flags in a per-agent memory block (offsets assigned at build time, or a map keyed by node
id). The Game AI Pro behaviour tree starter kit chapter discusses controlling the memory allocation of BT nodes. Avoid
instantiating a node graph per agent unless agents are few.

## Reactive vs memory composites
- **Memory** composites resume at the running child (above): cheap, but higher-priority branches
  aren't re-checked while a long action runs.
- **Reactive** composites re-evaluate earlier children every tick and **abort** the running child if
  an earlier one now succeeds (e.g. "enemy visible" interrupts "patrol"). Unreal implements this as
  decorator observer aborts (Self / Lower Priority / Both).
- Event-driven trees avoid ticking from the root every frame: only re-evaluate on blackboard changes.

## Blackboard
Typed key-value store per agent (target, last known position, alert level). Conditions read it;
services/sensors write it. Keep actions free of perception queries; read the blackboard instead.

## Gotchas
- `abort` on an idle memory sequence still calls the abort of child 0, so make `abort` idempotent. Forgetting `abort` leaves animations, movement requests or reservations (cover points, attack
  tokens) active after an interrupt.
- Actions returning Running forever with no timeout: add TimeLimit decorators on anything that waits.
- Long `Sequence` of conditions every tick costs CPU; tick trees at a lower rate for distant agents.

## Debugging
Record per-tick node statuses per agent into a ring buffer and draw the tree with colours (green
success, red failure, yellow running); a timeline scrubber makes "why did it do that" answerable.

## Verify
- [ ] Unit tests: sequence/selector/parallel status tables and abort propagation.
- [ ] Interrupting a running Move action releases its movement request and reservations.

## Checked (2026-10-22)
- Ran the Sequence in Python with scripted leaves: statuses `[Running, Running, Success, Running]` for a three-child sequence where child b returns Running twice (resumes at b without re-ticking a: log `a, b, b, b, c`, then restarts at a); `abort` while b is running aborts b and resets the memory index; `abort` on a never-started sequence calls abort on child 0 (the gotcha added above).
- Game AI Pro ch. 6 (BT starter kit) text confirms Parallel nodes, abort of running behaviours and memory-allocation control (section 6.4.3); behaviortree.dev basics page lists RUNNING semantics (HTTP 200); Unreal observer aborts (Self, Lower Priority, Both) from Epic's decorator reference. The instance-memory claim about Unreal's BT was removed (not checked).
