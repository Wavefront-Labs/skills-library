---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-source-addresses-and-state-replace-provider
name: provider-source-addresses-and-state-replace-provider
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, source-address, provider-namespace, replace-provider, state-replace-provider, provider-fork, required-providers]
level: practitioner
status: docs-checked
description: "Read provider source addresses (hostname/namespace/type), local names, and switch state to a fork or private registry host with terraform state replace-provider."
sources: ["https://developer.hashicorp.com/terraform/language/providers/requirements#source-addresses", "https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider", "https://opentofu.org/docs/language/providers/requirements/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider source addresses and `state replace-provider`

## Address anatomy
`[<HOSTNAME>/]<NAMESPACE>/<TYPE>`
- Hostname (optional): the registry that distributes the provider. If omitted it defaults to
  `registry.terraform.io` in Terraform and `registry.opentofu.org` in OpenTofu.
- Namespace: for the public registry and HCP Terraform's private registry, the organisation that
  publishes the provider; may mean something else on other registry hosts.
- Type: short name of the platform; unique within a namespace on a registry host. Usually the
  provider's preferred local name, with exceptions (`hashicorp/google-beta` has preferred local
  name `google`).
- Fully qualified: `registry.terraform.io/hashicorp/http`; the display form omits the public
  registry host (`hashicorp/random`).
- Omitting `source` gives the implied address `registry.terraform.io/hashicorp/<LOCAL NAME>`
  (OpenTofu: `registry.opentofu.org/hashicorp/<LOCAL NAME>`); use explicit sources in
  modules for 0.13 or later.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```
(Version constraint illustrative.)

## Local names versus source addresses
- The source address is used only when requiring the provider; everywhere else the module uses
  the local name, unique per module and chosen when requiring the provider.
- Use the provider's preferred local name so you can omit the `provider` meta-argument; Terraform
  reads the first word of the resource type as the local name.
- If two providers share a type name, use compound local names like `hashicorp-http` and
  `mycorp-http`, and set `provider` on every affected resource.

## In-house hostnames
A source address must include or imply a registry hostname, but for filesystem-distributed
providers the host need not provide a registry service: use a hostname in a domain you control,
for example `terraform.example.com/examplecorp/ourcloud`. Under an implied local mirror directory,
use `terraform.example.com/examplecorp/ourcloud/1.0.0/<platform>/` (such as `linux_amd64`) holding
the provider executable.

## Rewriting state: `terraform state replace-provider`
Usage: `terraform state replace-provider [options] FROM_PROVIDER_FQN TO_PROVIDER_FQN`. It updates
all resources in state that use the "from" provider, setting the provider to the "to" provider, so
you can change the source of a provider that already has resources in state.
```bash
terraform state replace-provider hashicorp/aws registry.acme.corp/acme/aws
```
That is the docs' example: replace `hashicorp/aws` with an acme fork at a private registry
`registry.acme.corp`.
- A backup copy of state is written before changes and cannot be disabled.
- Options: `-auto-approve` skips interactive approval; `-var 'NAME=VALUE'`; `-var-file=FILENAME`;
  `-lock=false` (dangerous if others may run commands against the same workspace);
  `-lock-timeout=0s` (duration to retry a state lock).
- For HCP Terraform CLI integration or remote backend only: `-ignore-remote-version`. For local
  state only: legacy `-state`, `-state-out` and `-backup`.
- Change `source` in `required_providers` to match (the docs example does not show the follow-up
  steps).

## Gotchas
- The backup is mandatory; the page calls the command destructive.
- Run it with the same lock discipline as any state write; do not use `-lock=false` with others active.

## Checked
Date: 2026-11-07. Read in full: Terraform "Provider Requirements" (names and addresses, local names, conflicts, in-house providers), the `terraform state replace-provider` page and the OpenTofu "Provider Requirements" page (hostname default, implied source). Confirmed: address format and parts, default hostnames, display form, implied source, local-name rules, in-house hostname and directory layout, replace-provider usage, example, backup and options. Trims: the version constraint `~> 5.70`, the `tfe.acme.com/acme/vault` and `registry.terraform.io/-/aws` examples with the `-auto-approve` legacy-state command, the "Provider configuration not present" error text, the claims that init installs both providers and about filesystem/network mirrors not changing addresses, the OpenTofu hostname-mapping and no-replace-provider-when-switching claims, the `init -upgrade` follow-up and the Verify steps. The CLI config provider_installation page was not read for this skill.
Method: documentation only; no commands were run.
