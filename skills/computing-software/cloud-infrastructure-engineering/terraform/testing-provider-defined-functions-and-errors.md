---
id: computing-software.cloud-infrastructure-engineering.terraform.testing-provider-defined-functions-and-errors
name: testing-provider-defined-functions-and-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, function-tests, function-error, provider-functions, plugin-framework, acceptance-tests]
level: practitioner
status: docs-checked
description: "Test provider-defined functions with unit tests and terraform-plugin-testing, and return precise argument errors with function.NewArgumentFuncError and parameter validators."
sources: ["https://developer.hashicorp.com/terraform/plugin/framework/functions/testing", "https://developer.hashicorp.com/terraform/plugin/framework/functions/errors", "https://developer.hashicorp.com/terraform/plugin/framework/functions/parameters", "https://developer.hashicorp.com/terraform/plugin/framework/validation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing provider functions and errors

## Returning errors
```go
func (f *ParseRFC3339Function) Run(ctx context.Context, req function.RunRequest, resp *function.RunResponse) {
    var ts string
    resp.Error = function.ConcatFuncErrors(resp.Error, req.Arguments.Get(ctx, &ts))
    if resp.Error != nil {
        return
    }
    t, err := time.Parse(time.RFC3339, ts)
    if err != nil {
        resp.Error = function.NewArgumentFuncError(0, fmt.Sprintf("invalid RFC3339 timestamp %q: %s", ts, err))
        return
    }
    resp.Error = function.ConcatFuncErrors(resp.Error, resp.Result.Set(ctx, t.Unix()))
}
```
`NewArgumentFuncError(index, msg)` takes the zero-based argument position and shows the
user the line and value; `function.NewFuncError(msg)` is for failures not tied to one
argument. Always concatenate with `ConcatFuncErrors` rather than replacing
`resp.Error`; it ignores nil errors. `FuncErrorFromDiags(ctx, diags)` converts
error-level diagnostics (warnings are logged, not included). Terraform prints
argument errors as `Error: Invalid function argument` followed by
`Invalid value for "<param>" parameter: ...`, and other errors as
`Error: Error in function call`.

Parameter-level validation: every parameter needs a `Name`. Use
`Validators: []function.StringParameterValidator{...}` on `function.StringParameter`
(validators implement `ValidateParameterString` and set `resp.Error` using
`req.ArgumentPosition`), or a custom value type that implements
`function.ValidateableParameter` (`ValidateParameter(ctx, req, resp)`, using
`req.Position`). All validators in the slice always run.
`AllowNullValue` and `AllowUnknownValues` are parameter settings; test null and
unknown inputs for any parameter that enables them.

## Unit tests (no Terraform)
```go
func TestParseRFC3339_Run(t *testing.T) {
    resp := function.RunResponse{Result: function.NewResultData(types.Int64Unknown())}
    req := function.RunRequest{Arguments: function.NewArgumentsData([]attr.Value{types.StringValue("nope")})}
    NewParseRFC3339Function().Run(context.Background(), req, &resp)
    if resp.Error == nil { t.Fatal("expected error") }
}
```

## Acceptance tests (real Terraform, TF 1.8+)
```go
resource.UnitTest(t, resource.TestCase{
    TerraformVersionChecks: []tfversion.TerraformVersionCheck{tfversion.SkipBelow(tfversion.Version1_8_0)},
    ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
    Steps: []resource.TestStep{
        {
            Config: `output "t" { value = provider::corp::parse_rfc3339("2026-10-18T00:00:00Z") }`,
            ConfigStateChecks: []statecheck.StateCheck{
                statecheck.ExpectKnownOutputValue("t", knownvalue.Int64Exact(1792281600)),
            },
        },
        {
            Config:      `output "t" { value = provider::corp::parse_rfc3339("nope") }`,
            ExpectError: regexp.MustCompile(`invalid RFC3339 timestamp`),
        },
    },
})
```
With `TestStep.Config` the framework injects the `required_providers` entry; with
`ConfigFile` or `ConfigDirectory` you must add it yourself. The docs prefer acceptance
tests, and keep unit tests for functions that need broad input coverage or fuzzing.

## Verify
- [ ] Tests cover known values, null elements inside collection/object arguments, null
  and unknown values for parameters that allow them, and each error path.

## Checked
2026-11-08. Confirmed against the three cited framework pages: `NewArgumentFuncError`,
`NewFuncError`, `ConcatFuncErrors`, `FuncErrorFromDiags`, error output shapes,
`function.NewArgumentsData`/`NewResultData`, `tfversion.SkipBelow(Version1_8_0)`,
`required_providers` note and the recommended test cases. Parameter validators
(`function.StringParameterValidator`, `ValidateableParameter`) confirmed on the
framework validation page and the parameters page. Removed: the "framework 1.8+" claim,
the claim that unknown arguments are withheld from `Run`, and the "no TF_ACC needed"
claim.
Method: documentation only; no commands were run.
