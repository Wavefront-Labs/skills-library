---
id: computing-software.cloud-infrastructure-engineering.terraform.legacy-provider-address-errors
name: legacy-provider-address-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, legacy-provider-address, replace-provider, state-replace-provider, source-address, terraform-upgrade]
level: practitioner
status: docs-checked
description: "Fix legacy provider addresses (registry.terraform.io/-/name) in 0.12-era state and missing source attributes with required_providers, 0.13upgrade and state replace-provider."
sources: ["https://developer.hashicorp.com/terraform/language/v1.1.x/upgrade-guides/0-13#explicit-provider-source-locations", "https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy provider address errors

## What the legacy address is
Before 0.13, providers had no namespace. Addresses starting `registry.terraform.io/-/`
mark legacy providers whose true namespace is unknown. For providers that were
installable automatically in 0.12, Terraform 0.13 resolves them through a lookup table
in the public registry (the special namespace `-`). In-house providers have no mapping,
so you supply it.

During `init`, Terraform builds the provider list from both configuration and state, so
a 0.12-written state can show lines like `Finding latest version of -/null...` next to
`Finding latest version of hashicorp/null...`. The guide says this is harmless but
confusing.

## Fix 1: explicit sources in configuration
A provider without a `source` is assumed to be in the `hashicorp` namespace; sources are
required for other namespaces. When init cannot find a provider it prints "Could not
find required providers, but found possible alternatives" and suggests
`terraform 0.13upgrade`. That command rewrites the current module only, so run it per
module (and review the diff); it is recommended even without the error.
```hcl
terraform {
  required_providers {
    newrelic = {
      source  = "newrelic/newrelic"
      version = "~> 2.1.1"
    }
  }
}
```
Then run `terraform init` again.

## Fix 2: rewrite state references
```bash
terraform state replace-provider -- -/random registry.terraform.io/hashicorp/random
terraform state replace-provider 'registry.terraform.io/-/happycloud' 'terraform.example.com/awesomecorp/happycloud'
```
- Usage is `terraform state replace-provider [options] FROM_PROVIDER_FQN TO_PROVIDER_FQN`;
  it updates all resources using the "from" provider. Options include `-auto-approve`,
  `-lock=false`, `-lock-timeout`, `-var`/`-var-file`, `-ignore-remote-version` (HCP
  Terraform CLI integration or remote backend) and the legacy `-state`, `-state-out`,
  `-backup` for local state.
- A backup of the state is always written first; it cannot be disabled.
- State is global to the configuration, so run it once per configuration, not per module.
- It writes a new state snapshot that Terraform 0.12 cannot read. Do it only when ready
  to commit to 0.13.
- In-house providers: if the state still has legacy references, init fails with "Failed to
  install legacy providers required by state" and prints the exact command to run.
  Choose a source under a domain you control, such as
  `terraform.example.com/awesomecorp/happycloud`.

## Order of work when upgrading
1. Update provider requirements in every module, run `terraform init`.
2. Run `terraform apply` at least once and accept its changes: Terraform updates provider
   references in state then, using resource blocks to find each resource's provider.
   Do not remove resource blocks before that first apply, or you may get "Provider
   configuration not present"; re-add the resource until the upgrade finishes.
3. For HCP Terraform or Enterprise VCS-driven workspaces, start a run manually after
   selecting a 0.13 release.
4. The same `replace-provider` command also moves resources to a fork or private
   registry, e.g. `terraform state replace-provider hashicorp/aws registry.acme.corp/acme/aws`.

## Checked
Date: 2026-11-07
Read in full: the Terraform v0.13 upgrade guide (language/v1.1.x/upgrade-guides/0-13, including explicit provider source locations, in-house providers and the FAQ on `-/provider`) and terraform state replace-provider (cli/commands/state/replace-provider).
Confirmed: meaning of `registry.terraform.io/-/`; the lookup table; the init messages quoted above; `0.13upgrade` behaviour; replace-provider usage, options, backup rule, once-per-configuration rule, 0.12 incompatibility warning, `--` form for `-/` addresses and the fork example; first-apply state update behaviour.
Removed: the "Failed to query available provider packages ... -/aws does not exist" and "Invalid legacy provider address" errors, "Terraform >= 0.14 cannot install -/ providers", the `state pull | jq` command, the step-through-0.14 upgrade path claim, the `integrations/github` namespace move, and the Verify checklist.
Not opened: Provider Requirements page and the terraform 0.13upgrade command page.
Method: documentation only; no commands were run.
