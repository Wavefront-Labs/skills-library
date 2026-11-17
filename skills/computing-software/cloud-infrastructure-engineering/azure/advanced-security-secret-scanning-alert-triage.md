---
id: computing-software.cloud-infrastructure-engineering.azure.advanced-security-secret-scanning-alert-triage
name: advanced-security-secret-scanning-alert-triage
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, devsecops, secret-scanning-alerts, github-advanced-security, push-protection, credential-rotation]
level: advanced
status: docs-checked
description: "Triage GitHub Advanced Security for Azure DevOps secret scanning alerts: validate, rotate, dismiss with reason, handle push protection bypasses and history."
sources: ["https://learn.microsoft.com/azure/devops/repos/security/github-advanced-security-secret-scanning", "https://learn.microsoft.com/azure/devops/repos/security/configure-github-advanced-security-features", "https://learn.microsoft.com/azure/devops/repos/security/github-advanced-security-permissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret scanning alert triage

**Goal:** treat every leaked credential as compromised and close alerts with evidence.

## Where alerts come from
- **Repository scanning** finds secrets across all branches and history (one alert per unique credential) once Advanced Security (Secret Protection) is enabled.
- **Push protection** blocks pushes containing high-confidence secrets; a developer can bypass with `skip-secret-scanning:true` in the commit message, which still creates an alert.

## Triage workflow
1. **Identify**: secret type, file, commit, author, whether it reached the default branch, whether it is in a public place (wikis, logs, forks).
2. **Validate**: is it a real, active credential? (test in a safe way, or ask the owner; check if the provider reports it).
3. **Rotate first, clean history second**: revoke/rotate the credential at the provider (Azure Storage key rotation, Entra app secret delete, PAT revoke, third-party API key). Removing it from Git does not un-leak it.
4. **Replace usage** with Key Vault references, managed identity or workload identity federation.
5. **Close the alert** with a reason: *Risk accepted* or *False positive* (add a comment naming the rotation ticket), never just dismiss.
6. Optional: rewrite history if the secret cannot be rotated (rare) or for hygiene.

## Permissions
- Viewing a repository's alert summary needs Contributor on the repository; dismissing needs Project administrator or the *Advanced Security: Manage and dismiss alerts* permission (grant to the security team).

## Metrics
- Open alerts by age, mean time to rotate, push protection bypass count per repo; review bypasses weekly.

## Verify
- [ ] No open high-confidence alerts older than the SLA (for example 24-72 h); each closed alert references a rotation ticket.

## Checked

2026-10-28. Confirmed on the Azure DevOps secret scanning and permissions pages: skip-secret-scanning:true bypass still raises an alert; one alert per unique credential across branches and history; closure reasons Risk accepted and False positive; Contributor views the summary, Project administrator dismisses, permission named Advanced Security: Manage and dismiss alerts. Fixed: closure reasons (Revoked and Used in tests do not exist) and the dismiss permission name. Removed: portal navigation path and the filter list.

Method: documentation only; no commands were run.
