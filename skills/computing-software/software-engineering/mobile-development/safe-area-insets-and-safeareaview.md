---
id: computing-software.software-engineering.mobile-development.safe-area-insets-and-safeareaview
name: safe-area-insets-and-safeareaview
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, safe-area, safeareaview, react-native-safe-area-context, usesafeareainsets, safeareaprovider, insets, notch, home-indicator, status-bar, edge-to-edge, display-cutout, layout, expo-router]
level: practitioner
status: docs-checked
description: "Keep content clear of notches and system bars with react-native-safe-area-context: SafeAreaProvider, SafeAreaView edges, useSafeAreaInsets and initialWindowMetrics."
sources: ["https://docs.expo.dev/versions/latest/sdk/safe-area-context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe area insets with react-native-safe-area-context

**Goal:** keep content clear of notches, home indicators, status bars and other system furniture on
every device, without hand-measuring a different constant per phone.

The library exposes insets as data (a hook and a context) as well as a `SafeAreaView` component.

```bash
npx expo install react-native-safe-area-context
```

## The pieces
```tsx
import { SafeAreaProvider, SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

export default function App() {
  return (
    <SafeAreaProvider>                      {/* must wrap the app root */}
      <Layout />
    </SafeAreaProvider>
  );
}

function Layout() {
  const insets = useSafeAreaInsets();        // { top, bottom, left, right }: numbers
  return (
    <View style={{ paddingTop: insets.top, flex: 1 }}>
      <SafeAreaView edges={['bottom']}>      {/* pad only the bottom edge */}
        <Footer />
      </SafeAreaView>
    </View>
  );
}
```

- **`SafeAreaProvider`** must wrap the app root for any of the components or hooks to work. The
  docs note it may also be required at modal roots when using `react-native-screens`.
- **`SafeAreaView`** is a regular View with the safe area edges applied as padding (custom padding
  you set is added to the safe-area padding). `edges` defaults to `["top", "right", "bottom", "left"]`;
  pass the subset you mean. `emulateUnlessSupported` defaults to `true` - on iOS 10+ it emulates the
  safe area using the status bar height and home indicator sizes.
- **`useSafeAreaInsets()`** returns `EdgeInsets` (`top`/`bottom`/`left`/`right` numbers) for direct
  use in styles. `SafeAreaInsetsContext.Consumer` gives the same data through the consumer API.
- **`initialWindowMetrics`** passed as the provider's `initialMetrics` prop speeds up the first
  render by avoiding an async measurement - but only valid when the provider does not remount, and
  not with `react-native-navigation`.

## View or hook?
The docs say to use `SafeAreaView` if you can: "It's implemented natively so when rotating the
device, there is no delay from the asynchronous bridge." The hook is described as "a more advanced
use-case" that "might perform worse than SafeAreaView when rotating the device". Use the hook when
you need the numbers, for example an absolutely positioned element or arithmetic like
`insets.top + headerHeight` (this use is a judgement, not stated by the page).

## Expo and web
Included in Expo Go, and **Expo Router sets up safe area context automatically**. On web under the
Expo Router provider, `useSafeAreaInsets()` and `useSafeAreaFrame()` return zero values and
`SafeAreaView` adds no safe-area spacing; the docs say to use CSS environment variables for web
safe-area spacing. Without Expo Router the provider supports web measurements, but CSS remains the
recommended approach. Plan a web branch for inset-dependent layout.

## Failure modes
- **No provider** - without Expo Router, add `SafeAreaProvider` in the app root; you may need it at
  other places too, including the root of modals and routes when using react-native-screens.
- **Double padding** - `SafeAreaView`'s safe padding plus your own `padding` on the same component
  (they add).
- **Nothing on web** - under Expo Router's provider the hook returns zero values and `SafeAreaView`
  adds no spacing; use CSS.
- **`initialMetrics` misuse** - you cannot use `initialWindowMetrics` if your provider remounts or
  you use react-native-navigation.
- **Lag on rotation** - the hook can perform worse than `SafeAreaView` when rotating.

## Verify
- [ ] `SafeAreaProvider` wraps the app root (and modal roots if `react-native-screens` is in use).
- [ ] On a notched iPhone and an Android with a display cutout: top and bottom content clear of
      system furniture in both orientations.
- [ ] Any `SafeAreaView` uses an explicit `edges` subset rather than the all-four default.
- [ ] Web layout uses the CSS safe-area properties, not RN insets.
- [ ] First render is not waiting on an inset measurement (pass `initialWindowMetrics` when the
      provider is stable).

## Checked
2026-11-08. Confirmed against the Expo SDK reference for react-native-safe-area-context: install
command, exports, `SafeAreaView` behaviour and the `edges` and `emulateUnlessSupported` defaults,
`useSafeAreaInsets` and `EdgeInsets`, provider guidance, Expo Router and web behaviour,
`initialWindowMetrics` limits. Removed: the claim about React Native core `SafeAreaView` (not on the
React Native View page), a dead GitHub source, and failure modes the page does not state.
Method: documentation only; no commands were run.
