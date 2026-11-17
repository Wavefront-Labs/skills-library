---
id: computing-software.qa-testing-engineering.test-case-design.model-based-testing-graphwalker
name: model-based-testing-graphwalker
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [model-based-testing, graphwalker, state-transition-testing, test-generation, path-generators, mbt]
level: practitioner
status: docs-checked
description: "Generate tests from a state model with GraphWalker: model vertices and edges, implement them in code, choose generators and stop conditions, run online or offline."
sources:
  - https://graphwalker.github.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model-based testing with GraphWalker

**Goal:** let a tool walk the state model and generate test paths, so coverage of states and transitions scales with the model.

## Model
Vertices = states (where you verify), edges = actions (what you do). Created in GraphWalker Studio or as a JSON model (`models` holding `vertices` and `edges` with a `startElementId`):
```
v_LoggedOut --e_Login--> v_Basket --e_AddItem--> v_Basket
v_Basket --e_Checkout [basket.size > 0]--> v_Payment --e_Pay--> v_Confirmation
```
Edges can carry boolean guards and script actions that modify execution state while a path is generated.

## Install and run
The current GraphWalker (graphwalker-rs) is a native binary: `cargo install graphwalker` (needs Rust and Cargo) or a prebuilt release; no JVM or Maven. Implement each vertex check and edge action in your own harness and drive it from the generated path.
```
graphwalker offline -m login.json "random(edge_coverage(100))"
graphwalker online -s RESTFUL -p 8080 -m login.json "random(edge_coverage(100))"
```

## Generators and stop conditions
- Generators: random, quick random, weighted random, A*, shortest all paths, predefined path, and New York Street Sweeper (Chinese Postman). Only `random(edge_coverage(100))` is shown on the site; take the other spellings from the Generators reference.
- Stop conditions: edge or vertex coverage, reached element, time duration, path length, requirement coverage, combinable with AND/OR (see the Stop Conditions reference for syntax).
- Offline: `graphwalker offline -m login.json "random(edge_coverage(100))"` prints a generated path to execute elsewhere; online mode serves it over REST or WebSocket.

## Value
Long random walks find sequence-dependent defects (state leaks, cache issues) that scripted tests miss; changing the model regenerates tests.

## Gotchas
- Model complexity explodes; model one feature/area per model and link models via shared vertices.
- Random paths need a seed recorded for reproduction.

## Verify
Edge coverage 100% reported, and a failing run can be replayed from its seed or path.

## Checked

2026-10-28 Confirmed against: GraphWalker site (graphwalker-rs, CLI offline/online commands, JSON model, generator and stop-condition lists, guards and actions, seeds, multi-model shared states, cargo install). Removed or generalised: the Java `@GraphWalker` and Maven plugin workflow, `java -jar graphwalker-cli.jar`, GraphML, exact generator and stop-condition function spellings other than `random(edge_coverage(100))`, and the ISTQB Model-Based Tester source (page returned an error).

Method: documentation only; no commands were run.
