---
id: computing-software.software-engineering.mobile-development.mobile-animations-and-gestures
name: mobile-animations-and-gestures
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-animations, gestures, jetpack-compose, swiftui, shared-element-transitions, predictive-back, reduce-motion, haptics]
level: practitioner
status: draft
description: "Animate mobile UI and handle gestures: Compose animate*AsState, AnimatedVisibility, shared elements, SwiftUI animations, matchedGeometryEffect, reduced motion."
sources: ["https://developer.android.com/develop/ui/compose/animation/introduction", "https://developer.android.com/develop/ui/compose/touch-input/pointer-input", "https://developer.apple.com/documentation/swiftui/animations", "https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animations and gestures

**Goal:** motion that explains state changes, follows the finger, stays at frame rate, and respects
users who turn animations off.

## Compose
Pick the highest-level API that fits:
| Need | API |
|---|---|
| animate one value on state change | `animateDpAsState`, `animateColorAsState`, `animateFloatAsState` |
| show/hide | `AnimatedVisibility(visible) { .. }` with `enter`/`exit` transitions |
| swap content | `AnimatedContent(targetState) { state -> .. }`, `Crossfade` |
| size changes | `Modifier.animateContentSize()` |
| several values tied to one state | `updateTransition(state)` |
| gesture-driven / interruptible | `Animatable` + coroutines (`animateTo`, `snapTo`, `animateDecay`) |
| repeat | `rememberInfiniteTransition()` |
| screen-to-screen hero | `SharedTransitionLayout` + `Modifier.sharedElement(...)` |
```kotlin
val elevation by animateDpAsState(if (selected) 8.dp else 0.dp, label = "elevation")
val offsetX = remember { Animatable(0f) }
Modifier.pointerInput(Unit) {
    detectHorizontalDragGestures(
        onDragEnd = { scope.launch { offsetX.animateTo(0f, spring(stiffness = Spring.StiffnessMedium)) } }
    ) { _, drag -> scope.launch { offsetX.snapTo(offsetX.value + drag) } }
}.offset { IntOffset(offsetX.value.roundToInt(), 0) }
```
- Read animated values in the **layout or draw phase** (`Modifier.offset { }` lambda,
  `graphicsLayer { alpha = a }`) rather than composition, to avoid recomposing every frame.
- Prefer `spring()` for interruptible, physical motion; `tween` with Material easing for
  choreographed transitions.
- Gesture helpers: `Modifier.clickable`, `combinedClickable` (long press), `draggable`,
  `anchoredDraggable` (swipe-to-reveal, bottom sheets), `transformable` (pinch/rotate), `nestedScroll`.
- **Predictive back**: opt in with `android:enableOnBackInvokedCallback="true"` (app or activity level;
  `false` turns the animations off), and use `PredictiveBackHandler` (needs `androidx.activity:activity-compose`
  1.8.0 or higher) for custom back animations. Back interception via `KeyEvent.KEYCODE_BACK` is no longer supported.

## SwiftUI
```swift
withAnimation(.spring(duration: 0.35, bounce: 0.2)) { isExpanded.toggle() }
Text(title).transition(.move(edge: .top).combined(with: .opacity))
Image(item.image).matchedGeometryEffect(id: item.id, in: namespace)   // hero between views
.navigationTransition(.zoom(sourceID: item.id, in: namespace))       // iOS 18 zoom push
```
- Implicit `.animation(.default, value: x)` always with `value:` (the valueless form is deprecated).
- `PhaseAnimator` and `KeyframeAnimator` (iOS 17) for multi-step animations; `.contentTransition(.numericText())` for counters.
- Gestures: `DragGesture`, `MagnifyGesture`, `RotateGesture`, `LongPressGesture`, composed with
  `.simultaneously`, `.sequenced`, `.exclusively`; `@GestureState` resets automatically when the gesture ends.
- `.sensoryFeedback(.success, trigger: value)` for haptics (iOS 17); Android
  `LocalHapticFeedback.current.performHapticFeedback`.

## Reduced motion
- Android: honour "Remove animations" (animator duration scale 0); Compose animations respect it.
  Check `Settings.Global.ANIMATOR_DURATION_SCALE` for custom ones.
- iOS: `@Environment(\.accessibilityReduceMotion)`; replace movement/zoom with fades.
- Avoid parallax and large motion for core flows; never convey information only through animation.

## Performance
- Animate transforms and alpha (GPU-friendly) rather than layout size where possible.
- Keep durations short (150-300 ms for most UI); long animations feel slow.
- Profile with Compose recomposition counts / Layout Inspector and Instruments' Hitches template.

## Verify
- [ ] Animations interruptible (tap mid-animation does the right thing).
- [ ] Reduced-motion setting tested on both platforms.
- [ ] No dropped frames during animation on a mid-range device.
