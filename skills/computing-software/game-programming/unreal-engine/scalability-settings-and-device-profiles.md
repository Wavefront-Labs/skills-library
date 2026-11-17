---
id: computing-software.game-programming.unreal-engine.scalability-settings-and-device-profiles
name: scalability-settings-and-device-profiles
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-insights, device-profiles, scalability-groups, cvars-per-platform, game-programming]
level: practitioner
status: draft
description: "Configure Unreal scalability groups and Device Profiles to set CVars per platform and hardware tier, with matching rules, inheritance and runtime quality switching."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-device-profiles-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scalability settings and device profiles

**Goal:** the right quality on every device class without per-platform code.

## Scalability groups
`sg.ViewDistanceQuality`, `sg.AntiAliasingQuality`, `sg.ShadowQuality`, `sg.GlobalIlluminationQuality`,
`sg.ReflectionQuality`, `sg.PostProcessQuality`, `sg.TextureQuality`, `sg.EffectsQuality`,
`sg.FoliageQuality`, `sg.ShadingQuality` — levels 0..3 (Low..Epic) and 4 (Cinematic). Each level maps
to CVars in `BaseScalability.ini`; override in `Config/DefaultScalability.ini`:
```ini
[ShadowQuality@1]
r.Shadow.MaxResolution=1024
r.Shadow.CSM.MaxCascades=2
```
Runtime: `UGameUserSettings::GetGameUserSettings()->SetOverallScalabilityLevel(2); ApplySettings(false);`
`RunHardwareBenchmark()` + `ApplyHardwareBenchmarkResults()` for auto-detect.

## Device profiles
`Config/DefaultDeviceProfiles.ini` (and per-platform `Config/<Platform>/<Platform>DeviceProfiles.ini`):
```ini
[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=1.0
+CVars=sg.ShadowQuality=1
+CVars=r.Shadow.MaxCSMResolution=1024
[/Script/AndroidDeviceProfileSelector.AndroidDeviceProfileMatchingRules]
+MatchProfile=(Profile="Android_Mid",Match=((SourceType=SRC_GpuFamily,CompareType=CMP_Regex,MatchString="Adreno \\(TM\\) 6[4-9][0-9]")))
```
- Profiles inherit via `BaseProfileName`.
- Matching rules pick a profile at startup based on GPU family, device make/model, memory, etc.
- `-dp=Android_Low` command line to force; `dp.Override` in console (some versions).
- Editor: Device Profiles window and **Preview Platform / Device Profile** to view content as a device.

## Precedence (simplified)
Base ini < device profile CVars < scalability group (user setting) < console/command line. Device
profiles can also set `sg.*` defaults per device and `ConsoleVariables` they lock.

## Gotchas
- Setting a CVar that a scalability group also controls gets overwritten when the user changes
  quality — put it into the group's ini section instead.
- Texture LOD groups per device profile (`TextureLODGroups`) affect cooking for mobile.

## Verify
- [ ] `DumpCVars r.Shadow` on device shows expected values for its profile.
- [ ] Log line "Selected Device Profile: [Android_Mid]" at startup on test devices.
