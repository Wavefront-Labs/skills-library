---
id: computing-software.cloud-infrastructure-engineering.terraform.legacy-provider-blocks-in-modules-and-orphaned-providers
name: legacy-provider-blocks-in-modules-and-orphaned-providers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, legacy-provider-in-module, module-provider-block-error, orphaned-provider, provider-configuration-not-present, module-removal]
level: advanced
status: docs-checked
description: "Fix legacy modules that embed provider blocks (not compatible with count, for_each, depends_on) and avoid orphaned providers when removing a module or provider configuration."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/providers#legacy-shared-modules-with-provider-configurations", "https://developer.hashicorp.com/terraform/language/modules/develop/providers#provider-version-constraints-in-modules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider blocks inside modules; orphaned providers

## The rule
Provider configurations are global to a whole Terraform configuration and can be
defined only in the root module. A module meant to be called by other modules must not
contain any `provider` blocks. A module with its own provider configurations (a
"legacy" shared module) cannot use `for_each`, `count` or `depends_on`, which arrived in
Terraform v0.13; the legacy pattern still works for module calls that do not use them.

Combining them gives an error such as:
```
Error: Module does not support count
Module "child" cannot be used with count because it contains a nested provider
configuration for "aws", at child/main.tf:2,10-15.
```

## Why removing such a module is a problem
Providers are used for every operation on their resources, including destroy and refresh,
so a provider configuration must stay in the configuration longer than every resource it
manages. Terraform keeps in state a reference to the provider configuration last used
for each resource, and uses it when the resource block is removed. If a module holds
both resources and their provider block, removing the module removes both at once.
In general, destroy every resource belonging to a provider configuration before removing
that provider block; if Terraform finds state for a resource whose provider
configuration is gone, planning returns an error asking you to reintroduce it.

## Refactor to the supported pattern
1. Remove every `provider` block from the module.
2. Keep the module's own requirements: each module declares `required_providers` (source
   and version), since only configurations, not requirements, are inherited. In a shared
   module constrain only the minimum with `>=`.
   If the module needs additional configurations declare
   `configuration_aliases = [ aws.src, aws.dst ]`.
3. Define provider blocks in the root. The default configuration is inherited
   automatically; aliased configurations are never inherited and must be passed through
   the module block's `providers` map (`providers = { aws = aws.east }`, keys are the
   child's names, values the caller's).
4. If instances need different provider configurations, use one module block per
   configuration set; `count`/`for_each` instances cannot receive different providers,
   because the resource-to-provider association is static.

## Checked
Date: 2026-11-07
Read in full: Providers Within Modules (language/modules/develop/providers), including provider version constraints, aliases, inheritance, explicit passing and the legacy shared modules section with all examples.
Confirmed: root-only configuration rule; legacy module incompatibility and the example error; v0.10/v0.11/v0.13 history; reason removal causes orphans; state retains provider reference; error on missing provider configuration; requirements-not-inherited note; `configuration_aliases`; providers map semantics; one module block per provider set.
Removed: the exact "Module is incompatible with count, for_each, and depends_on" text and the exact "Provider configuration not present" orphan text (that text is on the 0.13 upgrade guide, not this page), `terraform destroy -target`, `removed` blocks, `terraform state rm` recovery, the "ignores the caller's assume_role" claim, the aliased-provider-in-root gotcha as a separate item (covered by the destroy-first rule), and the Verify checklist with grep.
Not opened: Provider Requirements and the removed block reference.
Method: documentation only; no commands were run.
