---
id: computing-software.cloud-infrastructure-engineering.azure.bicepconfig-and-bicep-linter-rules
name: bicepconfig-and-bicep-linter-rules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, bicepconfig, linter-rules, bicep-lint, module-aliases, ci-quality-gates]
level: practitioner
status: docs-checked
description: "Configure bicepconfig.json: linter rule levels, rules worth making errors, module registry aliases, and running bicep lint with SARIF output in CI."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/bicep/bicep-config", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/linter", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/bicep-config-linter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bicepconfig.json and linter rules

**Goal:** Bicep code reviewed by a machine before a human: secrets, hard-coded URLs and sloppy parameters fail the build.

## bicepconfig.json (repo root; nearest file up the tree wins)
```json
{
  "analyzers": {
    "core": {
      "enabled": true,
      "rules": {
        "no-hardcoded-env-urls": { "level": "error" },
        "secure-secrets-in-params": { "level": "error" },
        "outputs-should-not-contain-secrets": { "level": "error" },
        "use-secure-value-for-secure-inputs": { "level": "error" },
        "protect-commandtoexecute-secrets": { "level": "error" },
        "no-unused-params": { "level": "warning" },
        "no-unused-vars": { "level": "warning" },
        "no-unnecessary-dependson": { "level": "warning" },
        "explicit-values-for-loc-params": { "level": "warning" },
        "use-recent-api-versions": { "level": "warning" },
        "use-resource-symbol-reference": { "level": "warning" }
      }
    }
  },
  "moduleAliases": {
    "br": {
      "corp": { "registry": "crplatform.azurecr.io", "modulePath": "bicep/modules" },
      "public": { "registry": "mcr.microsoft.com", "modulePath": "bicep" }
    }
  }
}
```
With aliases: `module kv 'br/corp:keyvault:1.4.0' = { ... }` and `br/public:avm/res/key-vault/vault:<version>`.

## Run in CI
```bash
az bicep install && az bicep upgrade
az bicep lint --file main.bicep --diagnostics-format sarif > bicep.sarif   # upload to code scanning
bicep build main.bicep                                                      # errors fail the step
```
Promote the rules you care about to `error` so the build fails on them.

## Suppressing a finding (sparingly)
```bicep
#disable-next-line no-hardcoded-env-urls
var legacyEndpoint = 'https://management.core.windows.net/'
```
Require a comment explaining why in code review.

## Gotchas
- The nearest `bicepconfig.json` up the directory tree wins, so open the repo root in VS Code.
- The linter checks the template only; pair it with what-if.

## Verify
- [ ] Pipeline fails on a test commit with a hard-coded `management.azure.com` URL; SARIF results appear in code scanning.

## Checked
2026-10-28. Confirmed on the Bicep config and linter pages: nearest bicepconfig.json wins, `moduleAliases`, rule names no-hardcoded-env-urls, secure-secrets-in-params, outputs-should-not-contain-secrets, use-secure-value-for-secure-inputs, protect-commandtoexecute-secrets, no-unnecessary-dependson, explicit-values-for-loc-params, use-recent-api-versions, use-resource-symbol-reference. check_commands confirmed `az bicep lint --diagnostics-format`. Removed: `maxAllowedAgeInDays` value, default-level claim for use-recent-api-versions, error-versus-warning build behaviour, VS Code and Azure-validation claims.
Method: documentation only; no commands were run.
