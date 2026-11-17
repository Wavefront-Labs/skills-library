---
id: computing-software.cloud-infrastructure-engineering.terraform.importstate-and-resource-identity-in-providers
name: importstate-and-resource-identity-in-providers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, import-state-method, resource-identity, importstate, import-block, passthrough-id, provider-development]
level: practitioner
status: docs-checked
description: "Support terraform import in a Plugin Framework provider: ImportState with passthrough or composite IDs, resource identity (Terraform 1.12+), and import-mode acceptance tests."
sources: ["https://developer.hashicorp.com/terraform/plugin/framework/resources/import", "https://developer.hashicorp.com/terraform/plugin/framework/resources/identity", "https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests/import-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ImportState and resource identity support

`ImportState` must either set enough state for `Read` to refresh the resource, or return
an error. Implement `resource.ResourceWithImportState`.

## Simple ID: passthrough
```go
func (r *ThingResource) ImportState(ctx context.Context, req resource.ImportStateRequest, resp *resource.ImportStateResponse) {
    resource.ImportStatePassthroughID(ctx, path.Root("id"), req, resp)
}
```
This sets the `id` attribute to the value given to `terraform import`. The identifier is
in `req.ID`; state data is written to `resp.State`.

## Multiple attributes
When `Read` needs several attributes, write custom logic: the import command accepts
one identifier string, conventionally with a separator such as a comma. Parse `req.ID`
and set each attribute (the docs example uses `attr_one,attr_two`):
```go
idParts := strings.Split(req.ID, ",")
if len(idParts) != 2 || idParts[0] == "" || idParts[1] == "" {
    resp.Diagnostics.AddError("Unexpected Import Identifier",
        fmt.Sprintf("Expected import identifier with format: attr_one,attr_two. Got: %q", req.ID))
    return
}
resp.Diagnostics.Append(resp.State.SetAttribute(ctx, path.Root("attr_one"), idParts[0])...)
resp.Diagnostics.Append(resp.State.SetAttribute(ctx, path.Root("attr_two"), idParts[1])...)
```

## No import support
Skip `ImportState`. `terraform import` then fails with "Resource Import Not
Implemented ... This resource does not support import."

## Resource identity (Terraform 1.12+)
A provider-determined object stored alongside state that identifies one remote object:
at most one object per provider, resolvable to existing state during import, and constant
over the object's life. Implement `resource.ResourceWithIdentity` and its `IdentitySchema`
method with `identityschema` attributes.
- Identity schemas allow only primitive types and lists of them, and have no
  `Required`/`Computed`. Each attribute sets exactly one of `RequiredForImport` or
  `OptionalForImport`.
- Set identity during Create, Read and Update (`resp.Identity.Set`); Read should return it
  so imports with partial identity data work.
- Users may import by `id` or `identity`, never both. When identity data is present,
  ignore `req.ID` (Core sets it to ""). Still support the ID form when identity data is
  absent; a provider needing only 1.12+ may return an error for IDs.
- For a single identity attribute copied into a single state attribute use
  `resource.ImportStatePassthroughWithIdentity(ctx, path.Root("id"), path.Root("id"), req, resp)`.
- A changed identity raises "Unexpected Identity Change"; set
  `ResourceBehavior{MutableIdentity: true}` in `Metadata` only if the remote identity can
  legitimately change.

## Acceptance tests (import mode)
Import mode creates a resource with Create, imports it, and deep-compares the two; the
step passes only if they match. Test steps in the docs:
- `ImportState: true`, `ResourceName`, `ImportStateVerify: true` for the `terraform import` workflow.
- `ImportStateKind: resource.ImportBlockWithID` for import blocks with an id.
- `ImportStateKind: resource.ImportBlockWithResourceIdentity` for import blocks using identity.

## Checked
Date: 2026-11-07
Read in full: Resource import (plugin/framework/resources/import), Resource Identity (plugin/framework/resources/identity) and Acceptance Tests: Import mode (plugin/testing/acceptance-tests/import-mode).
Confirmed: passthrough and multi-attribute ImportState patterns, the not-implemented error, every identity rule above, passthrough-with-identity helper, mutable identity, and the three test step shapes.
Removed: the "Read must populate every attribute or the next plan diffs" claim, the write-only and `ignore_changes = [password]` advice (1.11 write-only not on these pages), the "framework v1.15+" and "plugin-testing 1.13+" version claims, `ImportStateIdFunc` and `ImportStateVerifyIgnore`, the "list/query features" claim, the resource docs `## Import` section advice and the Verify checklist.
Not opened: the SDKv2 import docs and the testing framework reference for `TestStep` fields.
Method: documentation only; no commands were run.
