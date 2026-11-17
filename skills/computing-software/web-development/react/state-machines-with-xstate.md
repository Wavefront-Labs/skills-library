---
id: computing-software.web-development.react.state-machines-with-xstate
name: state-machines-with-xstate
category: computing-software
field: web-development
product: react
tags: [xstate, state-machines, statecharts, actor-model, react]
level: advanced
status: docs-checked
description: "Modelling complex UI flows with XState v5: machines, guards, actions and invoked actors, useMachine and useActor in React, the visual editor, and when a reducer is enough."
sources:
  - https://stately.ai/docs/setup
  - https://stately.ai/docs/promise-actors
  - https://stately.ai/docs/invoke
  - https://stately.ai/docs/states
  - https://stately.ai/docs/xstate-react
  - https://stately.ai/docs/xstate-store
  - https://stately.ai/docs/inspector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State machines with XState

Use a state machine when a flow has many mutually exclusive states and transitions that must be impossible otherwise (checkout, uploads with retry, auth flows, multi-step wizards, media players). Boolean soup (`isLoading && !isError && hasRetried`) is the signal.

## 1. A machine (XState v5; v6 is in alpha at the time of the check)
```ts
import { setup, assign, fromPromise } from "xstate";

export const uploadMachine = setup({
  types: { context: {} as { file?: File; error?: string; retries: number },
           events: {} as { type: "SELECT"; file: File } | { type: "UPLOAD" } | { type: "RETRY" } | { type: "CANCEL" } },
  actors: { upload: fromPromise(({ input }: { input: { file: File } }) => api.upload(input.file)) },
  guards: { canRetry: ({ context }) => context.retries < 3 },
}).createMachine({
  id: "upload", initial: "idle", context: { retries: 0 },
  states: {
    idle: { on: { SELECT: { target: "ready", actions: assign({ file: ({ event }) => event.file }) } } },
    ready: { on: { UPLOAD: "uploading" } },
    uploading: {
      invoke: { src: "upload", input: ({ context }) => ({ file: context.file! }),
        onDone: "done",
        onError: { target: "failed", actions: assign({ error: ({ event }) => String(event.error) }) } },
      on: { CANCEL: "ready" },               // leaving the state cancels the invoked actor
    },
    failed: { on: { RETRY: { guard: "canRetry", target: "uploading", actions: assign({ retries: ({ context }) => context.retries + 1 }) } } },
    done: { type: "final" },
  },
});
```

## 2. In React
```tsx
import { useMachine } from "@xstate/react";
const [state, send] = useMachine(uploadMachine);
{state.matches("uploading") && <Spinner />}
<button disabled={!state.can({ type: "RETRY" })} onClick={() => send({ type: "RETRY" })}>Retry</button>
```
- `useActorRef` + `useSelector` for shared actors without re-rendering on every change.
- `@xstate/store` is a lighter event-driven store when you don't need full statecharts.

## 3. Tooling
- Stately visual editor / VS Code extension shows the statechart; inspect running actors with `@statelyai/inspect`.
- Test paths can be generated from a machine with `@xstate/graph` and `@xstate/test` (see the XState docs for the current API).

## 4. When not to
Simple forms, toggles, or fetch states: `useReducer` with a discriminated union `{ status: "idle" | "loading" | "error" | "success" }` gives most of the benefit with no dependency.

## Verify
- [ ] Impossible states are unrepresentable; every transition covered by tests; cancelling or unmounting stops invoked actors.

## Checked

Checked 2026-10-25 against the Stately docs repository (statelyai/docs, content/docs) and the XState releases. Confirmed: `setup({ types, actors, guards })` then `.createMachine`; `fromPromise` actors take `input` and are invoked with `src`, `input`, `onDone`, `onError`; an invoked actor starts when the state is entered and stops when it is exited; `state.can(event)` and `state.matches`; `useMachine` is an alias of `useActor`, and `useActorRef` with `useSelector` minimises re-renders; `@xstate/store` is a small event-based store (docs for 4.x, needs TypeScript 5.4+); `@statelyai/inspect` and `createBrowserInspector`; v6 packages are alpha releases. Replaced the model-based testing bullet with a pointer to the documented packages.

Method: documentation only; no commands were run.
