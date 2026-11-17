---
id: computing-software.software-engineering.mobile-development.splash-screens-with-react-native-bootsplash
name: splash-screens-with-react-native-bootsplash
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-bootsplash, bootsplash, splash-screen, launch-screen, app-startup, hide-animation, boot-theme, generate-cli, expo-plugins, storyboard, drawable, cold-start, native-splash]
level: practitioner
status: docs-checked
description: "Show a native splash while the app boots and hide it on your terms with react-native-bootsplash: the generate CLI, native init snippets, hide with fade, useHideAnimation, Expo."
sources: ["https://github.com/zoontek/react-native-bootsplash", "https://reactnavigation.org/docs/navigation-container/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splash screens with react-native-bootsplash

**Goal:** a real native splash during cold start - no white flash, no JS-driven placeholder - that
hides once your app is actually ready.

The splash is an Android Drawable XML and an iOS Storyboard, shown by the OS before JS exists.
That is the point: it covers the window between process start and React mounting, which no JS
component can.

```bash
npm install --save react-native-bootsplash
cd ios && pod install
```

## Generating assets
The CLI is **`generate`** (migrating from v6: see the migration guide linked from the README):

```bash
npx react-native-bootsplash generate logo.svg \
  --platforms=android,ios,web \
  --background=F5FCFF \
  --logo-width=100 \
  --assets-output=assets/bootsplash \
  --flavor=main
```
It generates the assets, updates config files, and creates the Android Drawable XML and the iOS
Storyboard automatically. `--flavor` targets an Android build flavor. `--brand`/`--dark-*`
variants and 50+ density-specific files require a paid `--license-key`; the free path covers a
logo over a solid background.

## Wiring it natively (bare RN)
iOS - in `customize(_ rootView: RCTRootView)` of the app delegate (SceneDelegate on RN 0.88+):

```swift
RNBootSplash.initWithStoryboard("BootSplash", rootView: rootView)
```

Android - in `MainActivity.onCreate`, **before** `super.onCreate`:

```kotlin
RNBootSplash.init(this, R.style.BootTheme)
```

One documented trap: with `react-native-screens` below v4.16.0 you must pass
`super.onCreate(null)` instead of `savedInstanceState`, and from v4.16.0 you additionally set
`supportFragmentManager.fragmentFactory = RNScreensFragmentFactory()`. If your app crashes at
launch with a screens-related stack, this pair is the first thing to check.

## The API
- **`BootSplash.hide({ fade?: boolean })`** - hide now or fade out. `fade` is a **boolean**, not a
  duration.
- **`BootSplash.isVisible()`** - current state.
- **`BootSplash.useHideAnimation(config)`** - build a custom hide animation: pass `ready`,
  `manifest` (the generated `manifest.json`), `logo`/`brand` sources and
  `statusBarTranslucent`/`navigationBarTranslucent`, drive it with `Animated` or Reanimated, and
  render the returned `{ container, logo, brand }` props. The translucent flags matter - without
  them the status/nav bars shift between the native and JS splash, which reads as a jump.

The README documents no `show()`: the splash is natively visible from process start, so the only
operation is hiding. Code calling `BootSplash.show()` is older-version code; see the migration guide.

```tsx
init().finally(async () => {
  await BootSplash.hide({ fade: true });
});
```

With React Navigation, hide in `<NavigationContainer onReady={() => BootSplash.hide()}>` so the
first screen is laid out before the splash goes.

## Expo
1. Uninstall `expo-splash-screen` and remove its plugin entry.
2. Add the plugin - `["react-native-bootsplash", { "logo": "./assets/logo.png", "logoWidth": 100, "background": "#f5fcff" }]` -
   or dynamically via `react-native-bootsplash/expo`. `logo` is required; `platforms` must be
   explicit (`["android", "ios", "web"]`); a license key arrives via the
   `BOOTSPLASH_LICENSE_KEY` environment variable.

## Styling and status bars
Default bar styles are `dark-content` in light mode and `light-content` in dark. To force one,
override in `values/styles.xml`:
```xml
<style name="BootTheme" parent="Theme.BootSplash">
  <item name="darkContentBarsStyle">true</item>
</style>
```

## Testing
Jest must mock the module (`jest.mock("react-native-bootsplash", ...)` in a setup file registered
under `setupFiles`), or imports fail on the missing native module.

## Failure modes
- **White flash before the splash** - the native init snippet is missing, so the OS shows the
  window background instead.
- **`BootSplash.show is not a function`** - older-version code; `show` is not in the documented API, see the migration guide.
- **`generate` fails or assets are wrong** - the SVG has effects or text the generator cannot
  rasterise; flatten it.
- **Crash at launch with react-native-screens** - the `onCreate(null)` / fragment-factory pairing
  above.
- **Splash disappears then a blank frame appears** - hiding before the first screen is painted;
  hide on navigation `onReady` or after initial data resolves, not on component mount.
- **Status bar shifts when the JS splash takes over** - `useHideAnimation` without the
  translucent flags.

## Verify
- [ ] Cold start from a killed process on a real device shows the splash with no white frame
      before it.
- [ ] The splash hides only after the first meaningful screen is painted (navigation `onReady`
      or post-init).
- [ ] Android release build with a non-default flavor shows the right assets.
- [ ] Dark mode shows the dark assets where configured.
- [ ] The Jest suite runs with the module mocked.

## Checked

2026-11-02. Confirmed against the react-native-bootsplash README (github.com/zoontek/react-native-bootsplash): generate CLI flags (--platforms, --logo-width, --flavor, --license-key, --brand/--dark-* need a license key, over 50 files), iOS customize snippet for RN >= 0.88 and < 0.88, Android init before super.onCreate, react-native-screens < 4.16.0 and >= 4.16.0 branches (RNScreensFragmentFactory), hide({ fade?: boolean }), isVisible, useHideAnimation config (ready, manifest, translucent flags, returned container/logo/brand), Expo plugin (platforms must be explicit, BOOTSPLASH_LICENSE_KEY), React Navigation onReady, Jest mock. Removed: the claim that the old init command was renamed and the MIGRATION.md source link (404 on main); the v6/v7 detail is left to the repo's migration guide.

Method: documentation only; no commands were run.
