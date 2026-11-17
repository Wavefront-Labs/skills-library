---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.open-source-finops-tools
name: open-source-finops-tools
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, open-source-finops-tools, opencost, cloud-custodian, infracost]
level: practitioner
status: docs-checked
description: "Pick open-source FinOps tools by capability: OpenCost for Kubernetes allocation, Cloud Custodian for policy cleanup, Infracost for pre-deploy estimates."
sources: ["https://www.opencost.io/docs/", "https://cloudcustodian.io/docs/", "https://www.infracost.io/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open-source FinOps tooling

Choose per capability, then prototype against one account or cluster before committing.

## Map
| Capability | Tool | What the docs say |
|---|---|---|
| Kubernetes cost allocation | OpenCost | Open source cost measurement and allocation for Kubernetes; needs Prometheus for metrics and storage; allocation API plus a cloud cost API for provider bill data |
| Policy, tagging and waste cleanup | Cloud Custodian | Stateless rules engine; YAML policies of resource type, filters and actions; covers security, tag policy, garbage collection of unused resources and cost management; policies can be validated and dry-run; can bind to serverless event streams for real-time remediation |
| Pre-deploy cost estimates | Infracost | Cost estimates for Terraform, CloudFormation and AWS CDK across AWS, Azure and Google Cloud; comments on pull requests with the cost diff, FinOps policy violations and tagging issues; can also estimate from a Terraform plan JSON |

## Steps
1. Write the capability requirements first, then match a tool to each.
2. Prototype each tool on one cluster or account and check its numbers against the bill.
3. Plan operation: where it runs, how it is upgraded, credentials it needs (OpenCost also needs Prometheus).
4. Record an owner for each tool.

## Gotchas
- OpenCost's allocation API is based on on-demand list pricing, so it does not reflect negotiated discounts unless you
  supply amortised net cost or use the cloud cost data.
- Dry-run Cloud Custodian policies and review the output before enabling destructive actions.

## Verify
- [ ] Each tool's numbers are compared with the bill and the difference is understood.
- [ ] Ownership and upgrade responsibility are written down per tool.

## Checked
Confirmed against the OpenCost docs and specification, the Cloud Custodian documentation home and the Infracost docs home:
tool purposes, Prometheus requirement, list-price basis, policy structure, dry-run and serverless binding, supported IaC
and clouds, PR comments. Removed: Komiser, Goldilocks and the dashboard stack (no sources read), the CNCF status claims,
specific command lines and flags, the "$0 without usage file" claim, `--dryrun`, `mark-for-op`, Prometheus retention
advice, total cost of ownership comparisons, upstream contribution advice, and the finops tools-services and landscape sources.
Method: docs-checked 2026-11-09 against https://www.opencost.io/docs/ , https://cloudcustodian.io/docs/ and https://www.infracost.io/docs/
