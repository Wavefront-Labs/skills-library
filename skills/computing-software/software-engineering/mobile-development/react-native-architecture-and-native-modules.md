---
id: computing-software.software-engineering.mobile-development.react-native-architecture-and-native-modules
name: react-native-architecture-and-native-modules
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, cross-platform-mobile, react-native, turbo-modules, fabric, expo, native-modules, hermes]
level: practitioner
status: docs-checked
description: "Build React Native apps on the New Architecture: JSI, Turbo Native Modules with Codegen or Expo Modules, and the frame-budget performance causes the React Native docs name."
sources:
  - https://reactnative.dev/architecture/landing-page
  - https://reactnative.dev/docs/turbo-native-modules-introduction
  - https://docs.expo.dev/modules/overview/
  - https://reactnative.dev/docs/performance
  - https://reactnative.dev/docs/hermes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Native architecture and native modules

**Goal:** a React Native app on the New Architecture that calls platform APIs through typed native
modules and keeps JavaScript and UI frame rates healthy. For module and component specs in depth,
see the `react-native-new-architecture` skill.

## 1. Architecture (0.76+ default)
- With 0.76 "The New Architecture is enabled by default in all the React Native projects"; it can be
  turned off (`newArchEnabled=false` in `android/gradle.properties`, `ENV['RCT_NEW_ARCH_ENABLED'] =
  '0'` in the iOS Podfile).
- **JSI** replaces the asynchronous bridge: JavaScript can hold a reference to a C++ object and
  invoke methods directly without serialization costs.
- The renderer supports concurrent React features and synchronous layout reads.
- An interoperability layer lets many old-architecture libraries run, with known limitations (no
  custom Shadow Nodes, no concurrent features), and the blog says it will be removed in a future
  release.
- **Hermes** is the default engine for new apps; in release builds JavaScript is compiled to
  bytecode ahead of time (see the Hermes page of reactnative.dev).

## 2. Writing native code: Turbo Native Module or Expo Modules API
A Turbo Native Module is a typed Flow or TypeScript spec, Codegen output, and your native code;
Codegen runs automatically with the Android build and with `pod install` on iOS. Spec files
should use the `Native` prefix.

```ts
// specs/NativeDeviceInfo.ts
import type { TurboModule } from "react-native";
import { TurboModuleRegistry } from "react-native";
export interface Spec extends TurboModule {
  getModel(): string;
}
export default TurboModuleRegistry.getEnforcing<Spec>("NativeDeviceInfo");
```
`package.json` needs a `codegenConfig` with `name`, `type`, `jsSrcsDir` and, for Android,
`javaPackageName`.

The Expo Modules API writes modules and views in Swift and Kotlin. Per the Expo docs: all Expo
Modules support the New Architecture and are backwards compatible with old-architecture apps; both
APIs use JSI; "If you intend to use C++ in your native module, use Turbo Modules"; "If you are
looking for a better developer experience and you are willing to depend on the `expo` package, then
use the Expo Modules API."

## 3. Performance (from the React Native Performance Overview)
- iOS and Android devices display at least 60 frames per second, leaving at most 16.67 ms per frame.
  There are two frame rates (toggle "Show Perf Monitor" in the Dev Menu): the JS thread, where
  business logic, API calls and touch handling run, and the UI (main) thread.
- Native stack navigators (such as `@react-navigation/native-stack`) run transitions on the main UI
  thread, so JS frame drops do not interrupt them; a `ScrollView` also scrolls while the JS thread
  is busy.
- Dev mode hurts JS performance greatly ("Always make sure to test performance in release builds").
- `console.*` calls can be "a big bottleneck in the JavaScript thread" in bundled apps, including
  debugging libraries such as `redux-logger`; the docs suggest `babel-plugin-transform-remove-console`
  for production builds.
- Slow `FlatList`: implement `getItemLayout`, or consider FlashList or Legend List.
- Heavy JS work during animations: defer work until idle (`requestIdleCallback`) or use
  `LayoutAnimation` for fire-and-forget animations; the `Animated` API computes keyframes on the JS
  thread unless `useNativeDriver: true` is set.
- Android views moved while alpha compositing is needed: `renderToHardwareTextureAndroid` can help,
  but watch memory. iOS already enables `shouldRasterizeIOS` by default.
- Animating an `Image`'s size on iOS re-crops and rescales every time; animate with
  `transform: [{scale}]` instead.
- A slow-feeling `TouchableX` after a heavy `onPress` re-render: wrap the action in
  `requestAnimationFrame`.

## Verify
- [ ] `newArchEnabled` is as intended for both platforms, and Codegen builds cleanly.
- [ ] Performance is judged on release builds, with `console.*` calls removed from production.
- [ ] Scrolling long lists is checked on a mid-range Android device.

## Checked
2026-11-08. Confirmed against reactnative.dev About the New Architecture, 0.76 blog post, Native
Modules guide, Performance Overview (updated 2026-10-27) and the Expo Modules API overview. Removed
because the cited pages do not state them: Expo/EAS recommendation and "managed" claims, "lazily
loaded" Turbo Modules, reactnative.directory advice, the Swift module example, upgrade-helper and
`expo install --fix` advice, OTA policy claims, Pods/Gradle clean commands, and source map
composition remarks.
Method: documentation only; no commands were run.
