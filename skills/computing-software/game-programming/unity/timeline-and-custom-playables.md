---
id: computing-software.game-programming.unity.timeline-and-custom-playables
name: timeline-and-custom-playables
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, unity-timeline, playables, playabledirector, signals, cutscenes, game-programming]
level: advanced
status: draft
description: "Build cutscenes and sequenced gameplay with Timeline: PlayableDirector, bindings, signals, and custom PlayableAsset/PlayableBehaviour tracks and mixers."
sources: ["https://docs.unity3d.com/Packages/com.unity.timeline@1.8/manual/index.html", "https://docs.unity3d.com/Manual/Playables.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timeline and custom playables

**Goal:** designers sequence cutscenes in Timeline; code supplies custom tracks and binds runtime objects.

## Basics
- `PlayableDirector` plays a `TimelineAsset`. Tracks (Animation, Activation, Audio, Signal, Control,
  Cinemachine) bind to scene objects via the director's **bindings** (stored per director, not in the asset).
- Wrap Mode: Hold (keep last frame), Loop, None (reset and stop). Update Method: Game Time, Unscaled
  (cutscenes during pause), DSP (music sync), Manual.

Rebind at runtime (spawned player):
```csharp
foreach (var o in director.playableAsset.outputs)
    if (o.streamName == "Player") director.SetGenericBinding(o.sourceObject, playerAnimator);
director.Play();
director.stopped += _ => GameFlow.Resume();
```

## Signals
Signal Track + Signal Emitter markers + a `SignalReceiver` component mapping SignalAsset -> UnityEvent.
Use for "start dialogue", "spawn enemy". Emitters have *Retroactive* (fire if skipped past) and *Emit
Once* flags; set Retroactive when cutscenes can be skipped.

## Custom track (three classes)
```csharp
[Serializable] public class FadeBehaviour : PlayableBehaviour { public float alpha = 1; }

public class FadeClip : PlayableAsset, ITimelineClipAsset {
    public FadeBehaviour template = new();
    public ClipCaps clipCaps => ClipCaps.Blending;
    public override Playable CreatePlayable(PlayableGraph g, GameObject owner)
        => ScriptPlayable<FadeBehaviour>.Create(g, template);
}

[TrackColor(0, 0, 0)] [TrackClipType(typeof(FadeClip))] [TrackBindingType(typeof(CanvasGroup))]
public class FadeTrack : TrackAsset {
    public override Playable CreateTrackMixer(PlayableGraph g, GameObject go, int inputCount)
        => ScriptPlayable<FadeMixer>.Create(g, inputCount);
}

public class FadeMixer : PlayableBehaviour {
    public override void ProcessFrame(Playable p, FrameData info, object playerData) {
        var cg = playerData as CanvasGroup; if (!cg) return;
        float a = 0;
        for (int i = 0; i < p.GetInputCount(); i++)
            a += p.GetInputWeight(i) * ((ScriptPlayable<FadeBehaviour>)p.GetInput(i)).GetBehaviour().alpha;
        cg.alpha = a;
    }
}
```
- Mixer pattern = blending works for free; clip-only behaviours can't crossfade.
- Restore the original value in `OnPlayableDestroy` / `OnGraphStop` or preview leaves scene objects dirty.
- `ExposedReference<T>` for clip fields that point at scene objects.

## Playables API without Timeline
`AnimationPlayableUtilities.PlayClip(animator, clip, out graph)` or build an `AnimationMixerPlayable`
graph to play clips without Animator Controller states; always `graph.Destroy()`.

## Verify
- [ ] Skipping a cutscene (`director.time = duration; director.Evaluate()`) still fires retroactive signals.
- [ ] Spawned characters animate (bindings set before Play).
