---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-tool-landscape-and-limits-of-stateless-provisioning
name: iac-tool-landscape-and-limits-of-stateless-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, config-vs-provisioning, tool-landscape, stateless-provisioning, tool-selection]
level: practitioner
status: docs-checked
description: "Compare Terraform, Pulumi and Ansible: declarative stateful versus idempotent stateless models, drift handling, and where each tool fits in a combined workflow."
sources: ["https://www.redhat.com/en/topics/automation/ansible-vs-terraform", "https://www.pulumi.com/docs/iac/concepts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IaC tool landscape and stateless provisioning limits

## Models (from Red Hat's Ansible vs Terraform page and Pulumi's concepts page)
| Tool | Model | State |
|---|---|---|
| Terraform | Declarative HCL: you define the desired end state and the engine works out the steps and manages dependencies | Stateful: a state file is the source of truth for every resource it provisions, which lets it manage full lifecycle including retiring resources |
| Pulumi | Programs in general-purpose languages (TypeScript, JavaScript, Python, Go, .NET, Java) and YAML declare resource objects; a deployment engine computes the operations to move current state to desired state | State stored in a backend; optional Pulumi Cloud adds access control, secrets, policy enforcement and drift detection |
| Ansible | A multipurpose automation engine for configuring systems, deploying software and orchestrating tasks across servers, network devices and security tools; procedural tasks relying on idempotency | Largely stateless: no persistent state file; it queries the target system before changing it |

Pulumi tracks dependencies between resources (for example a server using a security group's ID output) and uses them to maximise parallelism while preserving correct ordering.

## Drift
- Terraform compares running infrastructure against its state file to flag discrepancies.
- Ansible typically limits drift by running continuously and relying on idempotent tasks to re-enforce desired configuration.
Implication (inference from the stateless model): an Ansible run only corrects what its tasks touch, and a resource removed from a playbook is not retired automatically because there is no state record of it. Treat resource retirement and drift reporting as explicit work when using Ansible for provisioning.

## Overlap and combination
Red Hat notes the tools overlap: Ansible can provision and Terraform can run basic configuration scripts. Its recommendation is to use both rather than pick one: Terraform for building infrastructure, Ansible for ongoing deployment and configuration. Ansible Automation Platform can orchestrate Terraform inside a wider workflow (pre-provisioning tasks, a Terraform deployment, post-provisioning configuration, ITSM integration), and a certified Terraform collection for Ansible exists.

## Gotchas
- Using two tools on the same resource guarantees drift fights. Pick one owner per resource type and document the boundary. (Practitioner guidance.)

## Verify
- [ ] Every resource type in the estate has exactly one owning tool recorded.

## Checked
Method: docs-checked 2026-11-09 against the Red Hat "Ansible vs. Terraform" page and the Pulumi IaC concepts page.
Removed as unconfirmed: the CloudFormation/CDK/Bicep and Crossplane rows (Crossplane page returned 404; cloud-native sources not read), specific claims that Ansible cloud modules have partial `--check` support, name/tag identity problems, and the "when Ansible provisioning is fine" list. Description and tags adjusted.
