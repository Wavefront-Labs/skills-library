---
id: computing-software.software-engineering.mobile-development.keyboard-handling-and-avoidingview
name: keyboard-handling-and-avoidingview
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, keyboard, keyboardavoidingview, keyboard-events, keyboardavoiding, soft-input, adjustresize, softkeyboard, textinput, mobile-forms, keyboardverticaloffset, keyboard-dismiss, android-manifest, ios-keyboard]
level: practitioner
status: docs-checked
description: "Keep content above the soft keyboard: KeyboardAvoidingView behavior values, keyboardVerticalOffset, Keyboard events and the iOS/Android availability split."
sources: ["https://reactnative.dev/docs/keyboardavoidingview", "https://reactnative.dev/docs/keyboard", "https://developer.android.com/guide/topics/manifest/activity-element"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard handling: KeyboardAvoidingView and the Keyboard API

**Goal:** inputs stay visible when the soft keyboard opens, without a hidden field, white gap or
jitter.

## KeyboardAvoidingView
The component "will automatically adjust its height, position, or bottom padding based on the
keyboard height to remain visible while the virtual keyboard is displayed."

```tsx
<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : undefined}
  keyboardVerticalOffset={headerHeight}
  style={{ flex: 1 }}
>
  <ScrollView keyboardShouldPersistTaps="handled">{form}</ScrollView>
</KeyboardAvoidingView>
```

| Prop | Values / type | Notes |
|---|---|---|
| `behavior` | `enum('height', 'position', 'padding')` | the docs say Android and iOS interact with this prop differently and that setting it is recommended on both |
| `contentContainerStyle` | View style | the style of the content container when `behavior` is `'position'` |
| `keyboardVerticalOffset` | number, default `0` | "the distance between the top of the user screen and the react native view, may be non-zero in some use cases" |
| `enabled` | boolean, default `true` | enables or disables the component |

The docs do not say which `behavior` value suits which screen; try each on both platforms. For
`keyboardVerticalOffset`, measure the height of whatever sits above your view (a header,
navigation bar or modal chrome) and test that the focused input stays visible. The page does not
describe a specific failure when it is omitted.

## The Keyboard API
```ts
import { Keyboard } from 'react-native';

const sub = Keyboard.addListener('keyboardDidShow', (e) => {
  // handle the event
});
sub.remove();                                  // EventSubscription

Keyboard.dismiss();                            // dismisses the active keyboard and removes focus
Keyboard.isVisible();                          // whether the keyboard is last known to be visible
Keyboard.metrics();                            // KeyboardMetrics | undefined, if visible
Keyboard.scheduleLayoutAnimation(event);       // sync a TextInput or accessory view with keyboard movement
```

Event names accepted by `addListener`: `keyboardWillShow`, `keyboardDidShow`, `keyboardWillHide`,
`keyboardDidHide`, `keyboardWillChangeFrame`, `keyboardDidChangeFrame`.

**Platform split:** the docs state that only `keyboardDidShow` and `keyboardDidHide` are available
on Android, so listen to those for cross-platform code. On Android 10 or below the events "will not
be fired" if your activity has `android:windowSoftInputMode` set to `adjustResize` or
`adjustNothing`. The Keyboard page does not document the event payload; check the type definitions.

## Android: windowSoftInputMode
```xml
<activity android:windowSoftInputMode="stateVisible|adjustResize" ... >
```
The Android manifest reference says `adjustResize` means "the activity's main window is always
resized to make room for the soft keyboard on screen", `adjustPan` pans the window contents so the
focus is not obscured, and `adjustNothing` leaves the activity responsible for making room using
window insets. With `adjustUnspecified` (the default) the system resizes if the window has a
scrollable layout view. One `state...` value may be combined with one `adjust...` value; setting
multiple values in a group has undefined results. React Native's docs do not describe how
`KeyboardAvoidingView` combines with each mode, so test the pair on a device and avoid applying two
adjustments to the same screen.

## Verify
- [ ] On both platforms: focus the lowest input in a form inside a headered screen. It stays
      visible.
- [ ] The Android build declares `windowSoftInputMode` deliberately.
- [ ] Every `Keyboard.addListener` uses an event that exists on the target platform, and its
      subscription is removed on unmount.
- [ ] Keyboard state after backgrounding and foregrounding is correct.

## Checked
2026-11-08. Confirmed against reactnative.dev KeyboardAvoidingView and Keyboard pages (last updated
2026-10-27) and the Android activity element reference: prop names, `behavior` enum, defaults, the
quoted descriptions, the Android event-availability note, the six event names, `dismiss`,
`isVisible`, `metrics`, `scheduleLayoutAnimation`, and all `windowSoftInputMode` values quoted.
Removed because the pages do not state them: which `behavior` value is most reliable, white-gap and
jitter causes, a claim that `adjustResize` makes `KeyboardAvoidingView` redundant, the
`keyboardShouldPersistTaps` explanation, the `endCoordinates` payload, and the tap-outside dismiss
recipe.
Method: documentation only; no commands were run.
