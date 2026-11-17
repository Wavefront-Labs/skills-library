---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.infrastructure-as-code-practice
name: infrastructure-as-code-practice
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, infrastructure-as-code-practice, infrastructure-as-code, terraform, opentofu, bicep, cloudformation, pulumi, gitops]
level: practitioner
status: draft
description: "Run infrastructure as code as an engineering practice: tool choice, repo and state layout, module versioning, plan review in CI, drift control and no-click production."
sources: ["https://developer.hashicorp.com/terraform/language", "https://learn.microsoft.com/azure/well-architected/operational-excellence/infrastructure-as-code-design", "https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html", "https://opentofu.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infrastructure as code practice

## Steps
1. **Choose the tool per estate**: Terraform/OpenTofu for multi-cloud and SaaS providers;
   Bicep for Azure-only; CloudFormation/CDK for AWS-only with StackSets; Pulumi when teams
   want general-purpose languages. One primary tool per layer avoids ownership fights.
2. **Layer the estate** by change rate and blast radius: organisation/landing zone, shared
   networking, platform services, application stacks. Separate state per layer and per
   environment; small states plan fast and fail small.
3. **Remote state with locking** (S3 + DynamoDB lock or S3 native lockfile, azurerm backend with
   blob lease, GCS backend), encrypted, versioned, access restricted to the pipeline identity.
4. **Modules**: versioned (git tags or a registry), semver, examples and tests
   (`terraform test`, Terratest); pin provider and module versions; renovate bumps.
5. **Pipeline workflow**: PR runs `fmt`, `validate`, linters (tflint), security scans
   (Checkov, Trivy), policy (OPA/Conftest, Sentinel) and posts the `plan`; merge applies the
   exact saved plan with an OIDC-federated role. No human holds standing apply rights to prod.
6. **Drift**: scheduled `plan -detailed-exitcode` (exit 2 = drift) or Azure deployment
   what-if; alert and reconcile. Block console changes in prod with SCPs/Azure Policy except
   break-glass.
7. **Promotion**: same code, different variables per environment; promote the module version,
   not copy-pasted code.
8. **Imports and refactors**: `import` blocks and `moved` blocks rather than manual state surgery.

## Gotchas
- One giant state means every plan touches everything and locks block teams.
- `-target` and manual `state rm` in routine work hide drift; reserve for incidents.
- Secrets in variables end up in state; source them from a secrets manager and protect state.
- `count` on lists reindexes resources on removal; prefer `for_each` with stable keys.

## Verify
- [ ] 100% of prod resources are in code (compare against cloud asset inventory).
- [ ] Every apply traces to a reviewed PR and pipeline run.
- [ ] Nightly drift check is green or has tickets.
