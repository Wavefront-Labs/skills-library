---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-development-with-the-plugin-framework
name: provider-development-with-the-plugin-framework
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [resource-crud, framework-schema, terraform, opentofu, terraform-plugin-framework, custom-provider, provider-development, go, golang, grpc, schema, crud, acceptance-testing, tfplugindocs, terraform-plugin-sdk2, provider-versioning, registry-publishing, gpg-signing, state-upgrade, muxing]
level: advanced
status: docs-checked
description: "Build a custom Terraform provider with the Plugin Framework in Go: resource/data-source schema, CRUD against an API, acceptance tests, docs, and registry release."
sources:
  - https://developer.hashicorp.com/terraform/plugin/framework/resources/read
  - https://developer.hashicorp.com/terraform/plugin/framework/resources/import
  - https://developer.hashicorp.com/terraform/plugin/framework/resources/state-upgrade
  - https://developer.hashicorp.com/terraform/plugin/framework/migrating/mux
  - https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests
  - https://developer.hashicorp.com/terraform/plugin/debugging
  - https://developer.hashicorp.com/terraform/registry/providers/publishing
  - https://developer.hashicorp.com/terraform/registry/providers/docs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Terraform provider development with the Plugin Framework

**Goal:** wrap a REST/gRPC API you control (or an unsupported SaaS) in a Terraform
provider whose resources behave correctly under plan/apply/destroy/import, with
acceptance tests proving it against the real API and a releasable registry artifact.

## 1. Scaffold
Use `terraform-plugin-framework`; start from HashiCorp's
`terraform-provider-scaffolding-framework` template repository. To try a local build without
`terraform init`, use a CLI configuration file (`.terraformrc` in your user directory, or the
file named by `TF_CLI_CONFIG_FILE`) with a `provider_installation` block containing `dev_overrides`:
```hcl
provider_installation {
  dev_overrides { "example.com/me/widget" = "<GOPATH>/bin" }
  direct {}
}
```

## 2. Schema and model
Define the resource schema with `schema.Schema{ Attributes: map[string]schema.Attribute{...} }`
using typed attributes. Mark server-assigned fields `Computed: true` and user-supplied
fields `Required: true`. Model the Go struct with `tfsdk:"field_name"` tags matching the
schema. `stringplanmodifier.UseStateForUnknown()` copies the prior state value (if not null)
and reduces `(known after apply)` noise for computed attributes that do not change.

## 3. CRUD and the request lifecycle
Implement `Create`, `Read`, `Update`, `Delete` on the resource type. Read prior state from
`req`, write results to `resp.State`, and add errors to `resp.Diagnostics`, returning early
on error. `Read` also runs during `plan`/`apply`/`refresh` and after import. If the remote
object is gone (for example HTTP 404), call `resp.State.RemoveResource(ctx)` and return; the
next plan recreates it. The framework errors if `Read` leaves unknown values in state, and any
error keeps the prior state. Implement `ImportState` (usually `resource.ImportStatePassthroughID`)
so `terraform import` works.

## 4. State upgrades
Implement `UpgradeState` returning `map[int64]resource.StateUpgrader`, keyed by prior schema
version, optionally with a `PriorSchema` to read the old state, when a schema change
would otherwise break existing state.

## 5. Acceptance tests
`terraform-plugin-testing` runs real Terraform operations against a live backend. The
`TF_ACC` environment variable (any value) must be set or acceptance tests are skipped.
Use `ConfigStateChecks` for state assertions. To assert no plan differences after a
change, use `ConfigPlanChecks` with `plancheck.ExpectEmptyPlan()`; the testing guide
recommends this over `PlanOnly` for steps that change provider setup.

## 6. Docs, versioning, release
`tfplugindocs` generates registry-format docs from resource and data source
descriptions and schema; the scaffolding repository runs it via a `go:generate` line.
For registry publishing the release needs a GPG-signed checksums file, and
`terraform-registry-manifest.json` at the repository root, which is renamed to
`terraform-provider-{NAME}_{VERSION}_manifest.json` in the release assets. GoReleaser,
configured from the scaffolding repository's `.goreleaser.yml`, builds, checksums and signs;
it cannot sign with a GPG key that needs a passphrase.

## Gotchas
- Muxing (`tf5muxserver` / `tf6muxserver`) is documented for serving a framework provider
  alongside an SDKv2 one during migration.
- Leaving unknown values in `Read`'s state is an error; set attributes to null or known values.

## Verify
- [ ] `terraform plan` after `apply` shows no changes (empty plan check passes).
- [ ] Deleting the resource out-of-band then `plan` shows a clean create, not an error.
- [ ] `terraform import` on a real remote object succeeds and matches config.
- [ ] Docs generated by `tfplugindocs` are current.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the web-unified-docs sources of the Plugin Framework (read, import, state-upgrade, mux), Plugin Testing (acceptance tests, migrating), and the registry publishing, docs and plugin debugging pages. Removed as not confirmed: "mismatched tfsdk tags panic at runtime", the Optional+Computed advice, the claim that `Read` loops forever on 404 and that `state rm` is needed, `stringvalidator`/`int64validator` examples, `PlanOnly` as the idempotency check, `statecheck.ExpectKnownValue`, "CI fails if docs drift", the semver tagging rule, the filesystem/network mirror for private providers, the `.sig` file name, and the SDKv2 muxing complexity warning. The original source list (page names only) was replaced with URLs.
