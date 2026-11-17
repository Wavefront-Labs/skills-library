---
id: computing-software.systems-network-administration.powershell.powershell-class-inheritance-and-interfaces
name: powershell-class-inheritance-and-interfaces
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-classes, class-inheritance, interfaces, dotnet-types]
level: advanced
status: verified
description: "Use inheritance in PowerShell classes: base constructors, overriding methods, calling base members, implementing .NET interfaces like IComparable, and limits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes_inheritance
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell class inheritance and interfaces

## Inherit
```powershell
class ServerCheck {
  [string]$ComputerName
  ServerCheck([string]$name) { $this.ComputerName = $name }
  [bool] Test() { return Test-Connection $this.ComputerName -Count 1 -Quiet }
  [string] ToString() { return "$($this.GetType().Name): $($this.ComputerName)" }
}
class WebCheck : ServerCheck {
  [int]$Port = 443
  WebCheck([string]$name, [int]$port) : base($name) { $this.Port = $port }
  [bool] Test() {
    if (-not ([ServerCheck]$this).Test()) { return $false }        # call base implementation
    return (Test-NetConnection $this.ComputerName -Port $this.Port -WarningAction SilentlyContinue).TcpTestSucceeded
  }
}
$checks = [ServerCheck]::new('dc01'), [WebCheck]::new('web01', 443)
$checks | ForEach-Object { '{0} -> {1}' -f $_, $_.Test() }
```
- `: base(args)` chains constructors. Without it, the base parameterless constructor must exist.
- Overriding: define a method with the same signature. Call the base version by casting `$this` to the base type.
- All methods are virtual; there is no `override` keyword.

## Interfaces
```powershell
class Version2 : System.IComparable {
  [int]$Major; [int]$Minor
  Version2([int]$a,[int]$b) { $this.Major=$a; $this.Minor=$b }
  [int] CompareTo([object]$o) {
    if ($this.Major -ne $o.Major) { return $this.Major.CompareTo($o.Major) }
    return $this.Minor.CompareTo($o.Minor)
  }
}
[Version2[]]$v = [Version2]::new(1,10), [Version2]::new(1,2)
$v | Sort-Object       # uses CompareTo
```
Base class first, then interfaces: `class X : BaseClass, IDisposable, IComparable`.

## Limits
- Single inheritance only; no abstract keyword (throw in base methods to emulate).
- No interfaces defined in PowerShell itself; implement .NET ones.
- Generic interfaces work when the type argument already exists, but not for the class itself: `class V3 : System.IEquatable[V3]` fails ("Type must be a type provided by the runtime") because `V3` is not resolvable at parse time. Use a non-generic `IComparable` (as above) or an already-defined type argument.

Run on 7.6.7: base-cast call (`([ServerCheck]$this).Test()`), `: base(...)`, missing base default constructor giving "Cannot find an overload for "new"", and `Sort-Object` ordering `Version2` objects through `CompareTo` (`1.2 1.10`).

## Verify
- [ ] Derived objects pass as base type parameters and dispatch to their own Test().
