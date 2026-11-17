---
id: computing-software.cloud-infrastructure-engineering.terraform.plugin-framework-attribute-validators
name: plugin-framework-attribute-validators
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, attribute-validators, terraform-plugin-framework-validators, config-validators, provider-development, validate-config, stringvalidator]
level: practitioner
status: docs-checked
description: "Validate provider configuration early with Plugin Framework attribute validators: stringvalidator, conflicts, ConfigValidators, custom validators, unknowns."
sources:
  - https://developer.hashicorp.com/terraform/plugin/framework/validation
  - https://pkg.go.dev/github.com/hashicorp/terraform-plugin-framework-validators
  - https://developer.hashicorp.com/terraform/plugin/framework/resources/validate-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attribute validators

Validators run during `terraform validate`, `plan`, `apply` and `destroy` (Terraform calls the provider's `Validate<Type>Config` RPCs), after the CLI's own syntax and schema checks, so users get errors before any API call - with the attribute path highlighted.

## Built-in helpers (terraform-plugin-framework-validators)
```go
import (
    "github.com/hashicorp/terraform-plugin-framework-validators/stringvalidator"
    "github.com/hashicorp/terraform-plugin-framework-validators/int64validator"
    "github.com/hashicorp/terraform-plugin-framework-validators/listvalidator"
)

"name": schema.StringAttribute{
    Required: true,
    Validators: []validator.String{
        stringvalidator.LengthBetween(3, 63),
        stringvalidator.RegexMatches(regexp.MustCompile(`^[a-z][a-z0-9-]*$`), "must be lowercase letters, digits and hyphens"),
    },
},
"tier": schema.StringAttribute{
    Optional: true,
    Validators: []validator.String{stringvalidator.OneOf("free", "pro", "enterprise")},
},
"port": schema.Int64Attribute{
    Optional: true,
    Validators: []validator.Int64{int64validator.Between(1, 65535)},
},
"cidrs": schema.ListAttribute{
    ElementType: types.StringType, Optional: true,
    Validators: []validator.List{listvalidator.SizeAtMost(10), listvalidator.UniqueValues(),
        listvalidator.ValueStringsAre(stringvalidator.LengthAtLeast(9))},
},
```
Cross-attribute rules on an attribute:
```go
"password": schema.StringAttribute{Optional: true, Sensitive: true,
    Validators: []validator.String{stringvalidator.ConflictsWith(path.MatchRoot("password_wo"))}},
"kms_key_id": schema.StringAttribute{Optional: true,
    Validators: []validator.String{stringvalidator.AlsoRequires(path.MatchRoot("encrypted"))}},
```
Also: `ExactlyOneOf`, `AtLeastOneOf`.

## Resource-level ConfigValidators
```go
func (r *dbResource) ConfigValidators(ctx context.Context) []resource.ConfigValidator {
    return []resource.ConfigValidator{
        resourcevalidator.ExactlyOneOf(path.MatchRoot("snapshot_id"), path.MatchRoot("engine_version")),
    }
}
```
The `resourcevalidator` package also has `Conflicting`, `AtLeastOneOf` and `RequiredTogether`. For logic that doesn't fit, implement `ValidateConfig(ctx, req, resp)` (`resource.ResourceWithValidateConfig`) on the resource.

## Custom validator
```go
type rfc3339Validator struct{}
func (v rfc3339Validator) Description(_ context.Context) string { return "must be an RFC 3339 timestamp" }
func (v rfc3339Validator) MarkdownDescription(ctx context.Context) string { return v.Description(ctx) }
func (v rfc3339Validator) ValidateString(ctx context.Context, req validator.StringRequest, resp *validator.StringResponse) {
    if req.ConfigValue.IsNull() || req.ConfigValue.IsUnknown() { return }   // unknown until apply: skip
    if _, err := time.Parse(time.RFC3339, req.ConfigValue.ValueString()); err != nil {
        resp.Diagnostics.AddAttributeError(req.AttributePath, "Invalid timestamp", v.Description(ctx)+": "+err.Error())
    }
}
```
Always skip null and unknown values: the docs say configuration values may be unknown and implementations should return early without new diagnostics, otherwise valid configs that reference other resources break.

All validators in the `Validators` slice always run, even after an earlier one errors. Validators needing other attributes should take `path.Expression`s (absolute or relative) and use `MergeExpressions`, `PathMatches` and `GetAttribute`. For rules on one custom value type reused across attributes, prefer value validation (`xattr.ValidateableAttribute`) over the deprecated `xattr.TypeWithValidate`. Function parameters accept the same helpers via `Validators: []function.StringParameterValidator{...}`.

## Validators vs plan modifiers vs API errors
- Validators: static rules on config. Config validation runs offline, before provider `Configure`, so no API client is available.
- Plan modifiers: use these when validation needs a configured API client (the docs point to plan modification for that).
- API errors: anything that depends on remote state (name already taken) - surface clearly in Create.

## Verify
- [ ] `terraform validate` reports invalid values with the attribute path; unknown values from other resources pass.
- [ ] Unit tests call validators directly with null/unknown/invalid/valid inputs.

## Checked
2026-11-08. Confirmed on the three cited pages: `Validators` field, `validator.String` interface methods (`Description`, `MarkdownDescription`, `ValidateString` with `req.ConfigValue` and `req.AttributePath`), `LengthBetween`, `RegexMatches`, `resourcevalidator.Conflicting`, `ConfigValidators`, `ValidateConfig`, unknown-value handling and the offline-validation note. Names `OneOf`, `LengthAtLeast`, `Between`, `SizeAtMost`, `UniqueValues`, `ValueStringsAre`, `ConflictsWith`, `AlsoRequires`, `ExactlyOneOf`, `AtLeastOneOf` and the `resourcevalidator` functions confirmed on the pkg.go.dev package pages of stringvalidator, int64validator, listvalidator and resourcevalidator. Fixed `req.Path` to `req.AttributePath`. Removed the named plan modifiers (`RequiresReplace`, `UseStateForUnknown`), which these pages do not cover.
Method: documentation only; no commands were run.
