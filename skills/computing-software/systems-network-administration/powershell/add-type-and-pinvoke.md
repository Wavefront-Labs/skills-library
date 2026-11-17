---
id: computing-software.systems-network-administration.powershell.add-type-and-pinvoke
name: add-type-and-pinvoke
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-classes, add-type, pinvoke, dllimport, win32-api, csharp-inline, memberdefinition]
level: advanced
status: verified
description: "Compile inline C# with Add-Type and call Win32 APIs through P/Invoke: MemberDefinition signatures, marshalling, error codes, session limits, and CLM/AV considerations."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/add-type
  - https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke
  - https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add-Type and P/Invoke

Use P/Invoke only when no cmdlet, CIM class or .NET API does the job (e.g. scheduling a
file replace at reboot, querying a token privilege, calling a vendor DLL).

## MemberDefinition: quickest P/Invoke
```powershell
$sig = @'
[DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, int dwFlags);
'@
$k32 = Add-Type -MemberDefinition $sig -Name Kernel32 -Namespace Win32 -PassThru
# MOVEFILE_DELAY_UNTIL_REBOOT = 0x4 ; null destination = delete at reboot (needs an administrator;
# the file cannot be on a remote share; both per the MoveFileExW docs)
if (-not [Win32.Kernel32]::MoveFileEx('<LOCKED_FILE_PATH>', $null, 0x4)) {
  throw [System.ComponentModel.Win32Exception]::new([Runtime.InteropServices.Marshal]::GetLastWin32Error())
}
```
- `SetLastError = true` + `Marshal.GetLastWin32Error()` (PS 7 also has `GetLastPInvokeError()`) gives
  the real error; `Win32Exception` turns the code into a message. Read it straight after the call: in a test a
  later statement read 0 ("The operation completed successfully") because PowerShell's own native calls
  overwrite the stored value. A plain move of a missing file returned `false` and `Win32Exception` rendered it as
  "The system cannot find the file specified" when read in the same `if` block.
- `CharSet.Unicode` and the `W` function variant: Windows strings are UTF-16. ANSI variants
  mangle non-ASCII names.
- Map types carefully: `HANDLE`/pointers -> `IntPtr`, `DWORD` -> `uint`, `BOOL` -> `bool`
  (4-byte), output strings -> `StringBuilder` with capacity, structs -> `[StructLayout(LayoutKind.Sequential)]`.
- pinvoke.net and the Win32 metadata (`Microsoft.Windows.SDK.Win32Metadata`) are good
  signature sources; verify against the docs page's parameter types.

## Full C# type
```powershell
Add-Type -TypeDefinition @'
using System;
public static class Hash {
  public static string Sha256Hex(string s) {
    using var sha = System.Security.Cryptography.SHA256.Create();
    return Convert.ToHexString(sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(s)));
  }
}
'@
[Hash]::Sha256Hex('abc')
```
- PS 7 (7.6.7 tested) compiles modern C# against .NET (`using var` and `Convert.ToHexString` both ran); Windows
  PowerShell 5.1 uses the legacy compiler and .NET Framework, and rejected the same code with
  `Syntax error, '(' expected` at `using var`. Write to the lowest edition you support.
  `System.Security.Cryptography.RandomNumberGenerator::GetBytes(int)` (static) is likewise missing in 5.1.
- Reference extra assemblies with `-ReferencedAssemblies`. `-OutputAssembly x.dll` writes the
  compiled assembly (worked in 5.1 and 7.6.7; a later `Add-Type -Path x.dll` loaded it).

## Session limits
- A type name is bound to one definition per session. Re-adding identical source is accepted silently, but
  changed source under the same name fails with *"Cannot add type. The type name 'X' already exists"*
  (confirmed in 5.1 and 7.6.7). Use a new name while iterating, or a new process.
- Guard repeat loads: `if (-not ('Win32.Kernel32' -as [type])) { Add-Type ... }`.
- The first compile in a fresh process took about 0.13 s (5.1) and 0.4 s (7.6.7) on the test machine; precompile
  hot paths into a DLL shipped in your module if start-up matters.

## Security considerations
- Adding new C# is blocked in constrained language mode (`Definition of new types is not supported in this
  language mode`, confirmed in 5.1 and 7.6.7); the docs say `Add-Type` can still load signed assemblies there, and
  scripts trusted by WDAC/AppLocker run in full language.
- Sign modules that need it and keep the C# in reviewed source control. Endpoint-security tools may scrutinise
  inline P/Invoke; that behaviour is product-specific and was not tested.

## Verify
- [ ] The call returns success and the Win32 error path throws a readable message.
- [ ] Script runs twice in one session without "type already exists".

## Checked
Run in PowerShell 7.6.7 (zip build) and Windows PowerShell 5.1.26100: MemberDefinition P/Invoke of MoveFileEx against a
missing file (returns false; Win32Exception message), `GetLastPInvokeError` (7 only), the `Hash` type (7 compiles,
5.1 errors at `using var`), re-adding same and changed source, `-OutputAssembly` plus `Add-Type -Path`, first-compile
timing, CLM simulation (`$ExecutionContext.SessionState.LanguageMode = 'ConstrainedLanguage'`). The MoveFileEx
reboot-delete call itself was not run (it would register a deletion on this machine); its flag value 0x4, NULL-target
behaviour, admin requirement and remote-share limit were read from the MoveFileExW docs and the Add-Type docs page.
