---
id: computing-software.software-engineering.csharp-dotnet.user-secrets-and-configuration-providers
name: user-secrets-and-configuration-providers
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-generic-host, user-secrets, configuration-providers, environment-variables, appsettings, secret-management]
level: practitioner
status: docs-checked
description: "Handle .NET configuration and secrets: provider order, dotnet user-secrets for development, environment variable naming with double underscore, and keeping secrets out of source."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets", "https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration", "https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration-providers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User secrets and configuration providers

## Provider order (later wins)
`Host.CreateApplicationBuilder` provides default configuration, from lowest to highest priority: a chained existing `IConfiguration`, `appsettings.json`, `appsettings.{Environment}.json`, app secrets (only in the Development environment), environment variables, command-line arguments. Adding a provider overrides earlier values, so the last one added wins. Other providers exist, for example key-per-file (`AddKeyPerFile`, which takes an absolute directory path) and the Azure Key Vault provider for Azure test and production secrets.

## Development secrets (Secret Manager)
```bash
dotnet user-secrets init                                  # adds <UserSecretsId> (a GUID by default) to the project file
dotnet user-secrets set "Movies:ServiceApiKey" "12345"
dotnet user-secrets list
dotnet user-secrets remove "Movies:ServiceApiKey"
dotnet user-secrets clear
```
- Secrets are stored outside the project tree and are not checked into source control. They live in `secrets.json` under the user profile: `%APPDATA%\Microsoft\UserSecrets\<user_secrets_id>\secrets.json` on Windows, `~/.microsoft/usersecrets/<user_secrets_id>/secrets.json` on Linux and macOS.
- They are **not encrypted**; Secret Manager is for development only and not a trusted store. Do not write code that depends on the storage location or format.
- Use `--project <path>` to target a project from another directory.
- If `GenerateAssemblyInfo` is false, add `UserSecretsIdAttribute` manually.

## Environment variables
The colon separator does not work on all platforms (Bash does not support it); all platforms support a double underscore, which is replaced with a colon: `ConnectionStrings__Db=...`, `Logging__LogLevel__Default=Debug`. Environment variables override all previously specified sources but are commonly stored as plain unencrypted text. `AddEnvironmentVariables(prefix: "CustomPrefix_")` loads variables with that prefix and strips it. The default configuration also loads `DOTNET_`-prefixed variables, which .NET uses for host and app configuration, not user configuration.

## Other facts
- Configuration keys are case-insensitive.
- Never store passwords or other sensitive data in source code or configuration files; access production secrets through a controlled means such as Azure Key Vault, and do not deploy development secrets with the app.

## Checked
2026-11-08. Confirmed against the ASP.NET Core "Safe storage of app secrets in development" page (Secret Manager commands, paths, no encryption, environment variable warning and double underscore), the .NET "Configuration" page (default provider order for Host.CreateApplicationBuilder, last-added wins) and the "Configuration providers" page (case-insensitive keys, prefixes, DOTNET_ prefix, AddKeyPerFile). Removed as unconfirmed: the WebApplication.CreateBuilder wording and /run/secrets path, environment-variable array syntax, the options validation snippet and reloadOnChange/IOptionsMonitor remarks, and the log-redaction and ASPNETCORE_ENVIRONMENT advice.
Method: documentation only; no commands were run.
