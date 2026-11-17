---
id: computing-software.systems-network-administration.powershell.dsc-and-configuration-management
name: dsc-and-configuration-management
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, dsc, desired-state-configuration, psdesiredstateconfiguration, dsc-v3, dsc-exe, lcm, local-configuration-manager, mof, configuration, node, resources, dsc-resources, psdscresources, computermanagementdsc, networkingdsc, start-dscconfiguration, test-dscconfiguration, get-dscconfigurationstatus, applyandautocorrect, applyandmonitor, push-mode, pull-server, azure-machine-configuration, azure-automation-dsc, configuration-data, credentials, certificate-encryption, drift, idempotent, configuration-management, ansible]
level: advanced
status: draft
description: "Declare and enforce Windows server state with PowerShell DSC: configurations, MOFs, LCM modes, resources, config data, credential encryption, drift checks, DSC v3 and Machine Configuration."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/overview
  - https://learn.microsoft.com/en-us/powershell/dsc/managing-nodes/metaconfig
  - https://learn.microsoft.com/en-us/azure/governance/machine-configuration/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DSC and configuration management — declare the server, let the engine converge it

**Goal:** describe a Windows server's configuration as code, apply it idempotently,
detect drift, and choose the right DSC generation for a new project.

## 0. Which DSC? (decide first)
| Generation | Runs on | Engine | Status (verify — this has moved fast) |
|---|---|---|---|
| **PSDSC 1.1** (`PSDesiredStateConfiguration`, in-box) | Windows PowerShell 5.1 | LCM service, MOF files, push/pull | Mature, in maintenance; most community resources target it |
| **PSDSC 2.x** module | PowerShell 7 | No LCM; used via Machine Configuration or `Invoke-DscResource` | Not a standalone push/pull platform |
| **DSC v3** (`dsc` CLI) | Windows/Linux/macOS | Stateless CLI, JSON/YAML documents | GA in 2025; resources in any language; can call PS resources via adapters |
| **Azure Machine Configuration** | Azure and Arc-enabled servers | Guest agent + PSDSC 2.x packages | Microsoft's successor to Azure Automation State Configuration (being retired) |

New estate with Ansible/Intune already: DSC may be redundant. Existing Windows-only
on-prem estate: PSDSC 1.1 push is still the simplest way to start; this skill uses it.

## 1. A configuration
```powershell
Configuration WebBaseline {
  param([string[]]$NodeName = 'localhost')
  Import-DscResource -ModuleName PSDscResources, ComputerManagementDsc
  Node $NodeName {
    WindowsFeature IIS { Name = 'Web-Server'; Ensure = 'Present' }
    Service W3SVC { Name = 'W3SVC'; StartupType = 'Automatic'; State = 'Running'; DependsOn = '[WindowsFeature]IIS' }
    Registry NoSMB1 {
      Key = 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters'
      ValueName = 'SMB1'; ValueData = '0'; ValueType = 'Dword'; Ensure = 'Present'
    }
    TimeZone TZ { IsSingleInstance = 'Yes'; TimeZone = 'UTC' }
  }
}
WebBaseline -NodeName web01, web02 -OutputPath .\out     # compiles one MOF per node
```
- Install resource modules (**the same version**) on the authoring machine *and* every
  target node; version mismatches fail at apply time. Pin with
  `Import-DscResource -ModuleName X -ModuleVersion 1.2.3`.
- Prefer `PSDscResources` over the in-box `PSDesiredStateConfiguration` resources, and
  community `*Dsc` modules (ComputerManagementDsc, NetworkingDsc, SqlServerDsc).
- Each resource instance needs a unique key; two resources managing the same setting
  with different values cause endless flip-flopping.

## 2. Configure the LCM, then push
```powershell
[DscLocalConfigurationManager()] Configuration Lcm {
  Node 'web01' { Settings {
    ConfigurationMode = 'ApplyAndAutoCorrect'   # or ApplyAndMonitor = detect only
    ConfigurationModeFrequencyMins = 30         # consistency check (min 15)
    RebootNodeIfNeeded = $false
    ActionAfterReboot = 'ContinueConfiguration'
  } }
}
Lcm -OutputPath .\lcm; Set-DscLocalConfigurationManager -Path .\lcm -Verbose
Start-DscConfiguration -Path .\out -ComputerName web01 -Wait -Verbose
```
Push requires WinRM to the node. Start new baselines with **ApplyAndMonitor** to see
drift before letting DSC fix it; switch to AutoCorrect once reports are clean.
`RebootNodeIfNeeded = $true` on servers can reboot production mid-day — tie it to
maintenance windows.

## 3. Drift and status
```powershell
Test-DscConfiguration -ComputerName web01 -Detailed      # InDesiredState + which resources aren't
Get-DscConfigurationStatus -CimSession web01 -All
Get-WinEvent -LogName 'Microsoft-Windows-Dsc/Operational' -MaxEvents 20
```
DSC also flags drift caused by GPOs — if Group Policy and DSC set the same registry
value differently, they fight every refresh. Give each setting one owner.

## 4. Configuration data and secrets
Separate structure from environment:
```powershell
$cd = @{ AllNodes = @(
  @{ NodeName = '*'; PSDscAllowDomainUser = $true; CertificateFile = '<CERT_DIR>\dsc.cer' }
  @{ NodeName = 'web01'; Role = 'Web' } ) }
WebBaseline -ConfigurationData $cd
```
Credentials in a MOF are **plain text** unless you encrypt with a per-node
document-encryption certificate (`CertificateFile` + LCM `CertificateID`).
`PSDscAllowPlainTextPassword = $true` is for labs only. Never commit MOFs.

## 5. DSC v3 in one look
```yaml
# web.dsc.yaml
$schema: https://aka.ms/dsc/schemas/v3/bundled/config/document.json
resources:
- name: no-smb1
  type: Microsoft.Windows/Registry
  properties: { keyPath: 'HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters', valueName: SMB1, valueData: { DWord: 0 } }
```
`dsc config test --file web.dsc.yaml` then `dsc config set --file web.dsc.yaml`. No
background agent: schedule it or drive it from another tool. Schema URLs and resource
type names were still evolving — copy from current docs, not from this sketch.

## Verify
- [ ] Resource module versions match on author box and nodes.
- [ ] `Test-DscConfiguration -Detailed` returns InDesiredState = True on every node.
- [ ] Drift test: change a managed setting by hand; the next consistency run reports (Monitor) or reverts (AutoCorrect) it.
- [ ] No plaintext credentials in MOFs; MOFs and certificates are outside source control.
- [ ] No setting is managed by both GPO and DSC.
