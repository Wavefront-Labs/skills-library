---
id: computing-software.software-engineering.mobile-development.react-native-new-architecture
name: react-native-new-architecture
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, react-native, turbomodules, fabric-renderer, jsi, codegen, new-architecture, expo-modules, bridgeless]
level: advanced
status: docs-checked
description: "Work with the React Native New Architecture: JSI, TurboModules and Codegen specs, Fabric native components, the 0.76 default and opt-out, the interop layer, Expo Modules."
sources: ["https://reactnative.dev/architecture/landing-page", "https://reactnative.dev/docs/turbo-native-modules-introduction", "https://reactnative.dev/docs/fabric-native-components-introduction", "https://reactnative.dev/blog/2024/10/23/the-new-architecture-is-here", "https://docs.expo.dev/modules/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Native New Architecture (Fabric / TurboModules / JSI)

**Goal:** build and migrate native modules and components for the New Architecture, which is enabled
by default since React Native 0.76.

## The pieces
- **JSI** (JavaScript Interface): replaces the asynchronous bridge between JavaScript and native.
  "JSI is an interface that allows JavaScript to hold a reference to a C++ object and vice-versa",
  so methods are invoked directly "without serialization costs". The docs cite VisionCamera
  processing frames in real time (frame buffers around 30 MB).
- **Turbo Native Modules**: a typed JavaScript specification (Flow or TypeScript), Codegen output
  generated from it, and your native code. Codegen converts the spec into native language
  interfaces.
- **Fabric**: the New Architecture renderer. It supports concurrent React features (Suspense for
  data fetching, Transitions), automatic batching with the React 18 renderer, and synchronous
  layout reads (`useLayoutEffect` with `measureInWindow` in a single commit, avoiding an `onLayout`
  visual jump).
- Enabling the New Architecture "may not immediately improve the performance or user experience";
  code may need refactoring to use synchronous layout effects or concurrent features.

## A Turbo Native Module (from the docs' guide)
Spec file; if you rename the module and spec, "always use 'Native' as prefix":
```ts
// specs/NativeLocalStorage.ts
import type {TurboModule} from 'react-native';
import {TurboModuleRegistry} from 'react-native';

export interface Spec extends TurboModule {
  setItem(value: string, key: string): void;
  getItem(key: string): string | null;
  removeItem(key: string): void;
  clear(): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeLocalStorage');
```
`TurboModuleRegistry.get<T>(name)` returns `null` if the module is unavailable;
`getEnforcing<T>(name)` throws instead.

Tell Codegen where the spec lives in `package.json`:
```json
"codegenConfig": {
  "name": "NativeLocalStorageSpec",
  "type": "modules",
  "jsSrcsDir": "specs",
  "android": { "javaPackageName": "com.nativelocalstorage" }
}
```
- Android: Codegen runs through the `generateCodegenArtifactsFromSchema` Gradle task, and "is
  automatically run when you build your Android application".
- iOS: Codegen runs as part of the script phases CocoaPods adds; run `bundle exec pod install`.
- The guide's Android example implements the module in a package extending `BaseReactPackage`, and
  on iOS renames `RCTNativeLocalStorage.m` to `.mm` so it is an Objective-C++ file.

## Fabric native components
For a new component that wraps a host component (for example a unique CheckBox on Android or a
UIButton on iOS) use a Fabric Native Component.
- The spec file "must be named `<MODULE_NAME>NativeComponent.{ts|js}`"; the `NativeComponent` suffix
  is used by Codegen to detect a spec file.
- The spec exports `codegenNativeComponent<NativeProps>(...)`, where `NativeProps` extends
  `ViewProps`. Its `codegenConfig` in `package.json` uses `"type": "components"` and, on iOS, an
  `ios.componentProvider` map from the JS component name to the iOS class.
- Android: Codegen generates a ViewManager interface and delegate; the guide's manager extends
  `SimpleViewManager` and implements the generated interface.
- iOS: the guide's component class extends `RCTViewComponentView`, "the base class for all the
  native components".
- The guide's component works only with the New Architecture; it points to a separate backwards
  compatibility guide for supporting both.

## Migrating an app
1. With 0.76 and later "the New Architecture is enabled by default in all the React Native
   projects". Most apps can upgrade with the same effort as any release.
2. After upgrading the app runs on the New Architecture with an automatic interoperability layer for
   the old architecture. The blog post says the interop layer does not support accessing custom
   Shadow Nodes or concurrent features, and that a future release will remove it, so modules will
   need to support the New Architecture.
3. To get concurrent features and full benefits, migrate custom Native Modules and Native
   Components to the new APIs. Library maintainers should first test their library with the
   interop layer and open an issue on the New Architecture Working Group if it does not work.
4. Opt-out, if you cannot use it: set `newArchEnabled=false` in `android/gradle.properties`; on iOS
   add `ENV['RCT_NEW_ARCH_ENABLED'] = '0'` in the main scope of `ios/Podfile` and run
   `bundle exec pod install`.

## Expo Modules API
The Expo Modules API lets you write Swift and Kotlin native modules and views. The docs say all
Expo Modules support the New Architecture and are backwards compatible with apps on the old
architecture, and that its performance characteristics are similar to Turbo Modules (both use JSI).
Their paraphrase of the React Native team's recommendation: use Turbo Modules if you intend to use
C++ in the module; use the Expo Modules API if you want a better developer experience and are
willing to depend on the `expo` package. They state adding the API has a negligible impact on app
size (possibly a few hundred kilobytes).

## Verify
- [ ] The app runs with the New Architecture enabled (the default since 0.76) unless a documented
      opt-out is recorded.
- [ ] Codegen output builds cleanly for Android and iOS.
- [ ] Custom native modules have a typed spec; spec file names follow the `Native` prefix and
      `NativeComponent` suffix rules.
- [ ] Libraries are tested with the interop layer, knowing it is planned to be removed.

## Checked
2026-11-08. Confirmed against reactnative.dev: About the New Architecture (updated 2026-10-14),
the 0.76 release blog post, the Native Modules and Native Components guides, and the Expo Modules
API overview: JSI description, Fabric capabilities, spec naming, `codegenConfig`, Codegen runs on
Android and iOS, `TurboModuleRegistry` modes, 0.76 default, interop layer limits and planned
removal, opt-out steps, Expo Modules comparison. Removed because the pages do not state them:
"lazily loaded", the C++ shadow tree description, bridgeless mode details, the `TurboReactPackage`
and Swift-shim wording, `WithDefault`/`Int32` type names, reactnative.directory and Upgrade Helper
advice, the Swift Expo module snippet and `create-expo-module`, and performance claims about
Reanimated and Hermes.
Method: documentation only; no commands were run.
