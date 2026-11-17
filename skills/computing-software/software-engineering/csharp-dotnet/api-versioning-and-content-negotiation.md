---
id: computing-software.software-engineering.csharp-dotnet.api-versioning-and-content-negotiation
name: api-versioning-and-content-negotiation
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-controllers, api-versioning, content-negotiation, asp-versioning, produces, formatters]
level: practitioner
status: draft
description: "Version ASP.NET Core APIs with Asp.Versioning (URL, header, media type), deprecate safely, and control content negotiation with Accept, Produces and custom formatters."
sources: ["https://github.com/dotnet/aspnet-api-versioning/wiki", "https://learn.microsoft.com/en-us/aspnet/core/web-api/advanced/formatting", "https://learn.microsoft.com/en-us/aspnet/core/web-api/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# API versioning and content negotiation

## Versioning (Asp.Versioning.Mvc / Asp.Versioning.Http packages)
```csharp
builder.Services.AddApiVersioning(o => {
    o.DefaultApiVersion = new ApiVersion(1, 0);
    o.AssumeDefaultVersionWhenUnspecified = true;
    o.ReportApiVersions = true;                                   // api-supported-versions / api-deprecated-versions headers
    o.ApiVersionReader = ApiVersionReader.Combine(new UrlSegmentApiVersionReader(), new HeaderApiVersionReader("x-api-version"));
}).AddMvc().AddApiExplorer(o => o.GroupNameFormat = "'v'VVV");

[ApiController, ApiVersion("1.0", Deprecated = true), ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public class OrdersController : ControllerBase {
    [HttpGet, MapToApiVersion("2.0")] public IActionResult GetV2() => Ok();
}
```
Minimal APIs: `app.NewApiVersionSet().HasApiVersion(1.0).Build()` then `.WithApiVersionSet(set).MapToApiVersion(1.0)`. Pick one scheme: URL segment is simplest and cacheable; header/media-type keeps URLs stable. Only bump the major version for breaking changes; additive fields are not breaking. Announce deprecation via `Deprecated` plus `Sunset` header and docs.

## Content negotiation
MVC picks the output formatter from the `Accept` header. JSON (System.Text.Json) is default; add XML with `AddXmlSerializerFormatters()`. 
```csharp
builder.Services.AddControllers(o => { o.ReturnHttpNotAcceptable = true; o.RespectBrowserAcceptHeader = false; });
[Produces("application/json")] [Consumes("application/json")]
[ProducesResponseType<OrderDto>(200)] [ProducesResponseType<ProblemDetails>(404)]
```
`ReturnHttpNotAcceptable` yields 406 for unsupported types instead of silently using JSON. Custom formats: derive `TextOutputFormatter`/`TextInputFormatter` (e.g. CSV) and add to `o.OutputFormatters`. Vendor media types (`application/vnd.acme.v2+json`) pair with `MediaTypeApiVersionReader`.

## Gotchas
- Returning `string` bypasses JSON formatter (text/plain); return `Ok(obj)`.
- `Produces` also drives OpenAPI; keep accurate.
- Different versions should share services, not copy controllers.
- Unspecified-version defaults can lock you in; prefer explicit.

## Verify
Tests: `GET /api/v1/orders` and `/v2` return the right shapes; `Accept: application/xml` returns 406 when XML is not enabled; response headers list supported versions.
