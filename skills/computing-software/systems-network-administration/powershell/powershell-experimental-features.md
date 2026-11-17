---
id: computing-software.systems-network-administration.powershell.powershell-experimental-features
name: powershell-experimental-features
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-environment, experimental-features, enable-experimentalfeature, powershell-7, config-json]
level: practitioner
status: verified
description: "Discover, enable and disable PowerShell 7 experimental features with Get/Enable-ExperimentalFeature, scope them to user or machine, and avoid depending on them in production."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/experimental-features
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enable-experimentalfeature
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell experimental features

PowerShell 7 ships some features off by default so they can change before becoming mainstream. Enabling one writes
to `powershell.config.json` and takes effect in **new** sessions.

## List and enable
```powershell
Get-ExperimentalFeature | ft Name,Enabled,Description -Wrap
Enable-ExperimentalFeature -Name PSLoadAssemblyFromNativeCode -Scope CurrentUser
Disable-ExperimentalFeature -Name PSLoadAssemblyFromNativeCode
```
The list depends on the version: 7.6.7 listed only `PSLoadAssemblyFromNativeCode`, `PSProfileDSCResource` and
`PSSerializeJSONLongEnumAsNumber`, and `Enable-ExperimentalFeature -Name PSFeedbackProvider` failed with `No experimental feature
was found that matched the name 'PSFeedbackProvider'` because it graduated in 7.6. Always list first.
Scopes: `CurrentUser` (`powershell.config.json` in the folder of `$PROFILE.CurrentUserCurrentHost`, normally
`Documents\PowerShell`), `AllUsers` (`$PSHOME\powershell.config.json`, needs admin). Start a new `pwsh` to apply (the cmdlet
prints that warning).

## Config file
```json
{ "ExperimentalFeatures": ["PSLoadAssemblyFromNativeCode"] }
```
This is the exact shape `Enable-ExperimentalFeature -Scope AllUsers` wrote (alongside other settings such as `ExecutionPolicy`);
`Disable-ExperimentalFeature` left `"ExperimentalFeatures": []`. Check inside a script:
`$EnabledExperimentalFeatures -contains 'PSLoadAssemblyFromNativeCode'` or `[ExperimentalFeature]::IsEnabled('...')` (both
returned True after enabling).

## Lifecycle
- Features graduate to mainstream (then no longer listed), or are removed.
- Microsoft's experimental-features table shows the history: `PSCommandNotFoundSuggestion` was experimental in 7.4 and mainstream
  in 7.5; `PSFeedbackProvider` was experimental in 7.4 and 7.5 and mainstream in 7.6; `PSNativePSPathResolution` was discontinued
  in 7.3.
- Release notes per version list what graduated.

## Rules for production
- Don't make production scripts depend on an experimental feature; gate with the check above.
- `AllUsers` scope on servers changes behaviour for every script on the box; prefer CurrentUser for trials.
- Module authors can declare experimental features in the manifest (`PrivateData.PSData.ExperimentalFeatures`) and
  use `[Experimental()]` attributes.

## Verify
- [ ] `Get-ExperimentalFeature` shows the expected state in a new session; scripts behave the same with the feature off.

## Checked
Ran on PowerShell 7.6.7 using a scratch `-SettingsFile` so no user config was touched: `Get-ExperimentalFeature` (three features),
the failed `PSFeedbackProvider` enable, `Enable-ExperimentalFeature -Scope AllUsers` for `PSLoadAssemblyFromNativeCode` (the file
content), a fresh session's `Get-ExperimentalFeature`, `$EnabledExperimentalFeatures`, `[ExperimentalFeature]::IsEnabled`, and
`Disable-ExperimentalFeature`. The CurrentUser location, the feature history table, the manifest property and `[Experimental()]` attribute come
from about_PowerShell_Config, the experimental-features page and about_Experimental_Features in the PowerShell docs. The CurrentUser scope
itself was not run (it would write to the real profile folder).
