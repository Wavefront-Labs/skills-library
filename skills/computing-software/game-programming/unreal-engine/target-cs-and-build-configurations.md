---
id: computing-software.game-programming.unreal-engine.target-cs-and-build-configurations
name: target-cs-and-build-configurations
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-build-tool, ubt, target-cs, build-configurations, debuggame, development, shipping, test-configuration, game-programming]
level: practitioner
status: docs-checked
description: "Configure Unreal targets and build configurations: Game/Editor/Server/Client Target.cs, Debug/DebugGame/Development/Test/Shipping differences, and target-rule properties."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-build-tool-target-reference
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configurations-reference-for-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Target.cs and build configurations

**Goal:** pick the right binary for the job (debugging, profiling, QA, release) and control what each
target includes.

## Targets
Targets are declared in C# `.target.cs` files under the project root. Each file declares a class deriving
from `TargetRules` and sets properties in its constructor. The class name must be the file name followed
by `Target` (`MyProject.target.cs` defines `MyProjectTarget`).

| Target type | Meaning (Epic's wording) |
|---|---|
| `Game` | A standalone game which requires cooked data to run. |
| `Client` | Same as Game, but with no server code; useful for networked games. |
| `Server` | Same as Game, but with no client code; useful for dedicated servers. |
| `Editor` | A target which extends the Unreal Editor. |
| `Program` | A standalone utility program built on top of Unreal Engine. |

A `<GAME_NAME>Client.Target.cs` file makes the Client build configurations valid; likewise
`<GAME_NAME>Server.Target.cs` for Server.

```csharp
public class MyGameTarget : TargetRules
{
    public MyGameTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("MyGame");
        if (Configuration == UnrealTargetConfiguration.Shipping)
        {
            bUseLoggingInShipping = false;
            GlobalDefinitions.Add("MYGAME_CHEATS=0");
        }
        else GlobalDefinitions.Add("MYGAME_CHEATS=1");
    }
}
```
Properties used above, as the target reference describes them:
- `Type` (`TargetType`): the type of target. `Configuration` is the configuration being built.
- `DefaultBuildSettings` (`BuildSettingsVersion`): the engine version whose defaults are kept for
  backwards compatibility; the latest value always uses current defaults, "at the risk of introducing
  build errors while upgrading".
- `ExtraModuleNames`: additional modules compiled into the target. `GlobalDefinitions`: macros defined
  across the whole target.
- `bUseLoggingInShipping`: logging for test/shipping builds. Related switches: `bUseConsoleInShipping`,
  `bUseChecksInShipping`, `bUseExecCommandsInShipping`, `bAllowProfileGPUInTest`,
  `bAllowProfileGPUInShipping`.
- `BuildEnvironment` (`TargetBuildEnvironment`) specifies the build environment; `bOverrideBuildEnvironment`
  ignores violations of the shared build environment (for example editor targets modifying definitions).
  Look up `TargetBuildEnvironment` in the engine source for its values.

## Configurations
Each configuration name has two keywords: the state (Debug, DebugGame, Development, Shipping, Test) and the
target (Game, Editor, Client, Server).

| Config | Epic's description |
|---|---|
| Debug | Builds engine and game code without optimizations; slower but easier to debug. |
| **DebugGame** | Builds game code without optimizations; ideal for debugging only game modules. |
| **Development** | Enables all but the most time-consuming engine and game code optimizations. The editor uses it by default, and code changes show in the editor. |
| **Test** | The Shipping configuration with some console commands, stats and profiling tools enabled. |
| **Shipping** | Optimal performance for shipping; strips console commands, stats and profiling tools. |

Notes from the configuration reference:
- Every configuration, Shipping included, produces debugging symbols when built from Visual Studio or when
  Project Settings > Project > Packaging > Project > Include Debug Files is on; Development and Shipping
  are just harder to debug.
- Compiling a Debug project and opening it in the editor needs the `-debug` flag for code changes to show.
- A UE solution (engine plus project source) offers Debug for Game, Client and Server; a UE project
  (project source only) offers DebugGame, Development and Shipping for Game and DebugGame and Development
  for Editor, and no Debug, Client or Server configurations.
- To open a project in the editor and see code changes, build an Editor configuration.

## Code guards
`bCompileAgainstEditor` is enabled for editor builds and mainly drives the value of `WITH_EDITOR`, so keep
editor-only code behind it:
```cpp
#if WITH_EDITOR
    // editor-only code (property change callbacks, validation)
#endif
```

## Verify
- [ ] Game and Editor (and Server if used) targets compile in Development and Shipping.
- [ ] The Shipping binary follows your `bUseConsoleInShipping` and `bUseLoggingInShipping` choices.
- [ ] DebugGame breakpoints in game code hit with correct locals.

## Checked
Checked 2026-11-08 against the Targets reference and the Build Configurations Reference.
Confirmed: target types, `.target.cs` structure and naming rule, the listed `TargetRules` properties,
the configuration descriptions, symbols and `-debug` notes, solution and project availability.
Removed because the pages do not state them: dedicated-server source-engine requirement, `UE_BUILD_*` and
`UE_SERVER` macros, "Unique" build environment requirement, `IncludeOrderVersion` sample line, profiling
advice, the optimisation state of engine code in DebugGame.
Method: docs-only read of cited pages, 2026-11-08
