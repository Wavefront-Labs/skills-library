---
id: computing-software.game-programming.unity.async-scene-loading-and-loading-screens
name: async-scene-loading-and-loading-screens
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-scenes, scenemanager, loadsceneasync, allowsceneactivation, loading-screen, scene-transition, async-operation, game-programming]
level: practitioner
status: docs-checked
description: "Load Unity scenes without freezing: LoadSceneAsync, progress and allowSceneActivation (the 0.9 stall), loading screens, fades and avoiding activation hitches."
sources: ["https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.LoadSceneAsync.html", "https://docs.unity3d.com/ScriptReference/AsyncOperation-allowSceneActivation.html", "https://docs.unity3d.com/ScriptReference/Application-backgroundLoadingPriority.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async scene loading and loading screens

**Goal:** switch levels with a responsive loading screen and no multi-second freeze.

## Basic pattern
```csharp
using UnityEngine; using UnityEngine.SceneManagement; using UnityEngine.UI;

public class SceneLoader : MonoBehaviour
{
    [SerializeField] CanvasGroup fade; [SerializeField] Slider bar;

    public async Awaitable Load(string sceneName)
    {
        DontDestroyOnLoad(gameObject);                     // loader survives the switch
        await FadeTo(1f);
        AsyncOperation op = SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Single);
        op.allowSceneActivation = false;
        while (op.progress < 0.9f)                          // loading phase reports 0..0.9
        {
            bar.value = op.progress / 0.9f;
            await Awaitable.NextFrameAsync();
        }
        bar.value = 1f;
        op.allowSceneActivation = true;                     // activation: Awake/OnEnable/Start of new scene
        await op;
        await FadeTo(0f);
        Destroy(gameObject);
    }

    async Awaitable FadeTo(float a)
    {
        while (!Mathf.Approximately(fade.alpha, a))
        { fade.alpha = Mathf.MoveTowards(fade.alpha, a, Time.unscaledDeltaTime * 3f); await Awaitable.NextFrameAsync(); }
    }
}
```
(Older versions: same logic in a coroutine with `yield return null` / `yield return op`.)

## The 0.9 rule
With `allowSceneActivation = false`, Unity stops `progress` at 0.9 and `isDone` stays false until you set
it true. Waiting for `isDone` before allowing activation is an infinite loop. While `isDone` is false the
AsyncOperation queue is stalled: a later operation such as `SceneManager.UnloadSceneAsync` does not run
until activation is allowed. Set it from a coroutine or a held operation reference, not from `Awake`.

## Where the hitch comes from
Async loading streams data on a background thread, but **activation** runs on the main thread:
deserialising the scene objects and calling every `Awake`/`OnEnable`/`Start`. Large scenes still
stutter at that moment. Mitigations:
- Keep the loading screen visible through activation (fade covers it).
- Move heavy init out of `Awake`/`Start` into spread-out steps over several frames.
- `Application.backgroundLoadingPriority` caps main-thread integration time per frame: Low 2 ms,
  BelowNormal 4 ms, Normal 10 ms, High 50 ms. Default is BelowNormal (UWP High, consoles Normal). It has
  no effect in the Editor. Raise it during loading screens, restore it for gameplay streaming.
- Split big levels into additive scenes or Addressables loaded progressively.

## Single vs additive
A persistent "Boot" scene plus additive content scenes gives more control (see unity additive scene
loading).

## Gotchas
- You can pass the scene name, or the full path shown in the Build Settings window. A bare name loads
  the first match in the list, so use full paths when names repeat.

## Verify
- [ ] Loading bar animates smoothly; no long frozen frame before activation.
- [ ] Profiler around activation shows which Awake/Start methods dominate.
- [ ] Memory returns to baseline after returning to the menu.

## Checked
2026-11-01. Confirmed against the allowSceneActivation, backgroundLoadingPriority and LoadSceneAsync
script references: the 0.9 stall, queue stall, per-priority integration limits, default, Editor
limitation, background-thread read plus main-thread integration, scene name or path forms. Removed
unconfirmed claims: Awaitable support versions, Single-mode unload and memory behaviour, timeScale and
UnloadUnusedAssets notes, the 100 ms figure.
Method: documentation only; no commands were run.
