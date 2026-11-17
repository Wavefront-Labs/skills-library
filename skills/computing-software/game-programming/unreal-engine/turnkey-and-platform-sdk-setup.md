---
id: computing-software.game-programming.unreal-engine.turnkey-and-platform-sdk-setup
name: turnkey-and-platform-sdk-setup
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, turnkey, platform-sdk, packaging, devices, game-programming]
level: practitioner
status: draft
description: "Use Unreal Turnkey to validate and install platform SDKs, manage devices and run BuildCookRun from Platforms menu or RunUAT Turnkey commands in CI."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-turnkey-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-unreal-engine-for-platform-development", "https://dev.epicgames.com/documentation/en-us/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Turnkey and platform SDK setup

**Goal:** every developer and build agent has the exact SDK versions the engine expects, and packaging
for a platform is one command.

## Platforms menu
Editor toolbar > **Platforms**: per platform shows SDK status (valid/invalid), Install SDK, Package
Project, Cook Content, device list and Launch On. Status comes from Turnkey checks against
`Engine/Config/<Platform>/<Platform>_SDK.json` (valid min/max versions).

## Command line
```bat
RunUAT.bat Turnkey -command=VerifySdk -platform=Win64+Android -UpdateIfNeeded -project=<Proj>\MyGame.uproject
RunUAT.bat Turnkey -command=InstallSdk -platform=Android -BestAvailable
RunUAT.bat Turnkey -command=ListDevices -platform=Android
RunUAT.bat Turnkey -command=ExecuteBuild -build="Package Shipping" -platform=Win64 -project=...
```
`VerifySdk` exits non-zero if SDKs are wrong, a good CI preflight step.

## SDK sources
Studios configure where SDK installers live via `TurnkeyManifest.json` / `Studio_TurnkeyManifest.xml`
(file shares, Perforce or Google Drive paths) so InstallSdk can fetch console SDKs, which Epic cannot
distribute. Android uses the bundled `SetupAndroid` scripts and Android Studio SDK manager; Turnkey
reports NDK/SDK/JDK mismatches.

## Custom build operations
Project Launcher profiles and `Build/Turnkey/*.xml` or `DefaultEngine.ini` `[/Script/UnrealEd.ProjectPackagingSettings]`
`ProjectCustomBuilds` add entries to the Platforms menu that run custom BuildCookRun arguments (e.g.
"Package with PSO logging").

## Gotchas
- Auto SDK (`UE_SDKS_ROOT`) lets agents switch SDKs per engine version without global installs;
  preferred on CI farms.
- Restart the editor after installing SDKs; detection happens at startup.
- Platform SDK versions change with engine versions; re-run VerifySdk after upgrades.

## Verify
- [ ] CI agents run Turnkey VerifySdk before builds; developers see green status in Platforms menu.
