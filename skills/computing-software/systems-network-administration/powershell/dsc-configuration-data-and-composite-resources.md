---
id: computing-software.systems-network-administration.powershell.dsc-configuration-data-and-composite-resources
name: dsc-configuration-data-and-composite-resources
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-dsc, composite-resources, configuration-data, allnodes, dsc]
level: advanced
status: docs-checked
description: "Separate DSC configuration from environment data with ConfigurationData (AllNodes, roles) and package reusable building blocks as composite resources."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/configurations/configdata?view=dsc-1.1
  - https://learn.microsoft.com/en-us/powershell/dsc/resources/authoringresourcecomposite?view=dsc-1.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DSC configuration data and composite resources

## ConfigurationData: one configuration, many environments
```powershell
$cd = @{
  AllNodes = @(
    @{ NodeName = '*'; LogPath = '<DATA_VOLUME>\Logs'; PSDscAllowDomainUser = $true }
    @{ NodeName = 'WEB01'; Role = 'Web'; Site = 'Shop' }
    @{ NodeName = 'SQL01'; Role = 'Sql' }
  )
  NonNodeData = @{ DnsServers = '10.0.10.11','10.0.10.12' }
}
Configuration Estate {
  Import-DscResource -ModuleName PSDscResources
  Node $AllNodes.Where({ $_.Role -eq 'Web' }).NodeName {
    WindowsFeature IIS { Name = 'Web-Server'; Ensure = 'Present' }
    File Logs { DestinationPath = $Node.LogPath; Type = 'Directory'; Ensure = 'Present' }
  }
}
Estate -ConfigurationData $cd -OutputPath .\mof
```
`ConfigurationData` is a hashtable that must have an `AllNodes` key (an array of hashtables, each with a `NodeName`);
other keys such as `NonNodeData` are optional. A `NodeName = '*'` entry applies its properties to all nodes.
`$AllNodes` is the whole collection, filterable with `.Where()` and `.ForEach()`; `$Node` is the current entry after
filtering.

## Composite resources: reuse blocks
A composite resource is a configuration packaged as a resource.
```text
ContosoDsc\
  ContosoDsc.psd1
  DSCResources\
    WebBaseline\
      WebBaseline.psd1            # RootModule = 'WebBaseline.schema.psm1'
      WebBaseline.schema.psm1     # Configuration WebBaseline { param($SiteName) ... }
```
```powershell
Configuration WebBaseline { param([string]$SiteName)
  Import-DscResource -ModuleName PSDscResources
  WindowsFeature IIS { Name = 'Web-Server'; Ensure = 'Present' }
  WindowsFeature AspNet { Name = 'Web-Asp-Net45'; Ensure = 'Present' }
}
# use it
Node WEB01 { WebBaseline Base { SiteName = 'Shop' } }
```

Save the parameterized configuration as `<Name>.schema.psm1` under `DSCResources\<Name>\`, with a `<Name>.psd1`
manifest containing `RootModule = '<Name>.schema.psm1'`, in addition to the module manifest for the parent module. The
resource is then discoverable with `Get-DscResource`.

## Notes
- Credentials in configuration data need certificate encryption (see dsc-credentials-encryption).

## Verify
- [ ] Compiling produces one MOF per node with the right role settings; the composite appears in `Get-DscResource`.

## Checked
2026-11-09. Read the Learn DSC 1.1 pages on ConfigurationData and on authoring composite resources. Confirmed: the
AllNodes/NodeName structure, NodeName '*', NonNodeData, $AllNodes/$Node with Where/ForEach, the schema.psm1 and psd1
layout, RootModule, Get-DscResource discovery. Removed as unconfirmed: DependsOn limits across composite boundaries,
composites-are-versioned-modules remark, per-environment source-control advice.
Method: documentation only; no commands were run.
