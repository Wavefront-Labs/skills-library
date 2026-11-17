---
id: computing-software.game-programming.unity.coroutines-and-yield-instructions
name: coroutines-and-yield-instructions
category: computing-software
field: game-programming
product: unity
tags: [unity, monobehaviour, unity-coroutines, yield-return, startcoroutine, waitforseconds, waituntil, stopcoroutine, ienumerator, game-programming]
level: intro
status: docs-checked
description: "Unity coroutines: IEnumerator and yield return, what stops them, StartCoroutine overloads and return value, where yield instructions resume, and allocation advice."
sources: ["https://docs.unity3d.com/Manual/Coroutines.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.StartCoroutine.html", "https://docs.unity3d.com/Manual/execution-order.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutines and yield instructions

**Goal:** spread work over several frames with coroutines, and know when they stop and resume.

## Basics
- A coroutine is a method that can suspend and resume later: return type `IEnumerator` with a
  `yield return` in the body. Variables and parameters are preserved between yields.
- Coroutines are not threads: synchronous work inside still runs on the main thread.
- Page example:
  ```csharp
  IEnumerator Fade() {
      Color c = renderer.material.color;
      for (float alpha = 1f; alpha >= 0; alpha -= 0.1f) {
          c.a = alpha; renderer.material.color = c;
          yield return null;                 // resume next frame
      }
  }
  // StartCoroutine(Fade());
  ```
- `yield return new WaitForSeconds(.1f)` adds a fixed delay. `yield return
  Awaitable.WaitForSecondsAsync(.1f)` works as an equivalent; yielding the generic `Awaitable<T0>` from a
  coroutine is not supported.

## Starting and stopping
- `StartCoroutine(IEnumerator)` returns a `Coroutine`. It returns at the first `yield return`, but you can
  `yield` the result to wait until it finishes. If the coroutine completes without yielding, it returns
  `null`. There is no guarantee coroutines end in the order they started.
- `StartCoroutine(string methodName, object value)`: string form has more runtime overhead but lets you use
  `StopCoroutine` with a specific method name. Page example: `StartCoroutine(nameof(DoSomething), 2.0f)`
  then `StopCoroutine(nameof(DoSomething))`.
- Stop with `StopCoroutine` and `StopAllCoroutines`. A coroutine also stops if `GameObject.activeSelf`
  becomes false or the MonoBehaviour is destroyed. Setting the MonoBehaviour `enabled = false` does not
  stop coroutines.
- Nesting: `yield return StartCoroutine(coroutineB())` pauses A until B finishes.

## When they resume
- `yield return null`: next frame. Yielding any type, including null, returns on a later frame unless
  stopped or finished.
- Execution-order page: `WaitForEndOfFrame` resumes at the end of the frame; `WaitForFixedUpdate` at the
  end of the fixed update step. The exact order between resuming coroutines and asynchronous tasks is not
  guaranteed. Regular .NET Tasks resume in the `Update` phase.

## Performance
Each coroutine creates an `IEnumerator` state machine; starting them frequently (for example per frame)
allocates. `yield return null` does not allocate; `new WaitForSeconds` does. Cache or pool
`WaitForSeconds` with fixed durations, avoid lambdas in `WaitUntil` and `WaitWhile`, and prefer
long-lived coroutines that loop with `yield return null`. Coroutines retain references to the owner and
captured variables, so make sure they end or are stopped. Profile to confirm.

## Edit mode
Primarily a runtime feature; they can run in Edit mode with `[ExecuteInEditMode]` or `[ExecuteAlways]`,
but the Edit mode update loop is less regular. The Editor coroutines package targets Edit mode.

## Checked
Date: 2026-11-07

Read in full: "Write and run coroutines", both `StartCoroutine` overloads with their examples, and the
"Event function execution order" page. The "Yield instruction reference" and "Analyzing coroutines"
sub-pages were not fetched, so the yield instruction table is limited to what these three pages state.

Removed because none of the pages confirm it: exact resume point of `yield return null` relative to
`Update`/`LateUpdate`, `WaitForSecondsRealtime`, `WaitUntil`/`WaitWhile` check timing, `timeScale 0`
behaviour of `WaitForSeconds`, `yield return asyncOperation` completion cases, the error when starting a
coroutine on an inactive GameObject, handle-versus-IEnumerator stop rules, "re-enabling does not
resume", "StopAllCoroutines only that component's" claim, exceptions ending a coroutine, the manager
ownership remark, "costs about as much as an Update", the SpawnWave sample and the Verify list.

Method: documentation only; no commands were run.
