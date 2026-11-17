---
id: computing-software.cloud-infrastructure-engineering.terraform.implementing-provider-functions-in-the-plugin-framework
name: implementing-provider-functions-in-the-plugin-framework
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-development, function-definition, function-implementation, tofu-provider-functions, plugin-framework, go]
level: sme
status: docs-checked
description: "Implement a provider-defined function with terraform-plugin-framework (definition, Run, errors, tests) and know OpenTofu differences in calling and configuring them."
sources: ["https://developer.hashicorp.com/terraform/plugin/framework/functions/implementation", "https://developer.hashicorp.com/terraform/plugin/framework/functions/testing", "https://opentofu.org/docs/language/functions/#provider-defined-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing a provider function

Provider-defined functions are supported in Terraform 1.8 and later. Implement the `function.Function` interface, then add the function to the provider.

## Register
```go
var _ provider.ProviderWithFunctions = &acmeProvider{}

func (p *acmeProvider) Functions(_ context.Context) []func() function.Function {
    return []func() function.Function{ NewSlugFunction }
}
```

## Define and run
```go
type slugFunction struct{}

func NewSlugFunction() function.Function { return &slugFunction{} }

func (f *slugFunction) Metadata(_ context.Context, _ function.MetadataRequest, resp *function.MetadataResponse) {
    resp.Name = "slug"
}

func (f *slugFunction) Definition(_ context.Context, _ function.DefinitionRequest, resp *function.DefinitionResponse) {
    resp.Definition = function.Definition{
        Summary:     "Convert a string to a DNS-safe slug.",
        Parameters:  []function.Parameter{ function.StringParameter{Name: "input"} },
        VariadicParameter: function.Int64Parameter{Name: "max_length"},
        Return:      function.StringReturn{},
    }
}

func (f *slugFunction) Run(ctx context.Context, req function.RunRequest, resp *function.RunResponse) {
    var input string
    var max []int64
    resp.Error = function.ConcatFuncErrors(resp.Error, req.Arguments.Get(ctx, &input, &max))
    if resp.Error != nil { return }
    out := slugify(input, max)
    if out == "" {
        resp.Error = function.ConcatFuncErrors(resp.Error, function.NewArgumentFuncError(0, "input produces an empty slug"))
        return
    }
    resp.Error = function.ConcatFuncErrors(resp.Error, resp.Result.Set(ctx, out))
}
```
`slugify` is your own helper. Usage: `provider::acme::slug(var.name, 40)`.

## Rules
- `Metadata` sets the function name WITHOUT the provider name (the call syntax adds the provider name).
- `Return` is required; `Parameters` are ordered and may be zero or more. An optional
  `VariadicParameter` takes zero or more values of one type after the final parameter, and is
  read as a Go slice (or the framework tuple type).
- Only argument data is provided to `Run`.
- By default Terraform does not pass null or unknown values to the provider logic. Set
  `AllowNullValue` / `AllowUnknownValues` on a parameter to allow them: null needs a pointer or
  framework type, unknown needs a framework type when reading the argument.
- Use `function.NewArgumentFuncError(index, msg)` to point at an argument; the index is
  zero-based. For a variadic element, add the number of non-variadic parameters to the element
  index.
- Set `DeprecationMessage` on the definition when deprecating a function, with an actionable message.

## Testing
Acceptance-style tests use `resource.UnitTest` with real configurations:
```go
resource.UnitTest(t, resource.TestCase{
    TerraformVersionChecks: []tfversion.TerraformVersionCheck{ tfversion.SkipBelow(tfversion.Version1_8_0) },
    ProtoV6ProviderFactories: map[string]func() (tfprotov6.ProviderServer, error){
        "acme": providerserver.NewProtocol6WithError(provider.New()),
    },
    Steps: []resource.TestStep{{
        Config: `output "t" { value = provider::acme::slug("Hello World!") }`,
        ConfigStateChecks: []statecheck.StateCheck{
            statecheck.ExpectKnownOutputValue("t", knownvalue.StringExact("hello-world")),
        },
    }},
})
```
- `TestStep.Config` injects a `required_providers` entry automatically; with `ConfigFile` or
  `ConfigDirectory` you must add the `required_providers` block yourself.
- Cover at least: known values, null elements inside list/map/object/set parameters, null and
  unknown values where those are allowed, and argument validation errors.
- For broad input testing (generic data functions, fuzzing), unit test `Run` directly with
  `function.NewArgumentsData` and `function.NewResultData`.

## OpenTofu differences
- Same `provider::name::function` syntax, from OpenTofu 1.7.0.
- OpenTofu also supports provider aliases: `provider::<provider_name>::<provider_alias>::<function_name>`.
- Functions are scoped to the module that requires the provider and are not inherited by child modules.
- Provider functions were added in protocol versions 5.5 and 6.5; OpenTofu says providers that
  supply functions may be configured. Do not rely on OpenTofu-only behaviour if the provider
  must also work on Terraform.

## Checked
Date: 2026-11-07. Read in full: the framework "Implement provider-defined functions" page, the "Testing functions" page and the OpenTofu Functions page (Provider-defined Functions section). Confirmed: Terraform 1.8+, `function.Function` interface, Metadata name without provider name, Return/Parameters/VariadicParameter semantics, AllowNullValue/AllowUnknownValues rules, `NewArgumentFuncError` index handling for variadics, `DeprecationMessage`, `provider.ProviderWithFunctions`, test constructs (`resource.UnitTest`, `tfversion.SkipBelow(tfversion.Version1_8_0)`, `ExpectKnownOutputValue`, `knownvalue.StringExact`, required_providers injection, test recommendations, `NewArgumentsData`/`NewResultData`), OpenTofu 1.7.0, alias syntax, module scoping, protocol 5.5/6.5. Trims: removed the "pure functions" and "unknown args make the result unknown without calling Run" claims, the OpenTofu "dynamic-schema functions" claim, and the Verify steps (TF_ACC behaviour, tfplugindocs output page) because the pages do not confirm them; ConcatFuncErrors calls now match the page's two-argument form; the provider factory placeholder replaced with the page's map form. The function documentation page was not read.
Method: documentation only; no commands were run.
