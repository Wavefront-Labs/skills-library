---
id: computing-software.software-engineering.d.d-dub-sdl-json-recipe-basics
name: d-dub-sdl-json-recipe-basics
category: computing-software
field: software-engineering
product: d
tags: [d-dub-sdl-json-recipe-basics, dub-configuration, dub-sdl, dub-json, dub-recipe, targettype, sourcepaths, importpaths, dependency, versions, libs, dflags, package-recipe, d]
level: practitioner
status: docs-checked
description: "Write a DUB package recipe: name, description, authors, license, targetType, targetName, mainSourceFile, sourcePaths, importPaths, dependency, versions, libs and dflags."
sources:
  - https://dub.pm/dub-reference/target_types/
  - https://dub.pm/dub-reference/package_settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dub.sdl and dub.json: name, targetType, sourcePaths, dependencies, versions

Goal: define a buildable package.

dub.sdl:
```
name "myapp"
description "Demo"
authors "A. Dev"
license "MIT"
targetType "executable"        # autodetect | none | executable | library | sourceLibrary | staticLibrary | dynamicLibrary
targetName "myapp"
mainSourceFile "source/app.d"
sourcePaths "source"
importPaths "source"
stringImportPaths "views"
dependency "vibe-d" version="~>0.10.0"
dependency "mylib" path="../mylib"
versions "UseFoo"
libs "z"
dflags "-preview=dip1000"
```
Same in JSON: `{"name":"myapp","targetType":"executable","dependencies":{"vibe-d":"~>0.10.0","mylib":{"path":"../mylib"}},"versions":["UseFoo"]}`.
- Platform suffixes on any setting: `dflags-ldc`, `libs-posix`, `versions-windows`, `lflags-linux-x86_64` etc.
- Fields also: `copyright`, `homepage`, `excludedSourceFiles`, `buildRequirements` (`allowWarnings`), `buildOptions` (`releaseMode`, `inline`, `optimize`, `debugInfo`, `unittests`), `preBuildCommands`, `postBuildCommands`, `copyFiles`, `lflags`, `toolchainRequirements`.
- Convert: `dub convert -f json` (or `sdl`; `-s` prints to stdout); formatting and comments are lost in conversion.

Gotchas:
- `targetType "library"` does not limit the library type; `staticLibrary`/`dynamicLibrary` force one; `sourceLibrary` adds its sources to the dependent's compiler invocation; `autodetect` is the default.

Verify: `dub build` and `dub describe` to inspect the resolved settings.

## Checked

Date 2026-11-02. Confirmed targetType values and meanings and dub convert (dub reference). Corrected the targetType library description; noted that convert loses comments and formatting.

Method: documentation only; no commands were run.
