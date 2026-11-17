---
id: computing-software.cloud-infrastructure-engineering.terraform.plugin-framework-plan-modifiers-and-state-upgraders
name: plugin-framework-plan-modifiers-and-state-upgraders
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, provider-development, plugin-framework, plan-modifiers, requires-replace, use-state-for-unknown, state-upgrader, schema-version, go]
level: sme
status: docs-checked
description: "Evolve a Plugin Framework resource safely: plan modifiers (RequiresReplace, UseStateForUnknown, ModifyPlan), schema Version bumps and UpgradeState functions for old state."
sources: ["https://developer.hashicorp.com/terraform/plugin/framework/resources/plan-modification", "https://developer.hashicorp.com/terraform/plugin/framework/resources/state-upgrade"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plan modifiers and state upgraders (Plugin Framework)

## Plan modifiers
Add attribute plan modifiers through the attribute's `PlanModifiers` field; the framework ships common ones in typed packages such as `resource/schema/stringplanmodifier`.
```go
"name": schema.StringAttribute{
    Required: true,
    PlanModifiers: []planmodifier.String{
        stringplanmodifier.RequiresReplace(),          // in-place update not possible: replace
    },
},
"id": schema.StringAttribute{
    Computed: true,
    PlanModifiers: []planmodifier.String{
        stringplanmodifier.UseStateForUnknown(),       // copy prior state: fewer "(known after apply)" lines
    },
},
```
- `RequiresReplace()`: a changed value means replace instead of update.
- `RequiresReplaceIf()`: like `RequiresReplace()` with provider-defined conditional logic. `RequiresReplaceIfConfigured()`: only triggers when the practitioner configured a value. The page defers their behaviour to the Go documentation, so check the Go docs for their signatures.
- `UseStateForUnknown()` copies the prior state value if it is not null. Use it for computed attributes known not to change over time.
- Order of the process: null-config attributes get their default, the framework marks computed attributes that are null in config as unknown when the plan differs from state, then attribute plan modifiers run, then resource plan modifiers.
- A plan modifier that returns an error stops further modifiers on that attribute and its nested attributes.
- Resource-level logic: implement `resource.ResourceWithModifyPlan` (`ModifyPlan`). Plan modifiers run on create, update and destroy: a null `req.State.Raw` means create, a null `req.Plan.Raw` means destroy. For a destroy plan (Terraform 1.3 and later supports diagnostics there) keep the response plan entirely null.
- After `Update`, every attribute state value must match its planned value or Terraform raises a `Provider produced inconsistent result` error; if the full value is not known at plan time, mark it unknown in the plan. Terraform's data consistency rules also apply: a configured value may not change in the plan (except being set null on destroy).
- Attribute plan modifiers under list or set nested attributes/blocks that read prior state get index-based prior state; elements are not re-aligned if rearranged or removed.

## Schema versions and state upgraders
When the stored shape changes (for example an attribute type), raise the schema `Version` to greater than 0 and implement `resource.ResourceWithUpgradeState`:
```go
func (r *thingResource) Schema(_ context.Context, _ resource.SchemaRequest, resp *resource.SchemaResponse) {
    resp.Schema = schema.Schema{Version: 1, Attributes: /* new schema */}
}

func (r *thingResource) UpgradeState(ctx context.Context) map[int64]resource.StateUpgrader {
    return map[int64]resource.StateUpgrader{
        0: {
            PriorSchema: &priorSchemaV0,          // lets you read old state into a typed model
            StateUpgrader: func(ctx context.Context, req resource.UpgradeStateRequest, resp *resource.UpgradeStateResponse) {
                var old thingModelV0
                resp.Diagnostics.Append(req.State.Get(ctx, &old)...)
                if resp.Diagnostics.HasError() { return }
                upgraded := thingModelV1{ID: old.ID, DisplayName: old.Name /* renamed */}
                resp.Diagnostics.Append(resp.State.Set(ctx, upgraded)...)
            },
        },
    }
}
```
- Terraform saves the schema version in state; when the provider advertises a newer version it calls back for an upgrade before planning.
- Each map key is a prior version; its upgrader must wholly upgrade state from that version to the current one. The framework does not run intermediate versions; incrementing by 1 is only a convention.
- The response must be fully populated: the framework copies nothing from the request.
- With no upgrade support, or none for the requested prior version, the framework returns an error diagnostic.
- `PriorSchema` is the recommended approach; without it, read `req.RawState` and write `resp.State` or `resp.DynamicValue` (advanced).
- Caveats: unknown values in the response state are an error (use null or known values); any response error makes Terraform keep the prior state.

## Checked
Date: 2026-11-07. Read in full: the Plan modification page (process order, common modifiers, caveats, resource-level ModifyPlan and the destroy section) and the State upgrade page (process, ResourceWithUpgradeState, PriorSchema and RawState examples, caveats). Trimmed: the `RequiresReplaceIf` example closure and its description arguments (the page only says to see the Go docs), "Migrating from SDKv2 with the same schema needs no version bump", "never reuse numbers" (the page says only that +1 is conventional), the normalise-in-Read advice, the `ExternalProviders` upgrade-test recipe and the Verify checklist, none of which these pages state.
Method: documentation only; no commands were run.
