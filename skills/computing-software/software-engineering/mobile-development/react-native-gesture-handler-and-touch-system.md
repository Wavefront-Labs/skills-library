---
id: computing-software.software-engineering.mobile-development.react-native-gesture-handler-and-touch-system
name: react-native-gesture-handler-and-touch-system
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-gesture-handler, gesture-handler, gesturedetector, pan-gesture, tap-gesture, pinch-gesture, gesture-composition, native-recogniser, touch-system, panresponder, scrollview-conflict, uithread, mobile-gestures, swipe, drag-and-drop]
level: advanced
status: draft
description: "Handle touch with react-native-gesture-handler's native recognisers: GestureHandlerRootView, the Gesture v2 API, composing pan/pinch/rotation, and resolving ScrollView conflicts."
sources: ["https://docs.swmansion.com/react-native-gesture-handler/", "https://docs.swmansion.com/react-native-gesture-handler/docs/api/gestures/pan-gesture", "https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-composition", "https://docs.swmansion.com/react-native-gesture-handler/docs/guides/quickstart", "https://reactnative.dev/docs/gesture-responder-system"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# React Native gesture handling and the touch system

**Goal:** drive interaction from native gesture recognisers so gestures stay responsive while the JS
thread is busy, and so they win the fight against platform scroll views.

React Native's built-in responder system (`PanResponder`, `onStartShouldSetResponder`) negotiates
touches in JS. That negotiation costs a round trip per event and loses to a native `ScrollView` in
common cases, which is why a horizontal swipe inside a vertical list often does nothing. 
`react-native-gesture-handler` (RNGH) attaches real `UIGestureRecognizer`s on iOS and Android
`GestureDetector`s, so recognition happens natively and can begin before JS has processed anything.

## The root view is mandatory
Wrap the app root once. Omitting this is the most common reason gestures silently never fire:

```tsx
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Navigation />
    </GestureHandlerRootView>
  );
}
```

`flex: 1` matters: a root view with no size clips its children's hit area. Tests need it too -
without a root view, `fireEvent` gestures pass in Jest but fail on a device, which is a misleading
green build.

## Gesture API (v2 style)
Gestures are configured objects passed to a `GestureDetector`, not components:

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import { useSharedValue, useAnimatedStyle, runOnJS } from 'react-native-reanimated';

const pan = Gesture.Pan()
  .minDistance(8)                    // ignore jitter below this many pixels
  .activeOffsetX([-12, 12])          // or activate on horizontal movement past these bounds
  .onUpdate(e => { tx.value = e.translationX; ty.value = e.translationY; })
  .onEnd(e => { tx.value = withDecay({ velocity: e.velocityX }); })
  .runOnJS(false);                 // default: handlers run on the UI thread

const tap = Gesture.Tap()
  .maxDurationMs(200)
  .maxDistance(20)
  .onEnd(() => { runOnJS(onPress)(); });

return (
  <GestureDetector gesture={Gesture.Simultaneous(pan, tap)}>
    <Animated.View style={style} />
  </GestureDetector>
);
```

Lifecycle callbacks, in order: `onBegin` (touch down, not yet recognised) -> `onStart` (recognised,
initial values) -> `onUpdate` / `onChange` (continuous; `onChange` gives deltas since the previous
event) -> `onEnd` (succeeded) -> `onFinalize` (always, success or failure). Use `onChange` when you
need per-frame deltas and `onUpdate` when you need absolute translation.

Recogniser types: `Tap`, `Pan`, `LongPress`, `Fling`, `Pinch`, `Rotation`, plus `Native` to wrap a
platform view's own gestures and `Manual` for fully custom logic.

## Composition is how you solve conflicts
| Combinator | Behaviour |
|---|---|
| `Gesture.Simultaneous(a, b)` | both may be active at once - pinch plus rotate on the same view |
| `Gesture.Exclusive(a, b)` | the first to activate cancels the others; earlier arguments win |
| `Gesture.Race(a, b)` | first to activate wins, others cancel |

Order inside `Exclusive` is the priority. A common pattern is `Exclusive(longPress, pan)` so a hold
does not turn into a drag.

Useful modifiers: `shouldCancelWhenOutside(bool)`, `activateAfterLongPress(ms)`,
`failOffsetX/Y`, `activeOffsetX/Y`, `maxPointers`, `minPointers`, `requireExternalGestureToFail(g)`.

## Scroll views
A `ScrollView` owns a native recogniser that competes with yours. Two ways out:
- Set `activeOffsetX`/`activeOffsetY` on your gesture so the scroll view claims the axis you do not
  want. A horizontal swipe carousel inside a vertical list wants `activeOffsetX([-12, 12])` and
  `failOffsetY([-12, 12])`.
- Use `Gesture.Native()` with `shouldActivateOnStart` / `disallowInterruption` to control hand-off
  explicitly.

Prefer the built-in `ScrollView` from RNGH (`import { ScrollView } from 'react-native-gesture-handler'`)
when nesting custom gestures, since it participates in the same recogniser graph.

## Failure modes
- **Nothing fires at all** - missing `GestureHandlerRootView`, or the child is a plain `View` that
  does not forward touches. `GestureDetector` needs a child that accepts a ref.
- **Works on iOS, not Android** - the gesture is nested in a native view (WebView, MapView, a
  third-party video player) that consumes the touch. Wrap that view in `NativeViewGestureHandler`
  or set its platform-specific touch handling.
- **Handler runs but React state never updates** - the handler executed on the UI thread. Reading
  or writing React state there is a no-op or a crash; bridge with `runOnJS`.
- **Stale values inside a handler** - the closure captured a render's props. Keep animated numbers
  in shared values, not in state.
- **A drag activates while the user meant to scroll** - no `minDistance`/`activeOffset`, so the
  recogniser claims the touch on the first pixel of movement.

## Verify
- [ ] `GestureHandlerRootView` with `flex: 1` wraps the app root, including the test render helper.
- [ ] Each gesture states an activation condition (`minDistance`, `activeOffsetX/Y`, or
      `activateAfterLongPress`) rather than activating on first movement.
- [ ] Every handler that touches React state goes through `runOnJS`.
- [ ] Nested inside a `ScrollView` on both platforms: the intended axis wins and the other still
      scrolls.
- [ ] Composed gestures use an explicit combinator; priority order in `Exclusive` is deliberate.

*Unconfirmed at time of writing: the installed RNGH major version and whether the target app is on
the New Architecture, which changes whether the legacy `*GestureHandler` component wrappers are
still exported. Check the library's migration guide before mixing v1 component style with v2
`Gesture` style.*
