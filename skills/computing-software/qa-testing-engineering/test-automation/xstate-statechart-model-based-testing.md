---
id: computing-software.qa-testing-engineering.test-automation.xstate-statechart-model-based-testing
name: xstate-statechart-model-based-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [xstate, statechart-testing, state-transition-testing, model-based-testing, javascript]
level: practitioner
status: verified
description: "Test XState statecharts: unit-test transitions with actors, generate shortest and simple paths with @xstate/graph, and drive UI tests from the model."
sources:
  - https://stately.ai/docs/testing
  - https://stately.ai/docs/graph
  - https://stately.ai/docs/actors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing statecharts in code (XState)

**Goal:** when behaviour is modelled as an XState machine, test the machine directly and reuse it to generate end-to-end paths.

## Unit-test transitions (XState v5)
```ts
import { createActor } from "xstate";
import { checkoutMachine } from "./checkoutMachine";

test("payment failure returns to payment step with error", () => {
  const actor = createActor(checkoutMachine).start();
  actor.send({ type: "ADDRESS_SUBMITTED", address: validAddress });
  actor.send({ type: "PAYMENT_FAILED", reason: "declined" });
  const snap = actor.getSnapshot();
  expect(snap.matches("payment")).toBe(true);
  expect(snap.context.error).toBe("declined");
});
```
Provide fake implementations for actors/actions with `checkoutMachine.provide({ actors: { charge: fromPromise(async () => ok) } })` so tests do not hit the network.

## Generate paths from the model
```ts
import { getShortestPaths, getSimplePaths } from "@xstate/graph";

const paths = getShortestPaths(checkoutMachine, {
  events: [{ type: "ADDRESS_SUBMITTED", address: validAddress }, { type: "PAYMENT_FAILED", reason: "declined" },
           { type: "PAYMENT_OK" }],
});
for (const p of paths) {
  test(`reaches ${JSON.stringify(p.state.value)}`, async () => {
    for (const step of p.steps) if (step.event.type !== "xstate.init") await driveUi(step.event);   // map events to Playwright actions
    await assertUiState(p.state);                           // map states to UI assertions
  });
}
```
Shortest paths reach every state (state coverage); simple paths cover more transition sequences but grow fast. In a run of a 4-state checkout machine (xstate 5.33.3, @xstate/graph 3.0.4) `getShortestPaths` returned 5 paths (address, payment, payment via a failure, done, done via a failure) and `getSimplePaths` returned 5; every path's `steps` starts with a synthetic `xstate.init` step, hence the skip above. Version note: use `@xstate/graph` for path generation; the old `@xstate/test` 0.5.1 is still the npm `latest` but is marked deprecated ("Superseded by @xstate/test@2 ... for XState v6"), and xstate 6 is alpha only.

## Practice
- Keep a mapping of event -> UI action and state -> UI assertion; the model then drives many E2E cases.
- Use guards with explicit names so tests can provide them (`guards: { isValid: () => true }`).
- Visualise the machine in Stately's editor during review; it doubles as the state diagram.

## Gotchas
- Generated paths with unbounded loops explode; constrain events or use shortest paths.
- Delayed transitions (`after: { 5000: ... }`) need fake timers (`vi.useFakeTimers()` then `advanceTimersByTime(5000)` reached the target state) or `createActor(m, { clock: new SimulatedClock() })` with `clock.increment(5000)` (also worked).
- The model can be wrong; review it against requirements, not just against itself.

## Verify
Unit tests cover each transition including guard outcomes, and generated path tests reach every state.
