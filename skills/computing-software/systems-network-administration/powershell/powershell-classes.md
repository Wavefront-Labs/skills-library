---
id: computing-software.systems-network-administration.powershell.powershell-classes
name: powershell-classes
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-classes, powershell-class-definition, constructors, inheritance, static-members, hidden, using-module, class-constructors, class-reload-gotchas]
level: advanced
status: verified
description: "Define PowerShell classes: properties, constructors, methods, static members, inheritance, validation, using module for export, and the reload and scope limits that bite."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes_constructors
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_using
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Defining PowerShell classes (PS 5+)

Use classes for DSC resources, for typed internal models in a module, or when you need
methods and inheritance. For plain output records, `[pscustomobject]` is simpler.

```powershell
class ServerRecord {
  [ValidateNotNullOrEmpty()] [string] $Name
  [ValidateRange(1, 65535)]  [int]    $Port = 5985
  [datetime] $LastSeen
  hidden [string] $Secret                         # not shown by default formatting/Get-Member
  static [int] $Count = 0

  ServerRecord() { }                              # parameterless ctor, enables hashtable init
  ServerRecord([string]$name) {                   # constructor
    $this.Name = $name
    [ServerRecord]::Count++
  }
  ServerRecord([string]$name, [int]$port) { $this.Name = $name; $this.Port = $port }

  [bool] IsStale([int]$days) {
    return $this.LastSeen -lt (Get-Date).AddDays(-$days)    # 'return' is required for output
  }
  [string] ToString() { return "$($this.Name):$($this.Port)" }
  static [ServerRecord] Parse([string]$s) {
    $n, $p = $s -split ':'
    return [ServerRecord]::new($n, [int]$p)
  }
}

$s = [ServerRecord]::new('web01')
$s = [ServerRecord]@{ Name = 'web02'; Port = 5986 }   # hashtable init needs a parameterless ctor
[ServerRecord]::Parse('db01:1433').IsStale(7)
```
Defining any constructor removes the implicit default one, which is why `ServerRecord() { }`
is declared explicitly.

## Inheritance and interfaces
```powershell
class WebServer : ServerRecord {
  [string[]] $Sites
  WebServer([string]$n) : base($n, 443) { }
  [string] ToString() { return "web:" + ([ServerRecord]$this).ToString() }
}
class ByPort : System.Collections.Generic.IComparer[ServerRecord] {
  [int] Compare([ServerRecord]$a, [ServerRecord]$b) { return $a.Port.CompareTo($b.Port) }
}
```

## Method rules that surprise script authors
- Output only via `return`; stray expressions inside methods are discarded (unlike functions).
- Variables from the script scope are not visible inside methods: an unqualified `$scriptVar` is a parse error
  ("Variable is not assigned in the method"); `$script:scriptVar` works. Prefer properties or parameters.
- `$this` is required to reach members. Typed parameters and return types are enforced.
- Errors: `throw` works (caught by the caller). about_Classes_Methods says non-terminating errors from `Write-Error` inside a method "aren't passed through"; on 7.6.7 the message was displayed and the method carried on, so do not rely on either: use `throw`.

## Exporting from modules
Classes defined in a `.psm1` are **not** exported by `Import-Module`. Consumers need
`using module ContosoTools` at the top of the script (parse-time, must be the first statements).
Alternatively, register the classes as type accelerators inside the `.psm1` (the pattern
documented in about_Classes) so they are usable after a plain `Import-Module`.

## Reload limit
A class type is compiled once per session. After editing a class, `Import-Module -Force` does
**not** update it in the current session (about_Classes: "there's no way to load any updated classes"): start a new `pwsh` (VS Code: restart the session).
Types referenced in class definitions must be resolvable at parse time: use `using namespace`
and `using assembly`, or `Add-Type` in a module loaded first.

Run on 7.6.7: constructors, hashtable init, `ValidateRange`/`ValidateNotNullOrEmpty` throwing at creation, `hidden` (visible with `Get-Member -Force`), static `Count`, `: base(...)`, the base-cast `ToString()`, and a class implementing `IComparer[ServerRecord]`. Without any parameterless constructor, `[NoDef]::new()` fails with "Cannot find an overload for "new" and the argument count: "0"".

## Verify
- [ ] Constructors validate input (a bad port throws at creation).
- [ ] A consumer script with `using module` can create the class; without it, the type is not found.
