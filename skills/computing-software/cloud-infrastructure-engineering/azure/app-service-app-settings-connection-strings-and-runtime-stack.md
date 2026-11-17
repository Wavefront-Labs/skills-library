---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-app-settings-connection-strings-and-runtime-stack
name: app-service-app-settings-connection-strings-and-runtime-stack
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, appsettings-config, connection-strings, runtime-stack, slot-settings, linux-fx-version]
level: practitioner
status: docs-checked
description: "Configure App Service apps: app settings and connection strings as env vars, nested keys, slot-sticky settings, bulk edits, and choosing/upgrading the runtime stack."
sources: ["https://learn.microsoft.com/en-us/azure/app-service/configure-common", "https://learn.microsoft.com/en-us/azure/app-service/configure-language-dotnetcore", "https://learn.microsoft.com/en-us/azure/app-service/configure-language-nodejs", "https://learn.microsoft.com/en-us/azure/app-service/language-support-policy", "https://learn.microsoft.com/en-us/cli/azure/webapp/config/appsettings", "https://learn.microsoft.com/en-us/cli/azure/webapp/config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App settings, connection strings and runtime stack

**Goal:** configuration outside the code, correct per slot, on a supported runtime.

## App settings
```bash
az webapp config appsettings set -g rg -n app-orders --settings \
  ASPNETCORE_ENVIRONMENT=Production Logging__LogLevel__Default=Warning FeatureX__Enabled=true
az webapp config appsettings set -g rg -n app-orders --slot staging --slot-settings ENVIRONMENT_NAME=staging
az webapp config appsettings list -g rg -n app-orders -o table
az webapp config appsettings delete -g rg -n app-orders --setting-names OLD_SETTING
```
- Exposed to the app as **environment variables**. In setting names replace a colon (`:`) with a double underscore (`__`) and a period (`.`) with a single underscore (`_`); for example `ApplicationInsights:InstrumentationKey` becomes `ApplicationInsights__InstrumentationKey`.
- `--slot-settings` makes a setting **sticky** to the slot (doesn't move on swap) - use for environment names,
  slot-specific endpoints, feature flags under test.
- Adding, removing or editing a setting restarts the app. Bulk edit with the portal's advanced edit (JSON) or JSON file input to the CLI.

## Connection strings
```bash
az webapp config connection-string set -g rg -n app-orders -t SQLAzure --settings OrdersDb='<connection string>'
```
Exposed with a type prefix: `SQLAZURECONNSTR_OrdersDb` (Azure SQL), `SQLCONNSTR_` (SQL Server), `MYSQLCONNSTR_`, `POSTGRESQLCONNSTR_`,
`CUSTOMCONNSTR_`, plus `NOTIFICATIONHUBCONNSTR_`, `SERVICEBUSCONNSTR_`, `EVENTHUBCONNSTR_`, `DOCDBCONNSTR_` and `REDISCACHECONNSTR_`. Prefer managed identity or Key
Vault references over secrets in connection strings.

## Runtime stack
```bash
az webapp list-runtimes --os-type linux -o table
az webapp config show -g rg -n app-orders --query "{linux:linuxFxVersion,net:netFrameworkVersion}"
az webapp config set -g rg -n app-orders --linux-fx-version "DOTNETCORE|8.0"
az webapp config set -g rg -n app-orders --linux-fx-version "NODE|24-lts"
```
- Track the language support policy: App Service follows community support timelines. After a runtime's end of support, apps keep running, but App Service can't provide security patches or support for that version, and you must upgrade to get support. App Service controls minor and patch versions (use a custom container if you need a specific one).
- Upgrade in a staging slot first, then swap.

## Gotchas
- Settings defined in IaC overwrite portal edits on next deploy (and vice versa drift) - pick one owner.
- Values with special characters need quoting in CLI; JSON file input avoids shell escaping issues.
- `WEBSITE_*` and `SCM_*` settings change platform behaviour - document any you set.

## Verify
- [ ] Kudu/SSH `env` shows expected variables; staging slot keeps its sticky settings after a swap; runtime is a supported version.

## Checked
Checked 2026-10-24 against azure-docs app-service pages (configure-common, configure-language-dotnetcore, configure-language-nodejs, language-support-policy) and the azure-docs-cli webapp reference (appsettings set, list, delete, connection-string set, config set --linux-fx-version, list-runtimes flags exist). Confirmed: colon to double underscore and period to underscore in names; restart on change; connection string type prefixes; --slot-settings; DOTNETCORE|8.0 and NODE|24-lts syntax; support policy wording. Found stale and fixed: the Node 20 example (the docs show NODE|24-lts), the incomplete connection string prefix list, the Linux-only explanation of the double underscore rule. Removed unconfirmed: the managed identity connection string keyword example and the .NET ConnectionStrings mapping note.

Method: documentation only; no commands were run.
