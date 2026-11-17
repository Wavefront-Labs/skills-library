---
id: computing-software.cloud-infrastructure-engineering.terraform.plugin-framework-data-sources
name: plugin-framework-data-sources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, framework-data-source, terraform-plugin-framework, provider-development, datasource-read, schema, acceptance-tests]
level: practitioner
status: docs-checked
description: "Implement a data source in the Terraform Plugin Framework: Metadata, Schema, Configure for the API client, Read from config into state, diagnostics and provider registration."
sources:
  - https://developer.hashicorp.com/terraform/plugin/framework/data-sources
  - https://developer.hashicorp.com/terraform/tutorials/providers-plugin-framework/providers-plugin-framework-data-source-read
  - https://developer.hashicorp.com/terraform/plugin/testing/acceptance-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Implementing data sources in the Plugin Framework

Data sources let Terraform reference external data. Terraform does not manage their lifecycle and they are intended to have no side-effects.

## Skeleton
```go
package provider

import (
    "context"
    "fmt"
    "github.com/hashicorp/terraform-plugin-framework/datasource"
    "github.com/hashicorp/terraform-plugin-framework/datasource/schema"
    "github.com/hashicorp/terraform-plugin-framework/types"
)

var _ datasource.DataSourceWithConfigure = &teamDataSource{}

func NewTeamDataSource() datasource.DataSource { return &teamDataSource{} }

type teamDataSource struct{ client *api.Client }

type teamModel struct {
    Name    types.String `tfsdk:"name"`
    ID      types.String `tfsdk:"id"`
    Members types.List   `tfsdk:"members"`
}

func (d *teamDataSource) Metadata(_ context.Context, req datasource.MetadataRequest, resp *datasource.MetadataResponse) {
    resp.TypeName = req.ProviderTypeName + "_team"
}

func (d *teamDataSource) Schema(_ context.Context, _ datasource.SchemaRequest, resp *datasource.SchemaResponse) {
    resp.Schema = schema.Schema{
        Attributes: map[string]schema.Attribute{
            "name":    schema.StringAttribute{Required: true},
            "id":      schema.StringAttribute{Computed: true},
            "members": schema.ListAttribute{Computed: true, ElementType: types.StringType},
        },
    }
}

func (d *teamDataSource) Configure(_ context.Context, req datasource.ConfigureRequest, resp *datasource.ConfigureResponse) {
    if req.ProviderData == nil { return }   // Terraform sets ProviderData after the ConfigureProvider RPC
    c, ok := req.ProviderData.(*api.Client)
    if !ok { resp.Diagnostics.AddError("Unexpected Data Source Configure Type", fmt.Sprintf("got %T", req.ProviderData)); return }
    d.client = c
}

func (d *teamDataSource) Read(ctx context.Context, req datasource.ReadRequest, resp *datasource.ReadResponse) {
    var cfg teamModel
    resp.Diagnostics.Append(req.Config.Get(ctx, &cfg)...)
    if resp.Diagnostics.HasError() { return }

    team, err := d.client.GetTeamByName(ctx, cfg.Name.ValueString())   // api.Client is your own client type
    if err != nil { resp.Diagnostics.AddError("Unable to Read Team", err.Error()); return }

    cfg.ID = types.StringValue(team.ID)
    members, diags := types.ListValueFrom(ctx, types.StringType, team.Members)
    resp.Diagnostics.Append(diags...)
    cfg.Members = members
    resp.Diagnostics.Append(resp.State.Set(ctx, &cfg)...)
}
```

## What the interfaces require
- `datasource.DataSource` needs `Metadata`, `Schema` and `Read`. `Metadata` sets the type name: provider type prefix, an underscore, then the data source name (`req.ProviderTypeName` carries the provider name set in the provider's own `Metadata`).
- `Configure` is optional (`DataSourceWithConfigure`); it fetches the client the provider configured. Add a nil check on `req.ProviderData`, because Terraform sets it after calling the `ConfigureProvider` RPC.
- `Read` has no plan or prior state, only configuration: read `req.Config`, fetch the remote data, write `resp.State`. Warning or error diagnostics go in `resp.Diagnostics`.
- Terraform calls the `ReadDataSource` RPC during `terraform apply`, `terraform plan` and `terraform refresh`.
- Register it through the provider's `DataSources` method (`provider.ProviderWithDataSources`): `return []func() datasource.DataSource{NewTeamDataSource}`.

## Design notes
- The reference page's example models use `types.String` and similar framework types; the tutorial also maps list data into Go slices of model structs. Pick per attribute; framework types are the ones that can represent null and unknown.
- Report API failures as error diagnostics, as the tutorial does ("Unable to Read HashiCups Coffees").

## Tests
Acceptance tests use the terraform-plugin-testing framework with `go test`: put them in a `_test.go` file, give the function a name starting `TestAcc`, and set `TF_ACC` (any value) or the tests do not run. Run all of them with `TF_ACC=1 go test -v ./...`. They run a real Terraform binary and can create real infrastructure, so use a separate account. Test case structure (steps and state checks) is on the testing framework's Test Cases pages, which this skill does not cover.

## Checked
Date: 2026-11-07. Read in full: the data sources reference page (Define Data Source Type, Metadata, Schema, Read, Add Data Source to Provider), the whole "Implement data source" tutorial (Configure with the nil check and DataSourceWithConfigure, the Schema, models and Read steps) and the acceptance-tests page (TestAcc prefix, TF_ACC, `TF_ACC=1 go test -v ./...`, separate-account recommendation).
Removed because no read page states them: "every Computed attribute must be set known, unknown is an error", "Terraform defers the read to apply when inputs are unknown", the not-found / `found` attribute advice, `tfplugindocs generate`, and the `statecheck` / `knownvalue` test code and the `-run` test invocation (the Test Cases pages were not opened). Removed the unsourced Verify checklist. The `api.Client` type in the skeleton is the skill's own illustrative client, not a framework type.
Method: documentation only; no commands were run.
