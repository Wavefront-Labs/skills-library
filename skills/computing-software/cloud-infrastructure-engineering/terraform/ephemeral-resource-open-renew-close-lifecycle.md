---
id: computing-software.cloud-infrastructure-engineering.terraform.ephemeral-resource-open-renew-close-lifecycle
name: ephemeral-resource-open-renew-close-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ephemeral-lifecycle, ephemeral-resource, ephemeral-values, plugin-framework]
level: practitioner
status: docs-checked
description: "Understand the ephemeral resource lifecycle: open during plan and apply, renew for long operations, close at the end, what is persisted, and implementing it in a provider."
sources: ["https://developer.hashicorp.com/terraform/language/resources/ephemeral", "https://developer.hashicorp.com/terraform/plugin/framework/ephemeral-resources", "https://developer.hashicorp.com/terraform/language/block/ephemeral", "https://developer.hashicorp.com/terraform/plugin/framework/ephemeral-resources/open", "https://developer.hashicorp.com/terraform/plugin/framework/ephemeral-resources/renew", "https://developer.hashicorp.com/terraform/plugin/framework/ephemeral-resources/close"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral resource lifecycle

```hcl
ephemeral "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
}
```
Terraform does not store ephemeral resources in state or plan files. They are supported
in Terraform 1.10 and later.

## Phases
| Phase | When | Provider method |
|---|---|---|
| **Open** | during any operation (such as `terraform plan` or `terraform apply`) when the resource's data is needed | `Open` (required) |
| **Renew** | the provider set a `RenewAt` time in the Open (or a previous Renew) response, the data is still in use and that time has passed | `Renew` (optional) |
| **Close** | once the data is no longer needed: after the providers that depend on the resource finish their work for the current run phase | `Close` (optional) |

Example with Vault: open obtains a lease and returns the secret; renew calls Vault's
lease renewal endpoint; close ends the lease so Vault revokes the credentials.

## Consequences
- You can only refer to an ephemeral resource in ephemeral contexts, otherwise Terraform
  errors at plan: a managed resource's write-only argument, another `ephemeral` block,
  `locals`, a `variable` with `ephemeral = true`, a child module `output` with
  `ephemeral = true`, a `provider` block, and provisioner and connection
  configuration.
- A resource or data source that depends on an ephemeral attribute makes Terraform
  provision the ephemeral resource first.
- If an input argument of an ephemeral resource references a value Terraform does not
  know yet but can learn during or after a plan, Terraform defers it to the apply
  stage.
- `ephemeral` blocks support `count`, `depends_on`, `for_each`, `provider` and
  `lifecycle` (`precondition`/`postcondition`); `count` and `for_each` are mutually
  exclusive.

## Implementing (Plugin Framework)
Implement `ephemeral.EphemeralResource` (`Metadata`, `Schema`, `Open`) and register it
through `provider.ProviderWithEphemeralResources`. `Renew` and `Close` come from the
optional `ephemeral.EphemeralResourceWithRenew` and `EphemeralResourceWithClose`
interfaces.
```go
func (e *ThingEphemeralResource) Open(ctx context.Context, req ephemeral.OpenRequest, resp *ephemeral.OpenResponse) {
    var data ThingEphemeralResourceModel
    resp.Diagnostics.Append(req.Config.Get(ctx, &data)...)
    if resp.Diagnostics.HasError() {
        return
    }

    data.Token = types.StringValue("token-123") // normally an external call

    resp.RenewAt = time.Now().Add(5 * time.Minute)   // when to call Renew
    privateData, _ := json.Marshal(ThingPrivateData{Name: data.Name.ValueString()})
    resp.Private.SetKey(ctx, "thing_data", privateData) // passed to Renew and Close

    resp.Diagnostics.Append(resp.Result.Set(ctx, &data)...)
}
```
- Open caveats: an error is returned if the `Result` contains unknown values, and an
  error is returned unless every non-computed known config value is saved as-is into the
  result (only null computed values can be modified).
- `Renew` cannot return new result data, so it suits remote objects such as Vault leases
  that can be renewed without changing their data. It receives the `Private` data from
  the latest Open or Renew and may set a new `RenewAt` and `Private`.
- Set `RenewAt` a little before the real expiry (usually no more than a few minutes)
  to allow for latency.
- `Close` receives the `Private` data from the latest Open or Renew call, for cleanup.

## Checked
Date: 2026-11-07
Read in full: Ephemeral values in resources (language/resources/ephemeral, redirects to manage-sensitive-data), ephemeral block reference (language/block/ephemeral), Plugin Framework Ephemeral resources overview, and its Open, Renew and Close pages including their example code.
Confirmed: Terraform 1.10+; never stored in state or plan files; lifecycle wording for open, renew, close; Vault lease example; ephemeral contexts list; dependency ordering; deferral to apply; supported meta-arguments; Open required, Renew/Close optional; RenewAt, Private, Result and Config handling; Open caveats; Renew cannot return new data; latency recommendation.
Removed: the sample plan output (`Opening...` / `Opening complete`), "Close always runs, even on error", the "no diff / no will be created line" claim, the invented `client.IssueToken` Go example (replaced with the page's shape), the `lease_id` private-key example, the claim that locals/outputs generally need marking, and the TF_LOG and `terraform state pull` Verify steps (none on the pages). Added the two sources for the block reference and the Open/Renew/Close pages.
Not opened: the Plugin Framework "configure" and "validate" ephemeral pages.
Method: documentation only; no commands were run.
