---
id: computing-software.game-programming.unity.player-settings-per-platform
name: player-settings-per-platform
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-player-settings, player-settings, build, platform-configuration, game-programming]
level: practitioner
status: draft
description: "Configure Unity Player Settings per platform: identifiers and versions, scripting backend and API level, color space, graphics APIs, orientation and scripted settings."
sources: ["https://docs.unity3d.com/Manual/class-PlayerSettings.html", "https://docs.unity3d.com/ScriptReference/PlayerSettings.html", "https://docs.unity3d.com/Manual/class-PlayerSettingsAndroid.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Player settings per platform

**Goal:** platform settings that are correct, versioned and set from CI rather than by hand.

## Key settings
| Area | Settings | Notes |
|---|---|---|
| Identity | Company/Product name, Version, Bundle Identifier / Package Name | identifier is permanent on stores |
| Build numbers | Android Bundle Version Code, iOS Build | must increase every upload |
| Other > Rendering | Color Space (Linear), Graphics APIs, Auto Graphics API | Linear for PBR; Vulkan/GLES fallbacks on Android |
| Configuration | Scripting Backend, API Compatibility Level, Target Architectures | IL2CPP + ARM64 required for Play Store |
| Configuration | Active Input Handling | changing restarts editor |
| Optimization | Managed Stripping Level, Strip Engine Code | test with link.xml |
| Resolution | Default orientation, fullscreen mode, Run In Background | |
| Splash | Unity logo (required on Personal) | |
| Publishing | keystore (Android), signing team (iOS) | keep secrets out of the repo |

## Script it
```csharp
PlayerSettings.bundleVersion = version;
PlayerSettings.Android.bundleVersionCode = buildNumber;
PlayerSettings.iOS.buildNumber = buildNumber.ToString();
PlayerSettings.SetScriptingBackend(NamedBuildTarget.Android, ScriptingImplementation.IL2CPP);
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.iOS, "com.studio.game");
```
Run from a `-executeMethod` build script so CI sets versions from tags. Unity 6 Build Profiles can
override some Player Settings per profile (e.g. demo vs full build identifiers).

## Gotchas
- Settings are in `ProjectSettings/ProjectSettings.asset`; merge conflicts there are common. Keep
  automation the source of truth for volatile values (version, build number).
- Switching color space or Graphics APIs reimports or recompiles shaders; do it early in a project.
- Android minimum/target API levels must meet Play Store policy; update yearly.
- `PlayerSettings` writes persist to the asset; CI should not commit them back.

## Verify
- [ ] Built package shows correct identifier, version and build number (aapt dump / Info.plist).
- [ ] Settings diff in the repo is reviewed like code.
