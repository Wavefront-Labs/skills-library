---
id: computing-software.systems-network-administration.powershell.dsc-pull-server-and-azure-automation
name: dsc-pull-server-and-azure-automation
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, dsc, dsc-pull-server, lcm, azure-automation-state-configuration]
level: advanced
status: docs-checked
description: "Run DSC in pull mode: LCM ConfigurationRepositoryWeb settings, registration keys, configuration names, reporting, and migrating off Azure Automation State Configuration."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/pull-server/pullserver
  - https://learn.microsoft.com/en-us/azure/governance/machine-configuration/whats-new/migrating-from-azure-automation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DSC pull server and Azure Automation State Configuration

In pull mode nodes fetch their MOF configurations and resources periodically from a server and report status.

## LCM configuration for pull (WMF 5.1)
```powershell
[DSCLocalConfigurationManager()]
configuration PullClient {
  Node 'SRV01' {
    Settings {
      RefreshMode = 'Pull'; ConfigurationMode = 'ApplyAndAutoCorrect'
      RefreshFrequencyMins = 30; ConfigurationModeFrequencyMins = 15; RebootNodeIfNeeded = $false
    }
    ConfigurationRepositoryWeb PullSrv {
      ServerURL = 'https://dscpull.corp.example.com:8080/PSDSCPullServer.svc'
      RegistrationKey = '<guid-from-pull-server>'
      ConfigurationNames = @('WebServerBaseline')
    }
    ReportServerWeb PullSrv { ServerURL = 'https://dscpull.corp.example.com:8080/PSDSCPullServer.svc'; RegistrationKey = '<guid>' }
  }
}
PullClient -OutputPath .\lcm
Set-DscLocalConfigurationManager -Path .\lcm -Verbose
```

## Server side
- Windows pull server: the `DSC-Service` feature plus xPSDesiredStateConfiguration's `xDscWebService` resource.
  Place configuration MOFs and their checksum files (`New-DscChecksum`, which writes `<name>.mof.checksum`) in the
  ConfigurationPath folder; recreate the checksum whenever the MOF changes. Package resource modules as
  `<Module Name>_<Module Version>.zip` in ModulePath, with a checksum from `New-DscChecksum`.
- The Windows pull server (`DSC-Service`) is supported but has no plans for new features. Options: the SQL Server
  provider (`SqlProvider`, `SqlConnectionString` on xDscWebService) and community solutions such as Tug.
- No `ConfigurationID` in the metaconfiguration means the V2 protocol with registration; a `ConfigurationID` means V1
  with no registration.

## Azure Automation State Configuration
Azure Automation State Configuration is retired on September 30, 2027. Migrate to **Azure Machine Configuration**
(Azure Policy), which includes hybrid support through Arc-enabled servers; onboard each node to Azure Arc before
removing it from Automation State Configuration.

## Operate
```powershell
Update-DscConfiguration -Wait -Verbose         # pull now
Get-DscConfigurationStatus                     # last run result
```

## Verify
- [ ] `Get-DscConfigurationStatus` on the node shows the last pull succeeded; the report server receives status.

## Checked
2026-11-09. Read the Learn DSC Pull Service page and the Azure Machine Configuration migration page. Confirmed:
ConfigurationRepositoryWeb and ReportServerWeb settings, RegistrationKey, ConfigurationNames, module zip naming,
New-DscChecksum, SQL option, community options, V1/V2 protocol note, retirement date and Arc onboarding. Removed:
"in maintenance" wording, "new onboarding closed", Compliant-status wording. The server URL and configuration name
in the example are placeholders.
Method: documentation only; no commands were run.
