---
id: computing-software.software-engineering.fsharp.warning-flags
name: warning-flags
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, warning-flags, fsharp-compiler, warnaserror, warnon]
level: practitioner
status: docs-checked
description: "Tune F# compiler warnings with --warnon, --warnaserror, --nowarn and --warn, including the opt-in warnings such as unused variables."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warning control
**Goal:** make the compiler stricter.

```xml
<PropertyGroup>
  <WarnOn>1182,3390</WarnOn>
</PropertyGroup>
```
- `--warnon:list` enables warnings that are off by default (comma-separated numbers). In a project use `<WarnOn>NNNN</WarnOn>` or `<WarnOn>FSNNNN</WarnOn>`.
- If `WarnOn` is set several times only the last occurrence is used, so put every number in one comma-separated value: `<WarnOn>3388,3559</WarnOn>`.
- `--warnaserror[+|-] [list]` turns warnings into errors, optionally for specific numbers. Later options override earlier ones: `--warnaserror+ --warnaserror-:list` makes everything an error except the listed numbers.
- `--nowarn:list` disables the listed warning numbers (found in compiler output).
- `--warn:level` sets the level 0 to 5; default is 3.

## Opt-in warnings (from the page)
- 1182 unused variables.
- 3390 malformed XML doc comments.
- 3559 type inferred as obj.
- 3560 all fields changed in a record copy.
- 3388 additional implicit upcast; 3389 implicit numeric widening.
- 21 and 22 (recursion checked at run time, bindings executed out of order) are level 5.

## Self-check
Add an unused local with `--warnon:1182` and confirm the warning appears; add `--warnaserror+` and confirm the build fails.

## Checked

Method: docs-checked 2026-11-09 against the F# compiler options page. Removed unconfirmed: MSBuild TreatWarningsAsErrors / WarningsAsErrors / NoWarn property use, warning number meanings FS0025, FS0064 and FS3370, `#nowarn` file-scope behaviour, incremental build claim.
