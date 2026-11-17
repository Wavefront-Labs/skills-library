---
id: computing-software.cloud-infrastructure-engineering.azure.app-configuration-providers-dotnet-java-python
name: app-configuration-providers-dotnet-java-python
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-configuration, app-config-provider, configuration-provider, dynamic-refresh, key-vault-references]
level: advanced
status: gated
description: "Load Azure App Configuration in .NET, Java Spring and Python with the configuration providers: label selection, Key Vault references, sentinel-key dynamic refresh."
sources: ["https://learn.microsoft.com/azure/azure-app-configuration/reference-dotnet-provider", "https://learn.microsoft.com/azure/azure-app-configuration/reference-kubernetes-provider", "https://learn.microsoft.com/azure/azure-app-configuration/quickstart-python-provider", "https://learn.microsoft.com/azure/azure-app-configuration/enable-dynamic-configuration-aspnet-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Configuration providers

**Goal:** apps read settings and feature flags from App Configuration with refresh, without bespoke code.

## .NET
```csharp
builder.Configuration.AddAzureAppConfiguration(o => {
  o.Connect(new Uri(endpoint), new DefaultAzureCredential())
   .Select("MyApp:*", LabelFilter.Null)                    // unlabeled defaults
   .Select("MyApp:*", builder.Environment.EnvironmentName)  // env label overrides (later wins)
   .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()))
   .ConfigureRefresh(r => r.Register("MyApp:Sentinel", refreshAll: true).SetRefreshInterval(TimeSpan.FromSeconds(30)))
   .UseFeatureFlags();
});
builder.Services.AddAzureAppConfiguration();
app.UseAzureAppConfiguration();       // triggers refresh on requests
```
Bind with `IOptionsSnapshot<T>` / `IOptionsMonitor<T>` to see refreshed values.

## Java Spring
Use the Spring Cloud Azure App Configuration starter with store endpoint, key/label filters and a monitoring trigger key; take the exact property names from the current Spring provider reference (not confirmed here).

## Python
The snippet below is (gated: unconfirmed, source is paywalled or blocked).
```python
from azure.appconfiguration.provider import load, SettingSelector
from azure.identity import DefaultAzureCredential
cfg = load(endpoint=ep, credential=DefaultAzureCredential(),
           selects=[SettingSelector(key_filter="MyApp:*", label_filter="\0"), SettingSelector(key_filter="MyApp:*", label_filter="prod")],
           trim_prefixes=["MyApp:"], keyvault_credential=DefaultAzureCredential(),
           refresh_on=[("MyApp:Sentinel", "\0")], refresh_interval=30)
cfg.refresh()   # call periodically or per request
```
Kubernetes: the App Configuration Kubernetes Provider syncs to ConfigMaps/Secrets via an `AzureAppConfigurationProvider` CR.

## Practices
- **Sentinel key**: update it last after a batch of changes so clients reload consistently.
- Give the app identity `App Configuration Data Reader` (and `Key Vault Secrets User` for references).
- Use App Configuration replicas for resilience; the providers support failover to replicas (see the provider reference).

## Verify
- [ ] Change a value, then the sentinel; app reflects it within the refresh interval without restart.

## Checked

2026-10-28. Confirmed on the .NET provider reference: App Configuration Data Reader role, SetRefreshInterval default 30 seconds (also for feature flags), refresh middleware checks on request once the interval has elapsed, AzureAppConfigurationProvider resource for the Kubernetes provider. Removed: Spring property and artifact names and the replica discovery option name. Gated: the Python snippet (refresh_on and refresh_interval arguments not confirmed in the fetched pages).

Method: documentation only; no commands were run.
