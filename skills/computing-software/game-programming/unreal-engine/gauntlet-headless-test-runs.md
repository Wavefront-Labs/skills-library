---
id: computing-software.game-programming.unreal-engine.gauntlet-headless-test-runs
name: gauntlet-headless-test-runs
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-packaging, gauntlet, runuat, headless-testing, performance-testing, multiplayer-test, csv-profiler, game-programming]
level: advanced
status: draft
description: "Run packaged-build tests with Unreal Gauntlet: RunUnreal via UAT, test node scripts in C#, client/server roles, collecting logs and CSV perf data in CI."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/csv-profiler-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gauntlet headless test runs

**Goal:** launch packaged builds (client, server, several clients) on build machines or devices, run a
scripted session, gather logs/perf data and report pass/fail to CI.

## What Gauntlet is
A UAT-based framework (C# in `Engine/Source/Programs/AutomationTool/Gauntlet`) that deploys builds,
starts processes with roles, monitors them, and evaluates results via a **test node** class. In-game,
a **Gauntlet test controller** (`UGauntletTestController` subclass, C++) drives the session (load map,
run actions, report state, request exit).

## Running
```
RunUAT.bat RunUnreal -project="<ProjectDir>/MyGame.uproject" -platform=Win64 -configuration=Development ^
  -build="<StagedBuildDir>" -test=MyGame.BootTest -ini:Engine:[/Script/...]... -verbose
```
- `-build` points to a staged/archived build (from BuildCookRun) or `editor` to run with the editor.
- `-test=` selects a C# test node; built-in ones include `UE.BootTest`, `UE.EditorAutomation`,
  `UE.TargetAutomation` (run automation tests inside a packaged build).
- Device/platform options select where to run (local PC, devkits, devices).

## Test node (C#)
```csharp
public class SoakTest : UnrealTestNode<UnrealTestConfiguration>
{
    public SoakTest(UnrealTestContext InContext) : base(InContext) { }
    public override UnrealTestConfiguration GetConfiguration()
    {
        var Config = base.GetConfiguration();
        var Server = Config.RequireRole(UnrealTargetRole.Server);
        Server.Controllers.Add("SoakTestController");
        var Clients = Config.RequireRoles(UnrealTargetRole.Client, 4);
        foreach (var C in Clients) { C.Controllers.Add("SoakTestController"); C.CommandLine += " -csvprofile"; }
        Config.MaxDuration = 30 * 60;   // seconds
        return Config;
    }
}
```
Result evaluation: process exit codes, log scanning (errors/ensures/fatal), controller-reported state.

## Performance data
Run with `-csvprofile` / `-csvGpuStats` to have the CSV profiler record frame times and stats; collect
CSVs as artifacts and track trends with `PerfReportTool` (engine tool) or your own dashboards.
`-trace=...` for Insights traces on demand.

## CI integration
Typical nightly: BuildCookRun -> archive -> Gauntlet boot test on each platform -> soak/perf test ->
publish logs, CSVs and summary. Horde/BuildGraph orchestrate this in larger setups.

## Verify
- [ ] Boot test passes on every target platform for nightly builds.
- [ ] Multi-client test launches server + clients and reports results without manual steps.
- [ ] CSV perf artifacts collected and compared against the previous build.
