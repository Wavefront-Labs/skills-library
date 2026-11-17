---
id: computing-software.it-support-helpdesk.remote-support-tools.remote-powershell-and-command-line-tools
name: remote-powershell-and-command-line-tools
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, powershell-remoting, winrm, psexec, sysinternals, invoke-command, enter-pssession, remote-registry, remote-event-viewer, headless-remediation, kerberos-double-hop, cimsession, remote-service-management, remote-registry-access]
level: practitioner
status: draft
description: "Headless remote administration beyond screen-sharing: PowerShell remoting/WinRM, PsExec, remote registry and event logs, for fixing or inspecting a machine without a GUI session."
sources:
  - "https://learn.microsoft.com/en-us/powershell/scripting/learn/remoting/running-remote-commands"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# remote-powershell-and-command-line-tools

Goal: fix or inspect a machine the user isn't present at, or faster than a
full remote-control session would allow, using command-line remoting —
distinct from the interactive-session tools covered in
`running-secure-remote-sessions`.

## PowerShell remoting (WinRM)
- `Enter-PSSession -ComputerName <HOST>` for an interactive remote shell;
  `Invoke-Command -ComputerName <HOST> -ScriptBlock { ... }` for one-shot
  commands against one or many machines in parallel (pass an array of
  names) — the latter is what you want for "run this fix on 40 machines,"
  not looping `Enter-PSSession` by hand.
- WinRM must be enabled on the target (`Enable-PSRemoting` on-prem, or an
  equivalent GPO/Intune-pushed firewall rule at scale — most modern
  domain-joined fleets have this via GPO already). If remoting fails with
  "WinRM cannot complete the operation," check the target is actually
  reachable and the WinRM service is running before assuming a
  permissions issue.
- **Kerberos double-hop problem**: a command run via `Invoke-Command`
  that itself tries to reach a *third* machine (e.g. a script that
  touches a file share) fails with access denied even though your
  credentials are valid, because the remote session can't forward your
  Kerberos ticket a second hop. Fix with CredSSP (`-Authentication
  CredSSP`, weaker security, needs enabling on both ends) or, better,
  constrained delegation configured by the domain admin — don't spend
  hours debugging permissions on the share before recognizing this
  pattern.
- Session reuse: `New-PSSession` + `Invoke-Command -Session $s` keeps a
  persistent connection across multiple commands — much faster than a
  fresh `Invoke-Command -ComputerName` per call when running several
  diagnostic steps in sequence.

## PsExec (Sysinternals)
- `PsExec \\<HOST> -s cmd` or `-i` for an interactive session in a given
  session ID — useful when WinRM isn't enabled but admin shares
  (`\\host\C$`) are reachable, since PsExec rides on SMB/RPC instead.
  First run against a new host triggers a EULA accept dialog unless
  `-accepteula` is passed — scripts that call PsExec unattended must
  include it or they'll hang waiting for a prompt that never shows on a
  headless run.
- `-s` runs as SYSTEM (useful for testing what a script will actually see
  when deployed via RMM/Intune as SYSTEM, matching the run-as-system
  context covered in the Intune remediation skill); without `-s` it runs
  as the connecting admin's own account, impersonated on the target.
- SMB/RPC must be reachable (ports 445, plus RPC endpoint mapper) —
  blocked on many segmented networks/VPNs by design; if PsExec can't
  connect, that's often a firewall/network segmentation fact, not a
  PsExec problem, and WinRM (port 5985/5986) may be the one that's open
  instead.

## Remote registry and event logs without a GUI session
- `Invoke-Command -ComputerName <HOST> -ScriptBlock { Get-ItemProperty
  'HKLM:\...' }` is the modern way to read/write a remote registry key —
  prefer this over the legacy Remote Registry service/`regedit`'s
  "Connect Network Registry," which needs that service running and is
  slower to script.
- `Get-WinEvent -ComputerName <HOST> -LogName <LOG>` or
  `-FilterHashtable` pulls remote event logs directly; needs the Remote
  Event Log Management firewall rule group enabled on the target (often
  on by default on domain-joined machines via GPO, not guaranteed on
  workgroup/home-joined devices).
- `Get-CimInstance -ComputerName <HOST> -ClassName Win32_...` (or a
  `CimSession` for repeated calls) is the modern replacement for
  `Get-WmiObject`, which is deprecated/removed in current PowerShell —
  don't write new scripts against WMI cmdlets directly.

## Gotchas
- None of this works if the target machine is asleep/hibernating or off
  — remote wake (Wake-on-LAN) is a separate, unreliable-at-scale
  mechanism; don't promise a fix "overnight" without confirming the
  machine stays awake or is already on.
- Credentials used for remoting are cached/transmitted per the auth
  method chosen (Kerberos by default on-domain, NTLM as fallback,
  explicit `-Credential` prompts) — avoid hardcoding admin passwords in
  scripts called across many machines; use a credential vault or
  gMSA/delegated rights scoped to what the task needs.
- A remote command that "hangs" is often waiting on user input the
  script didn't suppress (a confirmation prompt, `-Confirm`) on a session
  with no one to answer it — always test with `-Force`/non-interactive
  flags before running unattended at scale.

## Verify
- `Invoke-Command -ComputerName <HOST> -ScriptBlock { $env:COMPUTERNAME }`
  returns the expected hostname (confirms remoting path works end to
  end) before relying on it for a fleet-wide fix, and the actual change
  (registry value, service state, log entry) is confirmed present on the
  target after the command returns success, not assumed from exit code
  alone.
