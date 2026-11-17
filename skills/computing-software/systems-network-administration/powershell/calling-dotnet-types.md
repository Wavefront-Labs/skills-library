---
id: computing-software.systems-network-administration.powershell.calling-dotnet-types
name: calling-dotnet-types
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-classes, dotnet-types, static-methods, using-namespace, type-accelerators, generics, get-member, type-casting]
level: practitioner
status: verified
description: "Call .NET from PowerShell: static methods and constructors, using namespace, generics, overload selection, type accelerators, loading assemblies, and when .NET beats a cmdlet."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/samples/creating-.net-and-com-objects--new-object-
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_using
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_type_accelerators
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Calling .NET types from PowerShell

## Syntax
```powershell
[System.Net.Dns]::GetHostAddresses('dc01')                  # static method
[math]::Round(3.14159, 2)                                   # type accelerator for System.Math
[System.IO.Path]::GetTempFileName()
[datetime]::UtcNow                                          # static property
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$list = [System.Collections.Generic.List[string]]::new()    # constructor (PS 5+)
$sb = New-Object System.Text.StringBuilder 256              # older form
$dict = [System.Collections.Generic.Dictionary[string, int]]::new([StringComparer]::OrdinalIgnoreCase)
```
- Shorten names: `using namespace System.Collections.Generic` at the top of the script, then
  `[List[string]]::new()`.
- See accelerators: `[psobject].Assembly.GetType('System.Management.Automation.TypeAccelerators')::Get`.
- Discover members: `[System.IO.File] | Get-Member -Static`; overloads by calling without
  parentheses: `[System.IO.File]::ReadAllLines`.

## Overloads and argument types
PowerShell picks an overload from argument types; when ambiguous, cast:
```powershell
[System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))   # UTF-8 no BOM
[string]::Join(',', [string[]]$items)
```
- .NET methods resolve relative paths against the **process** working directory, not `$PWD`.
  Always pass full paths: `(Resolve-Path .\x.txt).ProviderPath` or `$PWD.ProviderPath`.
- `[ref]` for out/ref parameters: `$n = 0; [int]::TryParse('42', [ref]$n)`.
- Methods returning `void` produce no output; methods returning values emit them into the
  pipeline: suppress with `[void]` or `$null =` (20,000 `List.Add` calls: about 30-180 ms either way versus about
  2 s with `| Out-Null` on the test machine).

## Where .NET beats a cmdlet
| Task | .NET |
|---|---|
| Reading huge files | `[System.IO.File]::ReadLines($p)` (streams) vs `Get-Content` |
| Writing many lines | `[System.IO.StreamWriter]` vs repeated `Add-Content` |
| Fast set membership | `[HashSet[string]]` vs `-contains` on arrays |
| DNS lookup without the DnsClient module | `[System.Net.Dns]::GetHostEntry()` |
| TCP port test with timeout | `[System.Net.Sockets.TcpClient]::new().ConnectAsync(h,p).Wait(ms)` |
| IP math | `[ipaddress]'10.0.0.1'`, `.GetAddressBytes()` |
| Secure random | `[System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)` (PS 7; the static method is missing in 5.1) |

## Loading assemblies
```powershell
Add-Type -AssemblyName System.Web                 # GAC or framework assembly by name
Add-Type -Path '<LIB_DIR>\Vendor.Sdk.dll'          # specific file
using assembly <LIB_DIR>\Vendor.Sdk.dll              # parse-time, needed when classes reference the types
```
`using assembly` takes a path or a full assembly name. `using assembly System.Windows.Forms` parsed in
Windows PowerShell 5.1, but that and `using assembly System.Net.Http` failed with `Cannot load assembly` in PowerShell
7.6.7, where `using assembly <full path to System.Windows.Forms.dll>` worked. In scripts that must run on both, use
`Add-Type -AssemblyName` at run time instead.
An assembly cannot be unloaded from a session; version conflicts need a new process.

## Disposal
Types implementing `IDisposable` (streams, TcpClient, SqlConnection, X509Store) must be disposed:
```powershell
$w = [System.IO.StreamWriter]::new($path)
try { foreach ($l in $lines) { $w.WriteLine($l) } } finally { $w.Dispose() }
```

## Verify
- [ ] Scripts using relative paths with .NET methods were changed to full paths.
- [ ] Disposable objects are disposed in `finally`.

## Checked
Ran every snippet class on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: static methods and properties, generic
`List`, `Dictionary` with a comparer, `HashSet`, `using namespace`, the TypeAccelerators `Get` call (94 accelerators in
5.1, 107 in 7.6.7), listing overloads without parentheses, `[ref]` with `TryParse`, `WriteAllText` with
`UTF8Encoding($false)` (bytes `74,111,115,195`, no BOM), `[string]::Join`, process-versus-`$PWD` directory
(`Set-Location` did not change `[Environment]::CurrentDirectory`), `GetHostEntry`, `ConnectAsync(...).Wait(ms)`,
`[ipaddress]`, `GetBytes(32)` (7 only), `Add-Type -AssemblyName System.Web`, disposal pattern, and
`IDisposable` for X509Store, TcpClient, StreamWriter and DbConnection (reflection). `using assembly` behaviour and the
`| Out-Null` timing above were measured. The "reading huge files" row is the documented streaming behaviour of
`File.ReadLines` (a 58-line file was read; no large-file benchmark was run).
