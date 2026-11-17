---
id: computing-software.game-programming.unreal-engine.buildgraph-ci-scripts
name: buildgraph-ci-scripts
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-packaging, buildgraph, ci-pipeline, horde, game-programming]
level: practitioner
status: docs-checked
description: "Write BuildGraph XML scripts for Unreal: tasks, nodes, agents, triggers, aggregates, properties and tags, and split nodes across a build farm with -Export and -SingleNode."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/buildgraph-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/buildgraph-script-tasks-reference-for-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuildGraph scripts for CI

**Goal:** a declarative script of build steps that runs locally and can be spread across build machines.

## Model (BuildGraph page)
- Script-based build automation, XML, integrated with UnrealBuildTool, AutomationTool and the Editor. A graph of
  user-defined nodes with dependencies; asked for a target (a node or named output) it runs every node required.
- Elements: Tasks (compile, cook...), Nodes (named ordered sequence of tasks producing outputs, may depend on other
  nodes), Agents (nodes run on the same machine; no effect when building locally), Triggers (groups needing manual
  intervention), Aggregates (a single name for groups of nodes and named outputs).
- `<Property>` declares reusable values, scoped to first declaration; `$(Property Name)` expands in any attribute string
  when the script is read. `<Option>` makes a property settable on the command line; `<EnvVar>` imports an environment
  variable. Any element can be conditional via the `If` attribute.
- Lists of files accept Perforce-style wildcards, full paths or a tagged collection (referenced with a `#` prefix).
  The `<Tag>` task adds files to a tag set (union and difference supported); nodes declare outputs as named tags.
- Epic ships examples in `[Engine Root]/Engine/Build/Graph/Examples`, the binary-distribution script
  `Engine/Build/InstalledEngineBuild.xml`, and a schema `Engine/Build/Graph/Schema.xsd` which Visual Studio uses for
  tooltips and validation.

## Running in parallel (BuildGraph page)
Generate the graph with `-Export=<Filename>` (JSON of nodes and dependencies). Each participating agent is synced to the
same changelist and re-runs UAT with `-SingleNode=<Name>`. Outputs travel between agents through shared storage,
`-SharedStorageDir=<Path>`. The page says machine allocation and coordination is assumed to be managed by an external
system.

## Predefined tasks (Script Tasks page)
Custom tasks derive from `CustomTask` with the `TaskElement` attribute (element name, parameter class) and
`TaskParameter` for XML fields; `LogTask` is recommended as a starting point. Task parameters confirmed on the page:
- `Command`: `Name` (required), `Arguments`; runs an AutomationTool child process.
- `Compile`: `Configuration` and `Platform` required; `Target`, `Project`, `Arguments`, `Tag`, `Clean` and others
  optional; uses UnrealBuildTool.
- `Cook`: `Project` and `Platform` required; `Maps` (separated by `+`), `Arguments`, `Tag`, `TagOutput` optional.
- `Copy`: `From` and `To` required; `Overwrite`, `Tag`, `ErrorIfNotFound`, `Exclude` optional.
- `Tag`: `With` required; `Files`, `Filter`, `Except`, `BaseDir`, `FileLists`.
- `Zip`: `FromDir` and `ZipFile` required. `Sign`: `Files` required. `Spawn`: `Exe` required. `Log`: `Message`, `Files`.
- Every task takes an optional `If` condition. `BuildCookRun` is called out as a common packaging command.

## Checked
Date: 2026-11-07. Read in full: the BuildGraph page. The BuildGraph Script Tasks page (about 58K characters) was read only
for its intro and the Command, Compile, Cook, Copy, Log, Sign, Spawn, Tag and Zip entries; other task entries (AWS,
Docker and others) were not opened. The `epicgames.com/BuildGraph` link formerly cited returns 403 and was not a source.
Unversioned en-us pages that state no engine version.
Removed as not on the pages read: the sample XML (`Requires`, `Produces` attributes, `Aggregate Requires`), the
`RunUAT.bat BuildGraph -Script= -Target= -set:` command, `-ListOnly`, `-Preprocess`, Horde and Jenkins/TeamCity claims,
`Error` task, and the gotchas and Verify checklist.
Method: documentation only; no commands were run.
