---
id: computing-software.software-engineering.csharp-dotnet.openapi-documents-in-aspnet-core
name: openapi-documents-in-aspnet-core
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-openapi, swashbuckle, microsoft-aspnetcore-openapi, scalar, openapi-transformers, aspnet-core]
level: practitioner
status: docs-checked
description: "Generate accurate OpenAPI documents from ASP.NET Core: Microsoft.AspNetCore.OpenApi (.NET 9+) vs Swashbuckle, typed results, transformers for auth, build-time docs and UI."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/customize-openapi", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/aspnetcore-openapi"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI documents in ASP.NET Core

**Goal:** a spec that matches real behaviour (status codes, schemas, auth), good enough
to generate clients from.

## Built-in generator (.NET 9 and later)
```csharp
builder.Services.AddOpenApi(o =>
{
    o.AddDocumentTransformer<BearerSecuritySchemeTransformer>();
});
if (app.Environment.IsDevelopment())
    app.MapOpenApi();                                // /openapi/{documentName}.json, JSON by default
```
The docs sample restricts the endpoint to Development to avoid exposing sensitive information in production. `MapOpenApi("/openapi/{documentName}.yaml")` serves YAML. ASP.NET Core generates documents only; UIs such as Swagger UI or Scalar are not included and must be added separately.

## Make responses explicit
```csharp
app.MapGet("/orders/{id:guid}", async Task<Results<Ok<OrderDto>, NotFound>> (Guid id, IOrders orders) =>
        await orders.Find(id) is { } o ? TypedResults.Ok(o) : TypedResults.NotFound())
   .WithName("GetOrder")
   .WithSummary("Get an order by id")
   .WithTags("Orders")
   .ProducesProblem(StatusCodes.Status500InternalServerError);
```
In minimal APIs, metadata comes from attributes, extension methods (`WithName` sets the operationId, `WithSummary`, `WithTags`, `Produces`) and returning `TypedResults`. Controllers use attributes such as `[Produces]`/`[ProducesResponseType]`. ASP.NET Core can also use XML doc comments when the project generates the XML documentation file.

## Transformers
```csharp
internal sealed class BearerSecuritySchemeTransformer : IOpenApiDocumentTransformer
{
    public Task TransformAsync(OpenApiDocument doc, OpenApiDocumentTransformerContext ctx, CancellationToken ct)
    {
        doc.Components ??= new();
        doc.Components.SecuritySchemes["Bearer"] = new OpenApiSecurityScheme
            { Type = SecuritySchemeType.Http, Scheme = "bearer", BearerFormat = "JWT" };
        return Task.CompletedTask;
    }
}
```
Operation transformers (`IOpenApiOperationTransformer`) adjust individual operations, for example adding security requirements per operation based on endpoint metadata; schema transformers (`IOpenApiSchemaTransformer`) adjust schemas.

## Build-time generation
```xml
<PackageReference Include="Microsoft.Extensions.ApiDescription.Server" PrivateAssets="all" />   <!-- version per your target framework -->
```
With this package installed, `dotnet build` generates the OpenAPI documents during build and writes them to the output directory (the docs show `obj/{ProjectName}.json`). The generated document can be diffed in PRs.

## Gotchas
- Don't expose the OpenAPI endpoint publicly in production unless intended; the docs show `MapOpenApi` combined with authorization and caching options.
- Check the generated schemas against your JSON serializer settings so the schema and wire format agree.

## Verify
- [ ] Generated spec lists every non-200 response the endpoint can return.
- [ ] Spec diffed in CI; a client generated from it compiles and passes a smoke test.

## Checked

Checked 2026-10-25 against aspnet/AspNetCore.Docs (fundamentals/openapi: overview, aspnetcore-openapi, customize-openapi, include-metadata, openapi-comments, using-openapi-documents) on main.
Confirmed: built-in OpenAPI support from .NET 9 via `Microsoft.AspNetCore.OpenApi`; `AddOpenApi`/`MapOpenApi`, JSON default and `{documentName}` route, YAML option; endpoint restricted to Development in the sample; no bundled UI (Swagger UI, Scalar listed as add-ons); document, operation and schema transformer interfaces; minimal API metadata via `WithName`, `WithSummary`, `WithTags`, `Produces`, `TypedResults`; XML doc comment support; `Microsoft.Extensions.ApiDescription.Server` generates documents at build time into the output directory.
Removed as unconfirmed: Scalar API call, Swashbuckle template history, `OpenApiDocumentsDirectory`, version pin, oasdiff/Spectral, `ConfigureHttpJsonOptions` and nullable schema claims, `RequireAuthorization` snippet claim, the "only 200" behaviour of untyped results.

Method: documentation only; no commands were run.
