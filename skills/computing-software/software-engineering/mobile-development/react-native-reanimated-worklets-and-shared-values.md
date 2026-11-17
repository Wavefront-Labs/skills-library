---
id: computing-software.software-engineering.mobile-development.react-native-reanimated-worklets-and-shared-values
name: react-native-reanimated-worklets-and-shared-values
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-reanimated, reanimated, worklets, shared-values, ui-thread, useanimatedstyle, withtiming, withspring, interpolate, layout-animations, babel-plugin, animation, gesture-animation, react-native-animation]
level: advanced
status: draft
description: "Animate on the UI thread with Reanimated worklets and shared values: babel plugin ordering, useAnimatedStyle, withTiming/withSpring, interpolate, runOnJS, layout animations."
sources: ["https://docs.swmansion.com/react-native-reanimated/", "https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/glossary", "https://docs.swmansion.com/react-native-reanimated/docs/api/animations/withTiming", "https://docs.swmansion.com/react-native-reanimated/docs/api/hooks/useAnimatedStyle", "https://docs.swmansion.com/react-native-reanimated/docs/api/LayoutAnimations/entryAnimations", "https://reactnative.dev/docs/animations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# React Native Reanimated: worklets and shared values

**Goal:** animate on the UI thread so frames keep rendering while the JS thread is busy, using
Reanimated's worklets and shared values instead of React Native's core `Animated` API.

Core `Animated` with `useNativeDriver: true` can only animate a fixed set of native-backed props
(transform, opacity) and still needs the JS thread to start and orchestrate the animation.
Reanimated runs the animation callback itself on the UI thread, so a long JS task (parsing a large
payload, a heavy render pass) does not stutter it.

## The babel plugin is not optional
Reanimated transforms worklet functions at build time. Add its plugin **last** in the plugins
array - this ordering requirement is the single most common setup failure:

```js
// babel.config.js
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    'react-native-reanimated/plugin',   // MUST be the last entry
  ],
};
```

Symptom of getting it wrong: worklets throw `TypeError: ... is not a function` at runtime, or the
build succeeds and a shared value reads back `undefined` on the UI thread. After changing babel
config, restart Metro with `npx react-native start --reset-cache` - a stale transform cache
reproduces the old broken output and makes the fix look like it did nothing.

## Worklets and shared values
A **worklet** is a function compiled so it can execute on the UI thread. Hooks such as
`useAnimatedStyle` treat their callback as a worklet automatically; a standalone function needs the
`'worklet'` directive as its first statement.

```tsx
import Animated, {
  useSharedValue, useAnimatedStyle, withTiming, Easing,
} from 'react-native-reanimated';

function Card() {
  const progress = useSharedValue(0);          // lives in UI-thread-accessible memory

  const style = useAnimatedStyle(() => ({      // this callback IS a worklet
    opacity: progress.value,
    transform: [{ scale: 0.9 + 0.1 * progress.value }],
  }));

  const show = () => {
    progress.value = withTiming(1, { duration: 220, easing: Easing.out(Easing.quad) });
  };

  return <Animated.View style={[styles.card, style]} />;
}
```

Rules that cause most bugs:
- Only `Animated.*` components accept animated styles. Passing a `useAnimatedStyle` result to a
  plain `View` silently does nothing.
- A worklet can only close over shared values, other worklets, or primitives captured when it was
  created. Reading a React state variable inside a worklet captures the value from the render that
  created it and never updates. Put it in a shared value instead.
- You cannot call React state setters or arbitrary JS host functions from a worklet. Bridge back
  with `runOnJS`:

```tsx
const onEnd = () => { runOnJS(setCompleted)(true); };   // setCompleted runs on the JS thread
```

## Animation builders
| Builder | Use |
|---|---|
| `withTiming(to, {duration, easing}, cb)` | deterministic duration; the default easing is not linear, so pass `Easing` explicitly when the curve matters |
| `withSpring(to, {damping, stiffness, mass, restDisplacementThreshold, restSpeedThreshold})` | physical feel; `damping` and `stiffness` are the two you tune first |
| `withDecay({velocity}, cb)` | momentum after a gesture; feed it the gesture's `velocityX`/`velocityY` |
| `withSequence(...anims)` | run in order |
| `withDelay(ms, anim)` | offset the start |
| `withRepeat(anim, times, reverse)` | loop; `times: -1` loops forever |
| `cancelAnimation(sv)` | stop and keep the current value |

Assigning a plain number (`progress.value = 1`) jumps immediately; assigning a builder animates.

## Interpolation and extrapolation
```tsx
const rotate = useDerivedValue(() => interpolate(
  scrollY.value, [0, 200], [0, 90], Extrapolation.CLAMP,
));
```
Always pass an extrapolation mode. The default extends the last segment linearly, so scrolling past
the final input stop keeps growing the output - the classic "header keeps scaling past the top"
bug. `Extrapolation.CLAMP` is what you want in most cases.

## Gestures drive worklets directly
Pair Reanimated with `react-native-gesture-handler` so the recogniser also runs on the UI thread.
With gesture-handler v2's `Gesture` API:

```tsx
const pan = Gesture.Pan()
  .onChange(e => { tx.value += e.changeX; })
  .onEnd(e => { tx.value = withDecay({ velocity: e.velocityX }); });

return <GestureDetector gesture={pan}><Animated.View style={style} /></GestureDetector>;
```

## Layout, entering and exiting animations
Attach as props on `Animated.*` components:

```tsx
<Animated.View entering={FadeInDown.duration(200)} exiting={FadeOutUp} layout={Layout.springify()}>
```
`layout` animates position and size changes when list items reorder or resize, which replaces
hand-rolling a transition for changing `FlatList` content. These fire through Reanimated's
mount/unmount machinery, so conditional rendering (`{show && <Animated.View .../>}`) works, but a
component hidden with `display: 'none'` never fires `exiting`.

## Failure modes
- **Animation jumps straight to the end value** - you assigned a builder to something that is not a
  shared value, or the babel plugin is missing so the worklet never compiled.
- **"Attempt to read property of undefined" inside a worklet** - the worklet captured a React value
  or an object unavailable on the UI thread. Capture primitives or shared values only.
- **Works on one platform but not the other** - usually a version mismatch between
  `react-native-reanimated` and `react-native-gesture-handler`. Check both against the published
  compatibility table rather than assuming the latest of each pair works together.
- **Reanimated 4.x requires the New Architecture.** An app still on the legacy bridge must pin the
  Reanimated major that supports it; upgrading Reanimated alone produces link-time or startup errors.

## Performance notes
- One `useAnimatedStyle` per animated view is cheaper than a single style object animating many
  views: a dependency change only re-evaluates the styles that actually use it.
- Do not read a shared value's `.value` on the JS thread during render - that forces a
  synchronisation. Keep reads inside worklets.
- `useDerivedValue` recomputes only when its dependencies change; prefer it over repeating the same
  `interpolate` call inside several `useAnimatedStyle` hooks.

## Verify
- [ ] `babel.config.js` lists `react-native-reanimated/plugin` last, and Metro was restarted with
      `--reset-cache` after any babel change.
- [ ] A long synchronous JS task (a button handler looping 10^8 times) does not interrupt an
      in-flight `withSpring` - that is the proof the animation is on the UI thread.
- [ ] No worklet reads React state directly; every cross-thread callback goes through `runOnJS`.
- [ ] Every `interpolate` call passes an explicit extrapolation mode.

*Unconfirmed at time of writing: the exact current Reanimated / gesture-handler version pairing, and
whether the target app is on the New Architecture. Check the compatibility table before pinning.*
