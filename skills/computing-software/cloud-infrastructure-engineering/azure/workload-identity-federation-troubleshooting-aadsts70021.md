---
id: computing-software.cloud-infrastructure-engineering.azure.workload-identity-federation-troubleshooting-aadsts70021
name: workload-identity-federation-troubleshooting-aadsts70021
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, wif-troubleshooting, aadsts70021, subject-mismatch, oidc, github-actions]
level: practitioner
status: docs-checked
description: "Fix workload identity federation login failures: decode the OIDC token, match issuer/subject/audience, and resolve AADSTS70021, 700211, 700213 and 700024."
sources: ["https://learn.microsoft.com/entra/workload-id/workload-identity-federation-create-trust", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations", "https://learn.microsoft.com/azure/devops/pipelines/release/troubleshoot-workload-identity", "https://login.microsoftonline.com/error"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot workload identity federation

**Goal:** turn "AADSTS70021: No matching federated identity record found" into a one-line fix.

## The match rule
Entra compares the external token to each federated credential on the app/managed identity:
**issuer** exact, **subject** exact and case-sensitive (or flexible expression), **audience** in the list
(normally `api://AzureADTokenExchange`).

## Error map
| Code | Meaning | Look at |
|---|---|---|
| AADSTS70021 | No FIC matched the assertion | issuer + subject + audience together |
| AADSTS700211 | No FIC matched the presented assertion **issuer** | issuer URL (exact match, no leading or trailing whitespace; ADO issuer form) |
| AADSTS700213 | No FIC matched the presented assertion **subject** | subject string |
| AADSTS700024 | Client assertion is not within its valid time range | token expired (long job) or clock |
| AADSTS70025 | The client has no configured federated identity credentials | wrong client ID |

## See what the token actually says
Request the workflow's OIDC ID token for audience `api://AzureADTokenExchange` (see GitHub's OIDC documentation), decode the payload (second dot-separated segment, base64url) and print only `iss`, `sub` and `aud`, never the token itself.
Typical GitHub subjects:
- `repo:org/repo:ref:refs/heads/main` (branch), `repo:org/repo:environment:prod` (job with `environment:` - this
  **replaces** the ref form), `repo:org/repo:pull_request`, `repo:org/repo:ref:refs/tags/v1.2.3`.
Azure DevOps has two issuer forms: the Azure DevOps issuer `https://vstoken.dev.azure.com/<organization id>` with subject `sc://<organization name>/<project name>/<service connection name>`, and, for new service connections, the Microsoft Entra issuer `https://login.microsoftonline.com/<tenant id>/v2.0` with subject `<microsoft entra prefix>/sc/<organization id>/<service connection id>`. Editing and saving the service connection updates the issuer URL (for identities Azure DevOps did not create, update it manually). AADSTS700223 or AADSTS700238 means workload identity federation is disabled in the tenant.

## Compare with what's configured
```bash
az ad app federated-credential list --id <appId>
az identity federated-credential list -g <rg> --identity-name <uami> -o table
```

## Usual culprits
- Job uses `environment:` but FIC was created for the branch subject (or vice versa).
- Repo or org renamed (GitHub subjects contain names).
- Wrong `client-id` (pointing at an app without the FIC) or wrong tenant.
- Long jobs: the federated assertion has a limited validity window (AADSTS700024); re-authenticate before late steps that need Azure, or split the job.
- Newly created FIC: allow several minutes for propagation within the region.
- A wrong subject is accepted when the credential is created and only fails at exchange, without a specific error until then.

## Verify
- [ ] Decoded `iss`/`sub`/`aud` exactly equal one listed credential; login step succeeds on rerun.

## Checked
Date: 2026-10-24. Checked against the Microsoft Entra error lookup service (login.microsoftonline.com/error?code=70021, 700211, 700213, 700024, 70025), MicrosoftDocs/entra-docs `docs/workload-id` (create-trust, considerations; main branch) and MicrosoftDocs/azure-devops-docs `troubleshoot-workload-identity` (main branch).
- Confirmed: meanings of AADSTS70021, 700211 (issuer), 700213 (subject), 700024 (assertion time range) and 70025 (no federated credentials); both Azure DevOps issuer/subject forms and the AADSTS700223/700238 tenant-disabled case; GitHub environment subject form; issuer whitespace rule; subject error behaviour; propagation delay.
- Removed as unconfirmed: the `actions/github-script` snippet and its version pin, the `--query` projection on `az ad app federated-credential list`, GitHub ID-based subject customisation, and claims about renamed organisations beyond subject contents.
Method: documentation only; no commands were run.
