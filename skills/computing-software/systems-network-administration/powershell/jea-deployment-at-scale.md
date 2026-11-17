---
id: computing-software.systems-network-administration.powershell.jea-deployment-at-scale
name: jea-deployment-at-scale
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, just-enough-administration, jea-deployment, dsc, jeadsc, module-distribution, configuration-management]
level: advanced
status: docs-checked
description: "Deploy JEA to many machines with the JustEnoughAdministration DSC resource: prerequisites, File plus JeaEndpoint configuration, properties, backup restricted endpoint."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/register-jea#multi-machine-deployment-with-dsc
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/register-jea
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JEA deployment at scale (DSC)

The register-jea page calls the JEA Desired State Configuration resource the simplest model for several machines.

## Prerequisites
- Role capabilities authored and added to a PowerShell module.
- That module stored on a read-only file share reachable by each machine.
- Session configuration settings decided (no `.pssc` file is needed with the DSC resource).
- Credentials allowing administrative actions on each machine, or access to the DSC pull server managing them.
- The JEA DSC resource downloaded.

## Configuration shape
The **File** resource copies the role-capability module from the share; the **JustEnoughAdministration** resource's `JeaEndpoint` defines the endpoint:
```powershell
Configuration JEAMaintenance
{
    Import-DscResource -Module JustEnoughAdministration, PSDesiredStateConfiguration
    File MaintenanceModule {
        SourcePath = "<share>\ContosoMaintenance"
        DestinationPath = "<ProgramFiles>\WindowsPowerShell\Modules\ContosoMaintenance"
        Checksum = "SHA-256"; Ensure = "Present"; Type = "Directory"; Recurse = $true
    }
    JeaEndpoint JEAMaintenanceEndpoint {
        EndpointName = "JEAMaintenance"
        RoleDefinitions = "@{ 'CONTOSO\JEAMaintenanceAuditors' = @{ RoleCapabilities = 'GeneralServerMaintenance-Audit' } }"
        TranscriptDirectory = '<ProgramData>\JEAConfiguration\Transcripts'
        DependsOn = '[File]MaintenanceModule'
    }
}
```
- Configurable properties: role definitions, virtual account groups, gMSA name, transcript directory, user drive, conditional access rules, startup scripts. Syntax matches the session configuration file.
- Apply by invoking the Local Configuration Manager directly or by updating the pull server configuration.
- The resource can replace the default **Microsoft.PowerShell** endpoint; it then registers a backup endpoint **Microsoft.PowerShell.Restricted** with the default WinRM ACL (Remote Management Users and local Administrators).

## Cautions
Registering restarts WinRM, ending remoting sessions and ongoing DSC configurations; the page recommends taking production machines offline. Updating an endpoint means unregistering and re-registering under the same name (also restarts WinRM).

## Checked
Method: 2026-11-08 docs-only read of the JEA register-jea page (MicrosoftDocs/PowerShell-Docs markdown). Dropped the Invoke-Command push, versioned-module and consistency-check advice, which the page does not state. Unchanged: DSC as the multi-machine route.
