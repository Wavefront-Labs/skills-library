---
id: computing-software.software-engineering.mobile-development.expo-constants-and-runtime-app-config
name: expo-constants-and-runtime-app-config
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, expo, expo-constants, app-config, app-json, expoconfig, execution-environment, manifest, environment-detection, runtime-config, expo-application, expo-device, build-number, version-code]
level: practitioner
status: docs-checked
description: "Read app config at runtime with expo-constants: expoConfig, executionEnvironment, platform manifests, and deprecated fields now in expo-application/expo-device."
sources: ["https://docs.expo.dev/versions/latest/sdk/constants/", "https://docs.expo.dev/workflow/configuration/", "https://docs.expo.dev/versions/latest/sdk/application/", "https://docs.expo.dev/versions/latest/sdk/device/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# expo-constants: runtime app config and environment

**Goal:** read the values from `app.json` / `app.config.js` at runtime, and know which kind of
build is running, without shipping your own config plumbing.

```bash
npx expo install expo-constants
```
```ts
import Constants from 'expo-constants';

const apiBase = (Constants.expoConfig?.extra as { apiBase?: string })?.apiBase;
```

## The fields that matter
**`Constants.expoConfig`** - the resolved app config, without fields such as `android.config` and
`ios.config` that the public config filters out. In a build it is the config embedded at build time;
when the app runs an update it is the config that comes with that update; in development it is what
the development server serves. Print it with `npx expo config --type public`. To pass your own values
to the app, add them to the `extra` field of the app config and read `Constants.expoConfig.extra`.
The configuration page says not to include any sensitive information in the app config.

**`Constants.executionEnvironment`** - which kind of build is running, from the
`ExecutionEnvironment` enum:

| Value | Meaning |
|---|---|
| `Bare` | native project directories you maintain yourself |
| `Standalone` | production/release build, with or without EAS Build |
| `StoreClient` | Expo Go or a development build built with `expo-dev-client` |

It replaces the deprecated `appOwnership`/`AppOwnership` enum. The enum values are the strings
`"bare"`, `"standalone"` and `"storeClient"`. `Constants.debugMode` is true when the app runs in
debug mode (`__DEV__`).

**`Constants.platform`** - the platform manifest (`PlatformManifest`: `android`, `ios`, `web`,
`detach`, `developer`, `hostUri`, `scheme`), distinct from `manifest` and `manifest2`. Two subtleties:
- `Constants.platform.ios.buildNumber` is the embedded `Info.plist` `CFBundleVersion` (settable via
  `ios.buildNumber` in app.json in a standalone app) and "will never change for a given native
  binary", while `Constants.expoConfig.ios.buildNumber` comes from the manifest, which can be
  updated. It is `null` in Expo Go.
- `Constants.platform.android.versionCode` (deprecated) is `null` in Expo Go.

**`Constants.manifest2`** - the manifest for apps using modern Expo Updates from a remote source
(EAS Update). The docs are explicit: `Constants.expoConfig` should be used for accessing the Expo
config object.

Also present: `expoGoConfig`, `easConfig`, `expoVersion`, `expoRuntimeVersion`, `debugMode`,
`deviceName`, `sessionId`, `statusBarHeight`, `systemFonts`, `isHeadless`, `linkingUri`,
`experienceUrl`, `getWebViewUserAgentAsync()`.

## Deprecations - use the right library
| Deprecated on expo-constants | Replacement |
|---|---|
| `versionCode` (Android) | `expo-application`'s `Application.nativeBuildVersion` |
| `deviceYearClass` | `expo-device`'s `Device.deviceYearClass` |
| `model` (iOS) | `expo-device`'s `Device.modelName` |
| `platform` (iOS) | `expo-device`'s `Device.modelId` |
| `systemVersion` (iOS) | `expo-device`'s `Device.osVersion` |
| `userInterfaceIdiom` | `expo-device`'s `Device.getDeviceTypeAsync()` |
| `appOwnership` / `AppOwnership` | `Constants.executionEnvironment` |

Rule of thumb: **expo-application** for native build version, **expo-device** for anything about
the device. Reaching for a deprecated constants field is usually a sign the value belongs to one
of those two.

## Patterns
```ts
// app.config.js - branch per environment, once, at config time
// (APP_ENV set via the build profile's env in eas.json)
export default () => ({
  extra: { apiBase: process.env.APP_ENV === 'production'
      ? 'https://api.example.com' : 'https://staging.example.com' },
});

// at runtime - typed, single source
const cfg = Constants.expoConfig?.extra as { apiBase: string };
const isDev = Constants.executionEnvironment === 'storeClient';
```
Keep `extra` reads behind one module rather than scattering `Constants.expoConfig` across the app;
a config module is also where the casting lives once.

## Failure modes
- **Values missing in the release build** - `app.config.js` branched on a variable that was not set
  for that build profile.
- **`extra` contains a secret** - the app config is embedded in the build and readable at runtime;
  keep secrets out of it.
- **Two build numbers disagreeing** - reading `expoConfig.ios.buildNumber` when the question is
  "which native binary", where `platform.ios.buildNumber` is authoritative.

## Verify
- [ ] Every runtime value has a declared source in `app.config.js` and one accessor module.
- [ ] `executionEnvironment` drives environment gating, and each of Standalone/StoreClient was
      actually built and checked.
- [ ] No secret is in `extra`.
- [ ] No deprecated constants field is read - version/device facts come from
      expo-application/expo-device.
- [ ] `platform.ios.buildNumber` vs `expoConfig.ios.buildNumber` chosen deliberately where the
      distinction matters.

## Checked
Date: 2026-11-08. Confirmed against the expo-constants reference and the app config page: expoConfig description and `npx expo config --type public`, `extra`, ExecutionEnvironment values and meanings, buildNumber and versionCode notes, manifest2, deprecated fields and their expo-device/expo-application replacements, PlatformManifest keys, and the other listed fields. Removed claims not on the pages: classic/modern manifest wording, `env` argument and EAS_BUILD_PROFILE in the config function, dev-gating failure modes, and the manifest/isDevice migration note.
Method: documentation only; no commands were run.
