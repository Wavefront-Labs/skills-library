---
id: computing-software.game-programming.unity.awaitable-and-async-await
name: awaitable-and-async-await
category: computing-software
field: game-programming
product: unity
tags: [unity, unity6, monobehaviour, unity-awaitable, unity-async-await, destroycancellationtoken, background-thread, mainthreadasync, cancellation, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity's Awaitable class for async/await: the static wait and thread-switch methods, Cancel, pooling caveat, and destroyCancellationToken caching."
sources: ["https://docs.unity3d.com/Manual/async-await-support.html", "https://docs.unity3d.com/ScriptReference/Awaitable.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour-destroyCancellationToken.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Awaitable and async/await

**Goal:** use Unity's `Awaitable` type (namespace `UnityEngine`, class implementing `IEnumerator`) as an
async return type and await target.

## What Awaitable is
- A custom Unity type that can be awaited and used as an async return type. The reference says it is
  usually a preferable alternative to .NET `Task` for asynchronous code in Unity, but the two differ.
- Instances are pooled and therefore not safe to `await` multiple times in the same method.
- Page example:
  ```csharp
  private async Awaitable DoSomethingAsync()
  {
      await LoadSceneAsync("SomeScene");
      await SomeApiReturningATask();
      await Awaitable.NextFrameAsync();
  }
  ```

## Members (from the reference tables)
| Member | Description on the page |
|---|---|
| `NextFrameAsync` | Resumes on the next frame |
| `FixedUpdateAsync` | Resumes on the next fixed update frame |
| `EndOfFrameAsync` | Resumes after all Unity subsystems have run for the current frame |
| `WaitForSecondsAsync` | Resumes after the specified number of seconds |
| `BackgroundThreadAsync` | Resumes on a ThreadPool background thread; completes immediately if already on one |
| `MainThreadAsync` | Resumes on the Unity main thread; completes immediately if already on it |
| `FromAsyncOperation` | Creates an Awaitable from an existing `AsyncOperation` |
| `Cancel` (instance) | Cancels it; if being awaited, the awaiter receives `System.OperationCanceledException` |
| `LogExceptionsAndForget` (instance) | Logs exceptions without an explicit result check |
| `IsCompleted` (property) | Whether it has run to completion |

## destroyCancellationToken
`MonoBehaviour.destroyCancellationToken` (`CancellationToken`, read only, in `UnityEngine`) is a token
raised when the MonoBehaviour is destroyed. The page notes you must cache it before you destroy the
MonoBehaviour object.

## Checked
Date: 2026-11-07

Read in full: the `Awaitable` class reference, the `destroyCancellationToken` property page and the
Manual "Asynchronous programming with the Awaitable class" page. The Manual page is only an index to
three sub-pages (Introduction, completion and continuation, code example reference); those were not
opened, and the method parameter lists (for example whether the waits accept a cancellation token) are
not shown on the reference, so none are claimed.

Removed because none of the pages confirm it: the DashAsync and BuildGridAsync samples, the "2023.1+"
version note, `Application.exitCancellationToken`, the claim that async methods do not stop on
destroy or disable and the resulting `MissingReferenceException` and Play Mode behaviour, the claim
that main-thread-only Unity APIs apply in background sections, the Task allocation and context
comparison, `async void` advice, the UniTask remark and the Verify list.

Method: documentation only; no commands were run.
