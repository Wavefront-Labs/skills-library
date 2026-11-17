---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.policy-as-code-with-opa-or-sentinel
name: policy-as-code-with-opa-or-sentinel
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, policy-as-code, opa, open-policy-agent, rego, conftest, sentinel, hcp-terraform, terraform-cloud, terraform-enterprise, enforcement-levels, advisory, soft-mandatory, hard-mandatory, opa-test, policy-testing, policy-bundles, gatekeeper, kyverno, azure-policy, service-control-policies, scp, organization-policy, guardrails, compliance-as-code, waivers, exceptions]
level: advanced
status: gated
description: "Build a policy-as-code program: choose OPA/Rego or Sentinel, layer it with cloud-native guardrails, unit-test policies, version and distribute them, and run an expiring waiver process."
sources: ["Open Policy Agent documentation - Policy language and testing", "HashiCorp Sentinel documentation - Enforcement levels and testing", "Conftest documentation", "HashiCorp Terraform documentation - Policy enforcement in HCP Terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy as code with OPA or Sentinel — guardrails people can read, test and trust

**Goal:** organisational rules (encryption, regions, tagging, network exposure, sizes) are
expressed as versioned, tested code, enforced at the right layer, with a clear way to get
an exception that expires.

The basic "run Conftest on plan.json in CI" step is covered in
`computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion`.
This skill is about running policy as a **programme**.

## 1. Pick the engine
| | OPA / Rego (+ Conftest) | Sentinel |
|---|---|---|
| Licence / where | open source; CI, Kubernetes (Gatekeeper), APIs, HCP Terraform also accepts OPA | HashiCorp commercial (HCP Terraform/TFE, Vault, Consul, Nomad) |
| Input | any JSON/YAML (plan JSON, K8s manifests, Dockerfiles) | Terraform plan/config/state imports (`tfplan/v2`, `tfconfig/v2`, `tfstate/v2`) |
| Enforcement | pass/fail; you build levels in CI (in HCP Terraform, OPA policy sets offer `advisory` and `mandatory`) | built-in `advisory`, `soft-mandatory` (overridable), `hard-mandatory` |
| Reuse | one language across infra, K8s admission, app authz | Terraform-centric |

Rule of thumb: already on HCP Terraform/TFE and Terraform-only → Sentinel is cheapest to adopt.
Multiple IaC tools or Kubernetes in scope → OPA, so one language covers all.
Kyverno is a YAML-native alternative for Kubernetes-only admission.

## 2. Layer the guardrails
1. **Cloud-native preventive** (cannot be bypassed by skipping CI): AWS SCPs/RCPs, Azure Policy `deny`, GCP Organization Policy constraints. Use for the few absolute rules — allowed regions, no public buckets org-wide, no disabling audit logs.
2. **Plan-time** (OPA/Sentinel): richer context-aware rules, fast feedback in the PR.
3. **Admission** (Gatekeeper/Kyverno) for cluster objects created outside Terraform.
4. **Detective** (AWS Config, Azure Policy audit, Security Command Center) for drift and click-ops.
Plan-time policy alone is advisory in practice — anyone with console access bypasses it.

## 3. Write policies people can act on
```rego
package terraform.tags
import rego.v1
required := {"owner", "cost-centre", "environment"}
deny contains msg if {
  some rc in input.resource_changes
  rc.change.actions[_] in {"create", "update"}
  tags := object.get(rc.change.after, "tags", {})
  missing := required - {k | some k, _ in tags}
  count(missing) > 0
  msg := sprintf("%s missing tags %v (see wiki/tagging)", [rc.address, missing])
}
```
- Message names the resource, the rule, and where to read the fix.
- Ignore `delete`/`no-op` changes, or you block cleanups.
- Beware `tags_all` vs `tags` (provider default tags) — check the field that actually lands.

## 4. Test the policies
- OPA: `*_test.rego` files with `test_` rules and fixture inputs; `opa test policy/ -v`; aim for a pass and a fail fixture per rule. Capture fixtures from real `terraform show -json` output.
- Sentinel: `sentinel test` with `test/<policy>/pass.hcl` / `fail.hcl` (folder named after the policy file minus extension; each HCL file is one test case; `mock "tfplan/v2"` data) and mock data generated from a real run in HCP Terraform. (Sentinel CLI not run here: gated: unconfirmed, layout taken from HashiCorp's Sentinel testing docs.)
- Run policy tests in the policy repo's own CI before releasing a new version.

## 5. Distribute and version
Policy repo → tagged releases → OPA bundles (or Conftest `--update` from an OCI registry), or
Sentinel policy sets attached to workspaces by tag/project. Roll out new rules as **advisory
first** for 2-4 weeks, publish the violation count, then promote to mandatory.

## 6. Exceptions
Waivers in code (allow-list file keyed by resource address + rule ID) with an owner, reason,
ticket and **expiry date**; a policy fails when the waiver expires. Report waiver counts monthly.

## Gotchas
- Unknown-after-apply values appear as absent from `change.after` in plan JSON and are flagged in `change.after_unknown` (checked with `terraform_data`: `id` and `output` absent from `after`, `true` in `after_unknown`) — a rule can pass on plan and be violated after apply; back it with detective controls.
- Module-wrapped resources have addresses like `module.x.aws_s3_bucket.this`; match on `type`, not address.
- Soft-mandatory overrides without audit become the norm; review who overrides.
- Rego v1 syntax (`if`, `contains`) is the default in OPA 1.0+; older examples omit it. The tag rule above was run with Conftest 0.71.1 (OPA 1.21.1): it denied a create missing two tags and an update missing all three, and skipped a delete.

## Verify
- [ ] Each rule has an ID, owner, severity and pass/fail tests.
- [ ] Absolute rules also exist as SCP/Azure Policy/Org Policy, not only in CI.
- [ ] New rules shipped advisory first with violation counts reviewed.
- [ ] Waivers carry expiry dates and fail when expired.
- [ ] Policy violations show actionable messages in the PR.

Uncertain: HCP Terraform OPA support and Sentinel import names change between releases — check current docs.
