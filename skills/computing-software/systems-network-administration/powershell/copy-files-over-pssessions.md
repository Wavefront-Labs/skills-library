---
id: computing-software.systems-network-administration.powershell.copy-files-over-pssessions
name: copy-files-over-pssessions
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, copy-item-tosession, copy-item-fromsession, winrm, file-transfer]
level: practitioner
status: docs-checked
description: "Copy files to and from remote machines with Copy-Item -ToSession and -FromSession over a PSSession: remote path semantics, recursion, and the WinRM ports and defaults."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/winrm-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copy files over PowerShell sessions

`Copy-Item` has two dynamic parameters, made available by the FileSystem provider, that copy through an existing `PSSession` instead of a UNC path.

## To and from a session
```powershell
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"
Copy-Item "<local-dir>\test.log" -Destination "<remote-dir>\" -ToSession $Session
Copy-Item "<remote-dir>\test.log" -Destination "<local-dir>\" -FromSession $Session
```
- `-ToSession`: `-Destination` refers to the local path on the remote machine.
- `-FromSession`: `-Path` and `-LiteralPath` refer to the local path on the remote machine.
- The original file is not deleted; `Copy-Item` copies, it does not move.

## Folders
- Copying a folder without `-Recurse` copies the folder only; subfolders and files are not copied. The doc's example creates the destination folder if it does not exist.
- `-Recurse` copies the contents with subfolder trees intact:
```powershell
Copy-Item "<local-dir>\" -Destination "<remote-dir>\" -ToSession $Session -Recurse
Copy-Item "<remote-dir>\scripts" -Destination "<local-dir>\scripts" -FromSession $Session -Recurse
```
- To rename during the copy, put the new file name in `-Destination` (for example `<remote-dir>\scriptingexample_copy.ps1`).
- `-Container` defaults to true and preserves directory structure; `-Container:$false` flattens, and same-named files are overwritten.
- `-Include` without `-Recurse` copies matching top-level folders but none of their contents.

## Transport context (WinRM security page)
- PowerShell Remoting uses WinRM on 5985 (HTTP) and 5986 (HTTPS), and is enabled by default on Windows Server 2012 R2 and later.
- By default only members of the Administrators group may connect; sessions run in the user's context, so normal OS access controls apply to the copy.
- WinRM encrypts remoting traffic after initial authentication, over HTTP or HTTPS.
- On a domain host reached by name, authentication defaults to Kerberos. Reached by IP address or in a workgroup, it falls back to NTLM, which is disabled by default until SSL is configured on the target or the client sets WinRM TrustedHosts. TrustedHosts only suppresses the server-identity error; it is not a trust statement.
- This is distinct from a cmdlet's own `-ComputerName` parameter, which uses RPC.

## Checked
Method: 2026-11-08 docs-only read of the Copy-Item reference (MicrosoftDocs/PowerShell-Docs markdown) and the WinRM security page (same repo). Rewritten to what they state. Dropped unsupported claims: SMB-blocked framing, PowerShell Direct and SSH sessions, JEA limits, large-file speed, 5.0 minimum, parallel loop, hash verification step. Unchanged: -ToSession/-FromSession path semantics.
